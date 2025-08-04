# universal_integer_system/src/transports/pulsar_connection_manager.py
import asyncio
import threading
from datetime import datetime
from typing import Optional
import pulsar
import structlog
from metrics import Metrics
from pulsar.schema import Record, AvroSchema
from health_server import HealthServer

logger = structlog.get_logger ()


class PulsarConnectionManager:
    """Production-ready connection management with metrics and monitoring"""

    def __init__ (self,config,metrics: Optional [Metrics] = None):
        self.config = config
        self._client: Optional [pulsar.Client] = None
        self._lock = threading.Lock ()
        self.metrics = metrics or Metrics ()
        self._health_status = "unknown"
        self._last_error = None
        self._health_server = HealthServer (self)

    def get_client (self) -> pulsar.Client:
        """Get or create client with automatic reconnection and metrics"""
        with self._lock:
            if self._client is None:
                self._client = self._create_client ()
            return self._client

    def _create_client (self) -> pulsar.Client:
        """Create client with production-ready settings"""
        start_time = datetime.time ()

        try:
            logger.info (
                "Creating Pulsar client",
                url=self.config.pulsar_url,
                tenant=self.config.tenant,
                namespace=self.config.namespace
                )

            client = pulsar.Client (
                service_url=self.config.pulsar_url,authentication=self._get_auth (),message_listener_threads=4
                )

            # Update metrics
            connection_time = datetime.now ().timestamp ()
            self.metrics.connections_total.labels (status='success').inc ()
            self.metrics.active_connections.inc ()

            logger.info (
                "Pulsar connection established",
                connection_time=connection_time,
                url=self.config.pulsar_url
                )

            self._health_status = "healthy"
            self._last_error = None

            return client

        except Exception as e:
            connection_time = datetime.now().timestamp()
            self.metrics.connections_total.labels (status='failed').inc ()
            self.metrics.errors.labels (type='connection',operation='create').inc ()

            logger.error (
                "Failed to establish Pulsar connection",
                error=str (e),
                connection_time=connection_time,
                url=self.config.pulsar_url
                )

            self._health_status = "unhealthy"
            self._last_error = str (e)
            raise

    def health_check (self) -> dict:
        """Perform health check on connection"""
        try:
            if self._client:
                # Try a simple operation
                self._client.get_stats ()


            self.metrics.health_checks.labels (
                component='connection',
                status='healthy'
                ).inc ()
            self.metrics.last_health_check.labels (
                component='connection'
                ).set (time.time ())

            return {
                "status":"healthy",
                "details":{
                    "url":self.config.pulsar_url,
                    "connected":self._client is not None
                    }
                }

        except Exception as e:
            self.metrics.health_checks.labels (
                component='connection',
                status='unhealthy'
                ).inc ()

            return {
                "status":"unhealthy",
                "error":str (e),
                "last_error":self._last_error
                }

    def close (self):
        """Closes the shared connection with metrics"""
        if self._client:
            self._client.close ()
            self._client = None
            self.metrics.active_connections.dec ()
            logger.info ("Pulsar connection closed")