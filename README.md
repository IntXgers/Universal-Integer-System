# Universal Integer System

🔢 **Stop reinventing status codes. Start speaking the same language.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## The Problem We Solve

Every distributed system reinvents the wheel:
- Service A: `{"status": "running"}` 
- Service B: `{"state": 2}` 
- Service C: `{"code": "ACTIVE"}`
- Your debugging session: 🤯

**Universal Integer System** provides a single source of truth for system communication. One integer, one meaning, everywhere.

## Why You Need This

```python
# Before: Chaos
if response.get('status') == 'active' or response.get('state') == 'running' or response.get('code') == 2:
    # Is this actually the same thing? Who knows!
    process_active_state()

# After: Clarity
from universal_integer_system import UniversalStatus

if response['code'] == UniversalStatus.ACTIVE:  # Always 11, everywhere
    process_active_state()
```

## Key Features

✨ **Self-Discovering** - Automatically finds and registers all integer codes  
🚀 **Zero Maintenance** - Add new codes, they're instantly available everywhere  
📊 **Production Ready** - Built-in metrics, monitoring, health checks  
🔍 **Traceable** - Every code knows its origin and purpose  
🌐 **Distributed** - Optional Pulsar integration for event streaming  
🛡️ **Immutable** - Codes never change meaning (unlike string constants)  

## Quick Start

### Installation

```bash
pip install universal-integer-system
```

### Basic Usage

```python
from universal_integer_system import UniversalStatus, translate_code

# Use standardized status codes
status = UniversalStatus.ACTIVE  # This is always 11
print(f"Status code: {status}")
print(f"Human readable: {translate_code(status)}")  # "active"

# Check status
if status == UniversalStatus.ACTIVE:
    print("System is running!")

# Built-in discovery
from universal_integer_system import discover

# Find all codes for a concept
codes = discover.find_codes_by_name("failed")
# Returns: [(32, 'failed'), (123, 'component.failed'), ...]
```

### Define Your Domain

```python
from enum import IntEnum

class PaymentEvent(IntEnum):
    """Payment events - Range: 12000-12099"""
    PAYMENT_INITIATED = 12000
    PAYMENT_AUTHORIZED = 12001
    PAYMENT_CAPTURED = 12002
    PAYMENT_FAILED = 12003
    PAYMENT_REFUNDED = 12004

# Your codes are automatically discoverable!
from universal_integer_system import translate_code

print(translate_code(12001))  # "payment.authorized"
```

## Architecture

The system uses a hierarchical integer space:

```
0-999:     Universal (shared by everyone)
├── 0-49:    Status (active, failed, etc.)
├── 50-69:   Priority levels
├── 70-89:   Severity/log levels  
└── 90-99:   Operation results

1000-1999: Authentication & Authorization
2000-3999: Infrastructure & Containers
4000-4999: Data & Storage
5000-5999: AI & Machine Learning
6000-6999: Business Logic
7000-7999: Monitoring & Observability
8000-8999: Integration & External Systems
9000-9999: Application-Specific
10000+:    Extended/Custom Ranges
```

## Real-World Example

```python
from universal_integer_system import (
    UniversalStatus,
    SystemEvent,
    translate_code,
    get_system_for_code
)

class OrderService:
    def process_order(self, order_id):
        # Emit standardized events
        self.emit_event(SystemEvent.COMPONENT_STARTED, {"component": "order_processor"})
        
        try:
            # Process the order
            self.update_status(order_id, UniversalStatus.PROCESSING)
            
            # ... business logic ...
            
            self.update_status(order_id, UniversalStatus.COMPLETED)
            self.emit_event(6124, {"order_id": order_id})  # ORDER_DELIVERED
            
        except Exception as e:
            self.update_status(order_id, UniversalStatus.FAILED)
            self.emit_event(SystemEvent.COMPONENT_FAILED, {
                "error": str(e),
                "order_id": order_id
            })
    
    def emit_event(self, code: int, data: dict):
        # Your existing event system just needs to include the code
        event = {
            "code": code,
            "name": translate_code(code),  # Human readable
            "system": get_system_for_code(code),  # Which subsystem
            "data": data
        }
        # Send to Pulsar, Kafka, RabbitMQ, etc.
```

