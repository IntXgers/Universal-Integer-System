"""
Production Pulsar Client for Life Coach Development Containers
============================================================
Clean, focused Pulsar client using integer system integration.
No circular dependencies, production-ready patterns.
"""

import threading
import pulsar
from security import initialize_container_security
from structlog import getLogger

logger = getLogger(__name__)

# =============================================================================
# PULSAR CONNECTION SINGLETON - UPDATED WITH CONFIGURATION
# =============================================================================

class PulsarConnectionManager:
    """
    Single responsibility: Maintain efficient connection to Pulsar cluster.
    NOW SUPPORTS CONFIGURATION PARAMETERS!
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, broker_url="pulsar://localhost:6650", 
                # ADDED: Configuration parameters
                auth_token: str = None,
                enable_tls: bool = False,
                producer_batching: bool = True,
                batch_size: int = 1000,
                # Original parameters
                security_config=None, container_id=None, user_id=None, org_id=None, project_id=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize_connection(
                    broker_url, tenant, namespace, auth_token, enable_tls, 
                    producer_batching, batch_size, security_config, 
                    container_id, user_id, org_id, project_id
                )
            return cls._instance

    def _initialize_connection(self, broker_url, tenant, namespace, auth_token, enable_tls,
                              producer_batching, batch_size, security_config,
                              container_id, user_id, org_id, project_id):
        """Initialize Pulsar connection with configuration."""
        self._broker_url = broker_url
        # ADDED: Store configuration
        self.tenant = tenant
        self.namespace = namespace
        self.auth_token = auth_token
        self.enable_tls = enable_tls
        self.producer_batching = producer_batching
        self.batch_size = batch_size
        self.security = None

        # Initialize security if container details provided
        if container_id and user_id and org_id and project_id:
            try:
                self.security = initialize_container_security(
                    container_id, user_id, org_id, project_id, security_config
                )
                logger.info("🔒 Security initialized for Pulsar connection")
            except Exception as e:
                logger.error(f"Failed to initialize security: {e}")
                self.security = None
        else:
            logger.info("No security configuration provided - using insecure connection")

        # CHANGED: Create Pulsar client with configuration
        client_config = {'service_url': broker_url}

        # ADDED: Apply authentication if configured
        if auth_token:
            client_config['authentication'] = pulsar.AuthenticationToken(auth_token)

        # ADDED: Apply TLS configuration
        if enable_tls:
            client_config['use_tls'] = True
            if self.security:
                # Apply TLS configuration from security module
                client_config = self.security.configure_secure_pulsar_client(client_config)

        # ADDED: Configure batching
        if producer_batching:
            client_config['enable_batching'] = True
            client_config['batching_max_messages'] = batch_size

        try:
            self._client = pulsar.Client(**client_config)
            connection_type = "secure (TLS)" if enable_tls else "insecure"
            logger.info(f"🔗 Established {connection_type} Pulsar connection to {broker_url}")
            logger.info(f"📋 Tenant: {tenant}, Namespace: {namespace}")
        except Exception as e:
            logger.error(f"Failed to establish Pulsar connection: {e}")
            raise

    def get_client(self):
        """Returns the shared Pulsar client."""
        return self._client

    def get_security(self):
        """Returns the security configuration (None if not configured)."""
        return getattr(self, 'security', None)

    def get_broker_url(self):
        """Returns the broker URL."""
        return self._broker_url

    def get_tenant(self):
        """Returns the configured tenant."""
        return getattr(self, 'tenant', 'life-coach')

    def get_namespace(self):
        """Returns the configured namespace."""
        return getattr(self, 'namespace', 'code-gen')

    def is_secure(self):
        """Returns True if connection is using TLS."""
        return getattr(self, 'enable_tls', False)

    def is_batching_enabled(self):
        """Returns True if producer batching is enabled."""
        return getattr(self, 'producer_batching', True)

    def get_batch_size(self):
        """Returns the configured batch size."""
        return getattr(self, 'batch_size', 1000)

    def close(self):
        """Closes the shared connection."""
        if hasattr(self, '_client') and self._client:
            self._client.close()
            self._client = None
            connection_type = "secure" if self.is_secure() else "insecure"
            logger.info(f"🔌 Closed {connection_type} Pulsar connection")