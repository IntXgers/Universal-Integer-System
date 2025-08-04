# universal_integer_system/src/transports/metrics.py
from prometheus_client import Counter,Histogram,Gauge,Info
from prometheus_client import start_http_server
import time
from functools import wraps
import structlog


logger = structlog.get_logger ()


class Metrics:
    """Comprehensive metrics for the Universal Integer System"""

    def __init__ (self,port: int = 9090):
        self.port = port

        # System Info
        self.system_info = Info (
            'universal_integer_system_info',
            'Universal Integer System information'
            )
        self.system_info.info (
            {
                'version':'1.0.0',
                'pulsar_enabled':'true'
                }
            )

        # Connection Metrics
        self.connections_total = Counter (
            'uis_connections_total',
            'Total number of Pulsar connections created',
            ['status']
            )
        self.active_connections = Gauge (
            'uis_active_connections',
            'Current number of active Pulsar connections'
            )

        # Message Metrics
        self.messages_sent = Counter (
            'uis_messages_sent_total',
            'Total messages sent',
            ['code','topic','status']
            )
        self.messages_received = Counter (
            'uis_messages_received_total',
            'Total messages received',
            ['code','topic','status']
            )
        self.message_processing_duration = Histogram (
            'uis_message_processing_duration_seconds',
            'Time spent processing messages',
            ['code','handler'],
            buckets=(0.001,0.005,0.01,0.05,0.1,0.5,1.0,5.0)
            )

        # Producer/Consumer Metrics
        self.active_producers = Gauge (
            'uis_active_producers',
            'Number of active producers',
            ['topic']
            )
        self.active_consumers = Gauge (
            'uis_active_consumers',
            'Number of active consumers',
            ['topic']
            )

        # Integer Code Metrics
        self.code_translations = Counter (
            'uis_code_translations_total',
            'Total integer code translations',
            ['code','system']
            )
        self.unknown_codes = Counter (
            'uis_unknown_codes_total',
            'Unknown codes encountered',
            ['code']
            )

        # Performance Metrics
        self.send_latency = Histogram (
            'uis_send_latency_seconds',
            'Message send latency',
            ['topic'],
            buckets=(0.001,0.005,0.01,0.05,0.1,0.5,1.0)
            )
        self.batch_size = Histogram (
            'uis_batch_size',
            'Producer batch sizes',
            ['topic'],
            buckets=(1,10,50,100,500,1000)
            )

        # Error Metrics
        self.errors = Counter (
            'uis_errors_total',
            'Total errors',
            ['type','operation']
            )

        # Health Metrics
        self.health_checks = Counter (
            'uis_health_checks_total',
            'Health check executions',
            ['component','status']
            )
        self.last_health_check = Gauge (
            'uis_last_health_check_timestamp',
            'Timestamp of last health check',
            ['component']
            )

    def start_server (self):
        """Start Prometheus metrics server"""
        start_http_server (self.port)
        logger.info (f"📊 Metrics server started on port {self.port}")

    def track_duration (self,metric: Histogram,**labels):
        """Decorator to track operation duration"""

        def decorator (func):
            @wraps (func)
            def wrapper (*args,**kwargs):
                start = time.time ()
                try:
                    result = func (*args,**kwargs)
                    return result
                finally:
                    duration = time.time () - start
                    metric.labels (**labels).observe (duration)

            return wrapper

        return decorator