## Advanced Features

### Automatic Discovery

```python
from universal_integer_system import StreamlinedDiscoveryTranslator

translator = StreamlinedDiscoveryTranslator()

# Get system statistics
stats = translator.get_system_summary()
print(f"Total defined codes: {stats['total_codes']}")

# Find codes by pattern
auth_codes = translator.find_codes_by_name("auth")

# Get detailed info about any code
info = translator.get_code_info(1001)
# {
#     'code': 1001,
#     'name': 'guest',
#     'system': 'auth.role',
#     'enum_class_name': 'UserRole'
# }
```

### Code Allocation Assistant

```python
# AI suggests where your new codes should go
suggestion = translator.suggest_code_allocation(
    "payment fraud detection system",
    estimated_size=20
)
# {
#     'suggested_system': 'business_logic',
#     'suggested_start_code': 6850,
#     'available_space': 150,
#     'rationale': 'Business concepts belong in business logic'
# }
```

### Distributed Systems (with Pulsar)

```python
from universal_integer_system import UniversalSystem

# Initialize the system
uis = UniversalSystem()
uis.configure(
    pulsar_url="pulsar://localhost:6650",
    tenant="your-org",
    namespace="production"
)

# Send events with automatic translation
await uis.send(
    code=UniversalStatus.ACTIVE,
    data={"service": "order-processor", "region": "us-east-1"}
)

# Subscribe to specific event codes
@uis.on(SystemEvent.COMPONENT_FAILED)
async def handle_component_failure(event):
    print(f"Component failed: {event.data}")
    # Auto-recovery logic here

# Start processing
await uis.start()
```

## Comparison

| Feature | String-based | HTTP Codes | Universal Integer System |
|---------|--------------|------------|-------------------------|
| Consistency | ❌ "active" vs "running" | ⚠️ Limited range | ✅ One code, one meaning |
| Discoverability | ❌ Grep and pray | ❌ Manual docs | ✅ Self-discovering |
| Performance | ❌ String comparison | ✅ Integer comparison | ✅ Integer + caching |
| Extensibility | ⚠️ Conflicts common | ❌ Fixed set | ✅ Unlimited ranges |
| Type Safety | ❌ Runtime errors | ⚠️ Magic numbers | ✅ Enums + validation |
| Monitoring | ❌ Parse first | ⚠️ Limited context | ✅ Built-in metrics |

## Who's This For?

- **Microservice Teams**: Finally speak the same language across services
- **Platform Engineers**: Standardize observability and monitoring  
- **AI/ML Systems**: Track model states and training events consistently
- **IoT Platforms**: Efficient integer codes for bandwidth-constrained devices
- **Anyone** tired of string-based status management

## Contributing

We love contributions! The system is designed to grow with community input.

## Adding New App Types

1. **Core Apps (16000-16499)**: Core team only
2. **Community Apps (16500-17999)**: 
   - Submit PR with justification
   - Must not duplicate existing functionality
   - Include documentation
3. **Regional Apps (18000-18999)**:
   - Must serve specific cultural/regional need
   - Include locale information
4. **Experimental (19000-19999)**:
   - Clearly mark as experimental
   - Include sunset date

```bash
# Clone the repo
git clone https://github.com/yourusername/universal-integer-system
cd universal-integer-system

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Plugin system for custom code ranges
- [ ] Code generation for different languages
- [ ] REST API for code discovery
- [ ] Integration examples (Kafka, RabbitMQ, etc.)
- [ ] Performance benchmarks
- [ ] Browser/JavaScript support

## Support

- 📖 [Documentation](https://universal-integer-system.readthedocs.io)
- 💬 [Discussions](https://github.com/yourusername/universal-integer-system/discussions)
- 🐛 [Issue Tracker](https://github.com/yourusername/universal-integer-system/issues)

---

Built with ❤️ for distributed systems everywhere.