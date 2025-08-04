#!/usr/bin/env python3 src/transports/config.py
"""
Container Configuration with Pydantic V2 Dataclasses
===================================================
Lightweight configuration for integer discovery and container layer.
Uses Pydantic V2 dataclasses for validation without BaseSettings bloat.
"""

import os
import uuid
from datetime import datetime
from typing import Optional,Dict,Any,List
from dataclasses import dataclass,field


def _get_pulsar_url ():
    """Get Pulsar URL with appropriate defaults"""
    url = os.getenv ('PULSAR_SERVICE_URL')
    if url:
        return url

    # Check if we're in development mode
    if os.getenv ('DEVELOPMENT_MODE','').lower () == 'true':
        return 'pulsar://localhost:6650'

    # Production mode - no defaults
    raise ValueError (
        "PULSAR_SERVICE_URL environment variable is required. "
        "For development, set DEVELOPMENT_MODE=true"
        )


@dataclass
class PulsarConfig:
    """Pulsar messaging configuration - unified for all containers"""
    service_url: str = field (default_factory=lambda:_get_pulsar_url ())
    tenant: str = field (default_factory=lambda:os.getenv ('PULSAR_TENANT','default'))
    container_id: str = field (default_factory=lambda:str (uuid.uuid4 ()))
    namespace: str = field (default_factory=lambda:os.getenv ('PULSAR_NAMESPACE','default'))
    auth_token: Optional [str] = field (default_factory=lambda:os.getenv ('PULSAR_AUTH_TOKEN'))
    broker_url: str = field (default_factory=lambda:os.getenv ('PULSAR_BROKER_URL'))
    container_type: int = 0  # From your integer system
    environment: int = field (default_factory=lambda:int (os.getenv ('CONTAINER_ENV','0')))
    version: str = "1.0.0"
    # Lifecycle tracking
    created_at: datetime = field (default_factory=datetime.utcnow)
    updated_at: datetime = field (default_factory=datetime.utcnow)
    status: int = 0  # From UniversalStatus
    # Autonomous system essentials
    priority: int = 60  # NORMAL priority
    resource_limits: Dict [str,Any] = field (
        default_factory=lambda:{
            "memory_mb":512,
            "cpu_cores":1,
            "disk_mb":1024
            }
        )
    # Health monitoring
    health_check_interval: int = 30
    timeout_seconds: int = 300
    # Container-specific metadata
    metadata: Dict [str,Any] = field (default_factory=dict)

    # Consumer settings
    consumer_subscription_name: str = field (
        default_factory=lambda:os.getenv ('PULSAR_SUBSCRIPTION','container-subscription')
        )

    def get_topic_name (self,topic: str) -> str:
        """Generate fully qualified topic name"""
        return f"persistent://{self.tenant}/{self.namespace}/{topic}"


@dataclass
class DatabaseConfig:
    """Database configuration for integer storage."""
    max_connections: int = field (default_factory=lambda:int (os.getenv ('MAX_CONNECTIONS','10')))
    url: str = field (default_factory=lambda:os.getenv ('DATABASE_URL','sqlite:///integer_codes.db'))
    timeout: float = field (default_factory=lambda:float (os.getenv ('DB_TIMEOUT','30.0')))
    tenant: str = field (default_factory=lambda:os.getenv ('DB_TENANT'))
    namespace: str = "code-gen",
    auth_token: str = None,
    enable_tls: bool = False,


@dataclass
class PulsarSecurityConfig:
    """Security-specific settings"""
    enable_tls: bool = False
    container_id: Optional [str] = None
    user_id: Optional [str] = None
    org_id: Optional [str] = None
    project_id: Optional [str] = None
    security_config: Optional [Dict [str,Any]] = None


@dataclass
class PulsarPerformanceConfig:
    """Performance and batching settings"""
    producer_batching: bool = True
    batch_size: int = 1000
    connection_timeout: int = 3000
    operation_timeout: int = 3000


