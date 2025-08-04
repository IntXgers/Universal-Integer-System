# universal_integer_system/src/transports/pulsar_manager.py
import time
from typing import Dict,List,Optional
import pulsar
import structlog
from metrics import Metrics
from src.transports.pulsar.config import PulsarConfig


logger = structlog.get_logger ()


class PulsarManager:
    """High-level Pulsar operations with comprehensive monitoring"""

    def __init__ (self,connection,config,metrics: Optional [Metrics] = None):
        self.connection = connection
        self.config = PulsarConfig(config)
        self.metrics = metrics or Metrics ()
        self._producers: Dict [str,pulsar.Producer] = {}
        self._consumers: Dict [str,pulsar.Consumer] = {}

    def setup (self):
        """Setup topics and schemas with monitoring"""
        logger.info (
            "Setting up Pulsar manager",
            auto_create_namespace=self.config.auto_create_namespace
            )

        client = self.connection.get_client ()

        # Log successful setup
        logger.info (
            "Pulsar Manager setup complete",
            producers=len (self._producers),
            consumers=len (self._consumers)
            )

    def get_producer (self,topic: str) -> pulsar.Producer:
        """Get or create producer with metrics"""
        formatted_topic = self._format_topic (topic)

        if formatted_topic not in self._producers:
            start_time = time.time ()

            try:
                client = self.connection.get_client ()
                producer = client.create_producer (
                    topic=formatted_topic,
                    producer_name=f"{self.config.namespace}-producer-{topic}",
                    batching_enabled=True,
                    batching_max_messages=1000,
                    batching_max_allowed_size_in_bytes=131072,
                    batching_max_publish_delay_ms=10,
                    compression_type=pulsar.CompressionType.SNAPPY,
                    send_timeout_millis=30000,
                    max_pending_messages=50000,
                    )

                self._producers [formatted_topic] = producer
                self.metrics.active_producers.labels (topic=topic).inc ()

                creation_time = time.time () - start_time
                logger.info (
                    "Producer created",
                    topic=formatted_topic,
                    creation_time=creation_time
                    )

            except Exception as e:
                self.metrics.errors.labels (
                    type='producer_creation',
                    operation='get_producer'
                    ).inc ()
                logger.error (
                    "Failed to create producer",
                    topic=formatted_topic,
                    error=str (e)
                    )
                raise

        return self._producers [formatted_topic]

    def get_consumer (self,topics: List [str],subscription: str) -> pulsar.Consumer:
        """Create consumer with monitoring"""
        start_time = time.time ()
        formatted_topics = [self._format_topic (t) for t in topics]

        try:
            client = self.connection.get_client ()
            consumer = client.subscribe (
                topic=formatted_topics if len (formatted_topics) > 1 else formatted_topics [0],
                subscription_name=subscription,
                consumer_type=pulsar.ConsumerType.Shared,
                negative_ack_redelivery_delay_ms=60000,
                max_total_receiver_queue_size_across_partitions=50000,
                )

            for topic in topics:
                self.metrics.active_consumers.labels (topic=topic).inc ()

            creation_time = time.time () - start_time
            logger.info (
                "Consumer created",
                topics=formatted_topics,
                subscription=subscription,
                creation_time=creation_time
                )

            return consumer

        except Exception as e:
            self.metrics.errors.labels (
                type='consumer_creation',
                operation='get_consumer'
                ).inc ()
            logger.error (
                "Failed to create consumer",
                topics=formatted_topics,
                error=str (e)
                )
            raise

    def health_check (self) -> dict:
        """Check health of all producers and consumers"""
        healthy_producers = 0
        unhealthy_producers = 0

        for topic,producer in self._producers.items ():
            try:
                if producer.is_connected ():
                    healthy_producers += 1
                else:
                    unhealthy_producers += 1
            except:
                unhealthy_producers += 1

        return {
            "status":"healthy" if unhealthy_producers == 0 else "degraded",
            "producers":{
                "total":len (self._producers),
                "healthy":healthy_producers,
                "unhealthy":unhealthy_producers
                },
            "consumers":{
                "total":len (self._consumers)
                }
            }