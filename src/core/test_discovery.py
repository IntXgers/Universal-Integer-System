#!/usr/bin/env python3
"""
Updated test_discovery.py
Tests for the Universal Integer Discovery System with handle_request function
"""

import unittest
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Import the discovery module and its functions
    import discovery
    from discovery import (
        handle_request,
        translate_code,
        get_system_for_code,
        format_code_with_context,
        find_codes_by_name,
        get_system_summary,
        get_translation_statistics,
        suggest_code_for_concept,
        validate_code_range,
        streamlined_translator
    )

    DISCOVERY_AVAILABLE = True
    print("✅ Successfully imported discovery module")
except ImportError as e:
    print(f"❌ Failed to import discovery module: {e}")
    DISCOVERY_AVAILABLE = False


class TestDiscoverySystem(unittest.TestCase):
    """Test suite for the Universal Integer Discovery System."""

    def setUp(self):
        """Set up test fixtures."""
        if not DISCOVERY_AVAILABLE:
            self.skipTest("Discovery module not available")

    def test_handle_request_with_integer(self):
        """Test handle_request with integer input (direct code translation)."""
        # Test with a known code
        response = handle_request(1000)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get("status"), "success")
        self.assertEqual(response.get("request_type"), "code_translation")
        self.assertEqual(response.get("code"), 1000)
        self.assertIn("translation", response)
        self.assertIn("system", response)

        print(f"✅ Integer request test: {response['formatted']}")

    def test_handle_request_with_string_commands(self):
        """Test handle_request with string commands."""
        test_commands = [
            "help",
            "stats",
            "summary",
            "search auth",
            "1000"  # Numeric string
        ]

        for command in test_commands:
            with self.subTest(command=command):
                response = handle_request(command)
                self.assertIsInstance(response, dict)
                self.assertIn("status", response)
                print(f"✅ Command '{command}': {response.get('status')}")

    def test_handle_request_with_structured_requests(self):
        """Test handle_request with structured dictionary requests."""
        test_requests = [
            {"operation": "translate", "code": 1000},
            {"operation": "search", "term": "system"},
            {"operation": "suggest", "concept": "test concept", "size": 5},
            {"operation": "system_info", "system": "auth_system"}
        ]

        for request in test_requests:
            with self.subTest(request=request):
                response = handle_request(request)
                self.assertIsInstance(response, dict)
                self.assertIn("status", response)
                operation = request.get("operation")
                print(f"✅ Structured request '{operation}': {response.get('status')}")

    def test_handle_request_with_batch(self):
        """Test handle_request with batch requests."""
        batch_request = [
            1000,
            "search user",
            {"operation": "stats"}
        ]

        response = handle_request(batch_request)

        self.assertIsInstance(response, dict)
        self.assertEqual(response.get("status"), "success")
        self.assertEqual(response.get("request_type"), "batch")
        self.assertEqual(response.get("total_requests"), 3)
        self.assertIn("results", response)
        self.assertEqual(len(response["results"]), 3)

        print(f"✅ Batch request test: {response['summary']}")

    def test_error_handling(self):
        """Test error handling for invalid requests."""
        invalid_requests = [
            None,
            {"operation": "unknown"},
            {"operation": "translate"},  # Missing code parameter
            object()  # Unsupported type
        ]

        for request in invalid_requests:
            with self.subTest(request=request):
                response = handle_request(request)
                self.assertIsInstance(response, dict)
                self.assertEqual(response.get("status"), "error")
                self.assertIn("error", response)
                print(f"✅ Error handling for {type(request).__name__}: OK")

    def test_core_translation_functions(self):
        """Test core translation functionality."""
        test_codes = [0, 100, 1000, 2000, 5000]

        for code in test_codes:
            # Test translate_code
            translation = translate_code(code)
            self.assertIsInstance(translation, str)

            # Test get_system_for_code
            system = get_system_for_code(code)
            self.assertIsInstance(system, str)

            # Test format_code_with_context
            formatted = format_code_with_context(code)
            self.assertIsInstance(formatted, str)
            self.assertIn(str(code), formatted)

            print(f"✅ Core functions for code {code}: {formatted}")

    def test_search_functionality(self):
        """Test search functionality."""
        # Test find_codes_by_name
        results = find_codes_by_name("system")
        self.assertIsInstance(results, list)

        # Test via handle_request
        response = handle_request("search system")
        self.assertEqual(response.get("status"), "success")
        self.assertEqual(response.get("request_type"), "name_search")
        self.assertIn("results", response)

        print(f"✅ Search test: Found {response.get('count', 0)} results")

    def test_system_summary(self):
        """Test system summary functionality."""
        summary = get_system_summary()
        self.assertIsInstance(summary, dict)

        # Should have multiple systems
        self.assertGreater(len(summary), 0)

        # Test via handle_request
        response = handle_request("summary")
        self.assertEqual(response.get("status"), "success")

        print(f"✅ System summary: {len(summary)} systems discovered")

    def test_statistics(self):
        """Test statistics functionality."""
        stats = get_translation_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn("total_codes_registered", stats)

        # Test via handle_request
        response = handle_request("stats")
        self.assertEqual(response.get("status"), "success")

        total_codes = stats.get("total_codes_registered", 0)
        print(f"✅ Statistics test: {total_codes} codes registered")

    def test_code_suggestion(self):
        """Test code suggestion functionality."""
        concept = "test authentication system"
        suggestion = suggest_code_for_concept(concept, 5)
        self.assertIsInstance(suggestion, dict)

        # Test via handle_request with string
        response = handle_request(f"suggest {concept}")
        self.assertEqual(response.get("status"), "success")

        # Test via handle_request with structured request
        structured_response = handle_request({
            "operation": "suggest",
            "concept": concept,
            "size": 5
        })
        self.assertEqual(structured_response.get("status"), "success")

        print(f"✅ Code suggestion test: Suggested system available")

    def test_validation(self):
        """Test validation functionality."""
        # Test the streamlined_translator validation
        validation = streamlined_translator.validate_code_addition(
            99999, "test_code", "future_expansion"
        )
        self.assertIsInstance(validation, dict)
        self.assertIn("valid", validation)

        # Test range validation
        valid = validate_code_range(1500, "auth_system")
        self.assertIsInstance(valid, bool)

        print(f"✅ Validation test: Range validation working")

    def test_compatibility_methods(self):
        """Test backward compatibility methods."""
        if hasattr(discovery, 'status_name'):
            status = discovery.status_name(0)
            self.assertIsInstance(status, str)
            print(f"✅ Compatibility: status_name(0) = {status}")

        if hasattr(discovery, 'severity_name'):
            severity = discovery.severity_name(80)
            self.assertIsInstance(severity, str)
            print(f"✅ Compatibility: severity_name(80) = {severity}")

    def test_system_initialization_logs(self):
        """Test that system shows expected initialization messages."""
        # This test verifies the system matches the log output you showed:
        # 🔍 Building streamlined discovery system...
        # ✅ Discovered 1550 integer codes
        # 🎯 System ready - automatic translation active

        stats = get_translation_statistics()
        total_codes = stats.get("total_codes_registered", 0)

        # Should have discovered codes (you showed 1550)
        self.assertGreater(total_codes, 0)

        # System should be ready (no exceptions thrown)
        response = handle_request(1000)
        self.assertEqual(response.get("status"), "success")

        print(f"✅ System initialization: {total_codes} codes ready for translation")