@dataclass
class SecurityConfig:
    """Security and encryption configuration."""
    encryption_key: Optional [str] = field (default_factory=lambda:os.getenv ('ENCRYPTION_KEY'))
    jwt_secret: Optional [str] = field (default_factory=lambda:os.getenv ('JWT_SECRET'))
    tls_cert_path: Optional [str] = field (default_factory=lambda:os.getenv ('TLS_CERT_PATH'))
    tls_key_path: Optional [str] = field (default_factory=lambda:os.getenv ('TLS_KEY_PATH'))
    enable_tls: bool = field (default_factory=lambda:os.getenv ('ENABLE_TLS','false').lower () == 'true')


@dataclass
class IntegerServiceConfig:
    """Integer discovery service configuration."""
    service_name: str = field (default_factory=lambda:os.getenv ('SERVICE_NAME','integer-discovery'))
    discovery_file_path: str = field (
        default_factory=lambda:os.getenv ('DISCOVERY_FILE_PATH','/app/universal_integer_system.py')
        )
    cache_size: int = field (default_factory=lambda:int (os.getenv ('CACHE_SIZE','10000')))
    request_timeout: float = field (default_factory=lambda:float (os.getenv ('REQUEST_TIMEOUT','10.0')))


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = field (default_factory=lambda:os.getenv ('LOG_LEVEL','INFO'))
    format: str = field (default_factory=lambda:os.getenv ('LOG_FORMAT','json'))
    output: str = field (default_factory=lambda:os.getenv ('LOG_OUTPUT','stdout'))


@dataclass
class ContainerConfig:
    """Main container configuration combining all subsystems."""
    database: DatabaseConfig = field (default_factory=DatabaseConfig)
    pulsar: PulsarConfig = field (default_factory=PulsarConfig)
    security: SecurityConfig = field (default_factory=SecurityConfig)
    integer_service: IntegerServiceConfig = field (default_factory=IntegerServiceConfig)
    logging: LoggingConfig = field (default_factory=LoggingConfig)

    # Environment detection
    environment: str = field (default_factory=lambda:os.getenv ('ENVIRONMENT','development'))
    debug: bool = field (default_factory=lambda:os.getenv ('DEBUG','false').lower () == 'true')


from dataclasses import dataclass


@dataclass
class ContainerIdentity:
    """Core identity for the user project container."""
    user_id: str
    org_id: str
    project_id: str
    container_id: str = ""  # Auto-generated if empty

    def __post_init__ (self):
        if not self.container_id:
            self.container_id = f"{self.user_id}_{self.org_id}_{self.project_id}"

    def get_base_path (self) -> str:
        """Generate a base path for container resources."""
        return f"/containers/{self.user_id}/{self.org_id}/{self.project_id}"


@dataclass
class ContainerConsumerConfig:
    """Configuration for container consumer"""
    container_name: str
    subscription_name: str
    tenant: str
    namespace: str
    pulsar_url: str = "pulsar://localhost:6650"
    created_at: datetime = field (default_factory=datetime.now)
    updated_at: datetime = field (default_factory=datetime.now)
    # Additional topics to listen to (beyond own container topic)
    additional_topics: List [str] = None

    # Processing options
    max_retries: int = 3


@dataclass
class ContainerProducerConfig:
    """Configuration for container producer"""
    container_name: str = field (default_factory=lambda:os.getenv ('CONTAINER_NAME'))
    pulsar_url: str = field (default_factory=lambda:os.getenv ('PULSAR_URL','pulsar://localhost:6650'))
    tenant: str = field (default_factory=lambda:os.getenv ('PULSAR_TENANT','default'))
    namespace: str = field (default_factory=lambda:os.getenv ('PULSAR_NAMESPACE','default'))
    # Producer settings
    producer_batching_enabled: bool = field (
        default_factory=lambda:os.getenv ('PULSAR_BATCHING','true').lower () == 'true'
        )
    producer_batch_size: int = field (default_factory=lambda:int (os.getenv ('PULSAR_BATCH_SIZE','1000')))
    created_at: datetime = field (default_factory=datetime.now)
    updated_at: datetime = field (default_factory=datetime.now)

    # Simple metadata
    auto_add_timestamp: bool = True
    auto_add_message_id: bool = True
