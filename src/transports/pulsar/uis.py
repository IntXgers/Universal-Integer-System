# universal_integer_system/uis.py
from typing import Dict,Any,Callable,Optional,List
import asyncio
import json
import time
import uuid
import structlog
from metrics import Metrics
from structlog import get_logger

from src.core.discovery import StreamlinedDiscoveryTranslator
from src.transports.pulsar.config import PulsarConfig
from src.transports.pulsar.pulsar_connection_manager import PulsarConnectionManager
from src.transports.pulsar.pulsar_manager import PulsarManager

logger = structlog.get_logger ()


class UniversalSystem:
    """The main system with comprehensive monitoring and observability"""

    def __init__ (self,enable_metrics=True,metrics_port=9090):
        self._configured = False
        self._config: Optional [PulsarConfig] = None
        self._connection: Optional [PulsarConnectionManager] = None
        self._manager: Optional [PulsarManager] = None
        self._handlers: Dict [int,List [Callable]] = {}
        self._running = False
        self._consumers = []

        # Setup logging
        logging=Logger ()

        # Setup metrics
        self.metrics = Metrics (port=metrics_port)
        if enable_metrics:
            self.metrics.start_server ()

        # Bind logger with context
        self.logger = logger.bind (component="universal_system")

        self.logger.info (
            "Universal Integer System initialized",
            metrics_enabled=enable_metrics,
            metrics_port=metrics_port
            )

    def configure (self,**kwargs):
        """Configure with observability"""
        trace_id = str (uuid.uuid4 ())
        config_logger = self.logger.bind (trace_id=trace_id,operation="configure")

        config_logger.info ("Configuring system",config=kwargs)

        try:
            self._config = Config.from_env (**kwargs)
            self._connection = PulsarConnectionManager (self._config,self.metrics)
            self._manager = PulsarManager (self._connection,self._config,self.metrics)
            self._configured = True

            config_logger.info (
                "System configured successfully",
                pulsar_url=self._config.pulsar_url,
                tenant=self._config.tenant,
                namespace=self._config.namespace
                )

        except Exception as e:
            self.metrics.errors.labels (type='configuration',operation='configure').inc ()
            config_logger.error ("Configuration failed",error=str (e))
            raise

    async def send (self,code: int,data: Dict [str,Any],topic: str = None):
        """Send event with full metrics and tracing"""
        if not self._configured:
            self.configure ()

        # Create trace context
        trace_id = str (uuid.uuid4 ())
        message_logger = self.logger.bind (
            trace_id=trace_id,
            code=code,
            operation="send"
            )

        start_time = time.time ()

        try:
            # Determine topic
            if topic is None:
                topic = self._get_topic_for_code (code)

            # Translate code
            code_name = StreamlinedDiscoveryTranslator ().translate_code (code)
            system = StreamlinedDiscoveryTranslator ().get_system_for_code (code)

            # Track translation
            self.metrics.code_translations.labels (code=str (code),system=system).inc ()

            # Get producer
            producer = self._manager.get_producer (topic)

            # Create event with trace ID
            event = {
                "code":code,
                "name":code_name,
                "data":data,
                "timestamp":time.time (),
                "version":"1.0",
                "trace_id":trace_id
                }

            # Send with metrics
            send_start = time.time ()
            await asyncio.get_event_loop ().run_in_executor (
                None,
                producer.send,
                json.dumps (event).encode ('utf-8')
                )

            # Update metrics
            send_duration = time.time () - send_start
            self.metrics.send_latency.labels (topic=topic).observe (send_duration)
            self.metrics.messages_sent.labels (
                code=str (code),
                topic=topic,
                status='success'
                ).inc ()

            total_duration = time.time () - start_time
            message_logger.info (
                "Message sent successfully",
                topic=topic,
                code_name=code_name,
                send_duration=send_duration,
                total_duration=total_duration
                )

        except Exception as e:
            self.metrics.messages_sent.labels (
                code=str (code),
                topic=topic or "unknown",
                status='failed'
                ).inc ()
            self.metrics.errors.labels (type='send',operation='send').inc ()

            message_logger.error (
                "Failed to send message",
                error=str (e),
                topic=topic
                )
            raise

    async def _consume_topic (self,topic: str):
        """Consume with comprehensive monitoring"""
        consumer_logger = self.logger.bind (
            topic=topic,
            operation="consume"
            )

        subscription = f"{self._config.namespace}-subscription"
        consumer = self._manager.get_consumer ([topic],subscription)

        consumer_logger.info ("Starting consumer",subscription=subscription)

        while self._running:
            try:
                msg = await asyncio.get_event_loop ().run_in_executor (
                    None,
                    lambda:consumer.receive (timeout_millis=1000)
                    )

                if msg:
                    receive_time = time.time ()

                    try:
                        # Parse event
                        event_data = json.loads (msg.data ().decode ('utf-8'))
                        trace_id = event_data.get ('trace_id',str (uuid.uuid4 ()))

                        # Create logger with trace context
                        event_logger = consumer_logger.bind (
                            trace_id=trace_id,
                            code=event_data ['code']
                            )

                        event = Event (
                            code=event_data ['code'],
                            data=event_data ['data'],
                            metadata={
                                'timestamp':event_data.get ('timestamp'),
                                'version':event_data.get ('version'),
                                'trace_id':trace_id
                                }
                            )

                        # Track receive
                        self.metrics.messages_received.labels (
                            code=str (event.code),
                            topic=topic,
                            status='success'
                            ).inc ()

                        # Process handlers with timing
                        if event.code in self._handlers:
                            for handler in self._handlers [event.code]:
                                handler_start = time.time ()

                                try:
                                    if asyncio.iscoroutinefunction (handler):
                                        await handler (event)
                                    else:
                                        handler (event)

                                    handler_duration = time.time () - handler_start
                                    self.metrics.message_processing_duration.labels (
                                        code=str (event.code),
                                        handler=handler.__name__
                                        ).observe (handler_duration)

                                except Exception as e:
                                    self.metrics.errors.labels (
                                        type='handler',
                                        operation=handler.__name__
                                        ).inc ()
                                    event_logger.error (
                                        "Handler failed",
                                        handler=handler.__name__,
                                        error=str (e)
                                        )

                        # Acknowledge
                        consumer.acknowledge (msg)

                        processing_time = time.time () - receive_time
                        event_logger.info (
                            "Message processed",
                            processing_time=processing_time
                            )

                    except Exception as e:
                        self.metrics.messages_received.labels (
                            code='unknown',
                            topic=topic,
                            status='failed'
                            ).inc ()
                        consumer_logger.error (
                            "Failed to process message",
                            error=str (e)
                            )
                        consumer.negative_acknowledge (msg)

            except Exception as e:
                if self._running:
                    consumer_logger.error ("Consumer error",error=str (e))
                await asyncio.sleep (1)

    async def health_check (self) -> dict:
        """Comprehensive health check"""
        health = {
            "status":"healthy",
            "timestamp":time.time (),
            "components":{}
            }

        # Check connection
        if self._connection:
            health ["components"] ["connection"] = self._connection.health_check ()

        # Check manager
        if self._manager:
            health ["components"] ["manager"] = self._manager.health_check ()

        # Check consumers
        health ["components"] ["consumers"] = {
            "total":len (self._consumers),
            "active":sum (1 for c in self._consumers if not c.done ())
            }

        # Overall status
        if any (
                c.get ("status") == "unhealthy"
                for c in health ["components"].values ()
                if isinstance (c,dict)
                ):
            health ["status"] = "unhealthy"
        elif any (
                c.get ("status") == "degraded"
                for c in health ["components"].values ()
                if isinstance (c,dict)
                ):
            health ["status"] = "degraded"

        return health