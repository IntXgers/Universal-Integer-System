# universal_integer_system/src/transports/health_server.py
from aiohttp import web
import json
from structlog import get_logger

logger = get_logger (__name__)



class HealthServer:
    """HTTP server for health checks and readiness probes"""

    def __init__ (self,system,port=8080):
        self.system = system
        self.port = port
        self.app = web.Application ()
        self.setup_routes ()

    def setup_routes (self):
        self.app.router.add_get ('/health',self.health)
        self.app.router.add_get ('/ready',self.ready)
        self.app.router.add_get ('/metrics',self.metrics)

    async def health (self,request):
        """Liveness probe endpoint"""
        health = await self.system.health_check ()
        status_code = 200 if health ['status'] == 'healthy' else 503
        return web.json_response (health,status=status_code)

    async def ready (self,request):
        """Readiness probe endpoint"""
        if self.system._configured and self.system._running:
            return web.json_response ({"ready":True},status=200)
        return web.json_response ({"ready":False},status=503)

    async def metrics (self,request):
        """Metrics endpoint (if not using Prometheus port)"""
        # This could return custom metrics in JSON format
        return web.json_response (
            {
                "messages_sent":self.system.metrics.messages_sent._value.sum (),
                "messages_received":self.system.metrics.messages_received._value.sum (),
                "active_producers":len (self.system._manager._producers),
                "active_consumers":len (self.system._consumers)
                }
            )

    async def start (self):
        """Start health server"""
        runner = web.AppRunner (self.app)
        await runner.setup ()
        site = web.TCPSite (runner,'0.0.0.0',self.port)
        await site.start ()
        logger.info (f"Health server started on port {self.port}")