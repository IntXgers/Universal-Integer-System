#!/usr/bin/env python3  src/transports/pulsar_producer.py
"""
Generic Container Producer - Real Pulsar Python Client
====================================================
Pure transport layer - just sends JSON messages to topics.
No knowledge of integer codes or business logic.
"""

import json
import time
import uuid
from typing import Dict,Any,Optional
from dataclasses import dataclass
from security import SetUpEncryption

import pulsar

from src.transports.pulsar.config import ContainerProducerConfig


class ContainerProducer:
    """Generic producer that works for any container type - pure transport"""

    def __init__ (self,config: ContainerProducerConfig):
        self.config = config
        self.client = None
        self.producer = None
        self.container_topic = f"{config.tenant}://{config.namespace}/{config.container_name}"

    def connect (self):
        """Connect to Pulsar"""
        if self.client is None:
            self.client = pulsar.Client (self.config.pulsar_url)
            self.producer = self.client.create_producer (
                topic=self.container_topic,
                producer_name=f"{self.config.container_name}_producer"
                )
            print (f"✅ {self.config.container_name} producer connected to {self.container_topic}")

    def send_message (self,message_data: Dict [str,Any]) -> str:
        """Send a message - pure transport, no business logic"""
        self.connect ()

        # Add basic metadata if configured
        if self.config.auto_add_timestamp and 'timestamp' not in message_data:
            message_data ['timestamp'] = int (time.time ()*1000)

        if self.config.auto_add_message_id and 'message_id' not in message_data:
            message_data ['message_id'] = str (uuid.uuid4 ())

        # Convert to JSON bytes and send
        message_bytes = json.dumps (message_data).encode ('utf-8')
        message_id = self.producer.send (message_bytes)

        return str (message_id)

    def close (self):
        """Clean shutdown"""
        if self.producer:
            self.producer.close ()
        if self.client:
            self.client.close ()
        print (f"✅ {self.config.container_name} producer closed")


def create_container_producer (container_name: str,pulsar_url: str = "pulsar://localhost:6650") -> ContainerProducer:
    """Create a producer for any container"""
    config = ContainerProducerConfig (
        container_name=container_name,
        pulsar_url=pulsar_url
        )
    return ContainerProducer (config)


# Example usage - pure transport, no business logic:
if __name__ == "__main__":
    # Any container type - now with custom tenant name
    producer = create_container_producer ("neural_mesh_001")

    # Topics now look like: life-coach://code-gen/neural_mesh_001
    producer.send_message (
        {
            "event_type":"pattern_discovered",
            "data":{"pattern":"optimization","confidence":0.85}
            }
        )

    # User container - topic: life-coach://code-gen/user_12345
    user_producer = create_container_producer ("user_12345")
    user_producer.send_message (
        {
            "action":"file_uploaded",
            "filename":"project.py"
            }
        )

    producer.close ()
    user_producer.close ()