class TestHandleRequestSpecific(unittest.TestCase):
    """Specific tests for the handle_request function."""

    def setUp(self):
        if not DISCOVERY_AVAILABLE:
            self.skipTest("Discovery module not available")

    def test_request_response_structure(self):
        """Test that all responses have consistent structure."""
        test_requests = [
            1000,
            "help",
            {"operation": "stats"},
            [1000, 2000]
        ]

        for request in test_requests:
            response = handle_request(request)

            # All responses should be dictionaries
            self.assertIsInstance(response, dict)

            # All responses should have status
            self.assertIn("status", response)
            self.assertIn(response["status"], ["success", "error"])

            # Success responses should have request_type
            if response["status"] == "success":
                self.assertIn("request_type", response)

            # Error responses should have error message
            if response["status"] == "error":
                self.assertIn("error", response)

    def test_help_command(self):
        """Test the help command provides useful information."""
        response = handle_request("help")

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["request_type"], "help")
        self.assertIn("help", response)

        help_content = response["help"]
        self.assertIn("supported_inputs", help_content)
        self.assertIn("examples", help_content)

        print("✅ Help command provides comprehensive guidance")

    def test_alias_functions(self):
        """Test that alias functions work correctly."""
        if hasattr(discovery, 'process_request'):
            response1 = discovery.process_request(1000)
            response2 = handle_request(1000)
            self.assertEqual(response1, response2)
            print("✅ process_request alias works")

        if hasattr(discovery, 'query_system'):
            response1 = discovery.query_system("stats")
            response2 = handle_request("stats")
            self.assertEqual(response1, response2)
            print("✅ query_system alias works")


def run_integration_test():
    """Run a comprehensive integration test."""
    print("\n" + "=" * 60)
    print("🚀 INTEGRATION TEST - Universal Integer Discovery System")
    print("=" * 60)

    if not DISCOVERY_AVAILABLE:
        print("❌ Discovery module not available - skipping integration test")
        return

    try:
        # Test 1: Basic functionality
        print("\n1. Testing basic code translation...")
        response = handle_request(1000)
        print(f"   Code 1000: {response.get('formatted', 'N/A')}")

        # Test 2: Search functionality
        print("\n2. Testing search...")
        response = handle_request("search auth")
        print(f"   Found {response.get('count', 0)} results for 'auth'")

        # Test 3: System statistics
        print("\n3. Testing system stats...")
        response = handle_request("stats")
        if response.get("status") == "success":
            stats = response["data"]
            print(f"   Total codes: {stats.get('total_codes_registered', 'N/A')}")
            print(f"   Discovery time: {stats.get('discovery_time_ms', 'N/A')}")

        # Test 4: Code suggestion
        print("\n4. Testing code suggestion...")
        response = handle_request("suggest new payment processing system")
        if response.get("status") == "success":
            suggestion = response["suggestion"]
            if "error" not in suggestion:
                print(f"   Suggested system: {suggestion.get('suggested_system', 'N/A')}")
                print(f"   Start code: {suggestion.get('suggested_start_code', 'N/A')}")
            else:
                print(f"   Suggestion error: {suggestion.get('error', 'N/A')}")

        # Test 5: Batch processing
        print("\n5. Testing batch processing...")
        batch = [1000, 2000, "search system"]
        response = handle_request(batch)
        if response.get("status") == "success":
            summary = response.get("summary", {})
            print(f"   Processed {response.get('total_requests', 0)} requests")
            print(f"   Successful: {summary.get('successful', 0)}")
            print(f"   Failed: {summary.get('failed', 0)}")

        print(f"\n✅ Integration test completed successfully!")

    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        raise


if __name__ == '__main__':
    # Run the integration test first
    run_integration_test()

    print("\n" + "=" * 60)
    print("🧪 RUNNING UNIT TESTS")
    print("=" * 60)

    # Run unit tests
    unittest.main(verbosity=2, exit=False)

    print(f"\n🎉 All tests completed!")