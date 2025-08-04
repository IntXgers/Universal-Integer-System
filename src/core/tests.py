"""Test suite for the Universal Integer System discovery functionality."""

import pytest
from universal_integer_system import (
    UniversalStatus,
)
from discovery import translate_code, get_system_for_code, StreamlinedDiscoveryTranslator,

class TestBasicTranslation:
    """Test basic code translation functionality."""

    def test_translate_known_code(self):
        """Test translating a known status code."""
        assert translate_code(11) == "active"
        assert translate_code(UniversalStatus.ACTIVE) == "active"

    def test_translate_unknown_code(self):
        """Test translating an unknown code."""
        result = translate_code(99999)
        assert result.startswith("unknown_")
        assert "99999" in result

    def test_get_system_for_code(self):
        """Test system classification."""
        assert get_system_for_code(11) == "universal_foundation"
        assert get_system_for_code(1001) == "auth_system"
        assert get_system_for_code(5000) == "ai_ml"


class TestDiscoveryTranslator:
    """Test the discovery translator functionality."""

    @pytest.fixture
    def translator(self):
        """Create a translator instance."""
        return StreamlinedDiscoveryTranslator()

    def test_initialization(self, translator):
        """Test translator initializes correctly."""
        assert len(translator._code_registry) > 0
        assert translator._stats['discovery_errors'] >= 0

    def test_format_code_with_context(self, translator):
        """Test code formatting with context."""
        result = translator.format_code_with_context(11)
        assert "11" in result
        assert "active" in result
        assert "universal_foundation" in result

    def test_find_codes_by_name(self, translator):
        """Test searching codes by name."""
        results = translator.find_codes_by_name("failed")
        assert len(results) > 0
        assert all("failed" in r['name'] for r in results)

    def test_code_suggestion(self, translator):
        """Test code allocation suggestions."""
        suggestion = translator.suggest_code_allocation(
            "authentication service",
            estimated_size=10
        )
        assert suggestion['suggested_system'] == "auth_system"
        assert 'suggested_start_code' in suggestion
        assert suggestion['available_space'] >= 10

    def test_validate_code_addition(self, translator):
        """Test code validation."""
        # Test adding to existing code
        validation = translator.validate_code_addition(
            11, "test_code", "universal_foundation"
        )
        assert not validation['valid']
        assert any("already exists" in e for e in validation['errors'])

        # Test valid addition
        validation = translator.validate_code_addition(
            98, "new_test_code", "universal_foundation"
        )
        assert validation['valid']
        assert len(validation['errors']) == 0


class TestCodeImmutability:
    """Test that codes maintain immutability."""

    def test_enum_values_unchanged(self):
        """Ensure critical enum values haven't changed."""
        assert UniversalStatus.UNKNOWN == 0
        assert UniversalStatus.ACTIVE == 11
        assert UniversalStatus.FAILED == 32
        assert UniversalStatus.COMPLETED == 21

    def test_cannot_modify_enum(self):
        """Test that enum values cannot be modified."""
        with pytest.raises(AttributeError):
            UniversalStatus.ACTIVE = 999


class TestPerformance:
    """Test performance characteristics."""

    def test_translation_caching(self):
        """Test that translations are cached."""
        translator = StreamlinedDiscoveryTranslator()

        # First call
        translator.translate_code(1000)
        initial_cache_hits = translator._stats['cache_hits']

        # Second call should hit cache
        translator.translate_code(1000)
        assert translator._stats['cache_hits'] == initial_cache_hits + 1

    def test_bulk_translation_performance(self):
        """Test performance with many translations."""
        import time

        translator = StreamlinedDiscoveryTranslator()
        codes = list(range(1000, 2000))

        start = time.time()
        results = [translator.translate_code(c) for c in codes]
        duration = time.time() - start

        assert len(results) == 1000
        assert duration < 0.1  # Should be very fast with caching


@pytest.mark.asyncio
class TestAsyncOperations:
    """Test async operations if using Pulsar."""

    async def test_basic_async_operation(self):
        """Test basic async functionality."""
        # This would test Pulsar integration if enabled
        assert True  # Placeholder for async tests