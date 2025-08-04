#!/usr/bin/env python3 src/core/discovery.py
"""
Streamlined Discovery System - Updated for Refactored Integer System
===================================================================
Updated to work with the new refactored universal integer code system.

Key Changes:
- Updated range definitions to match new architecture
- Fixed method indentation issues
- Improved system detection for new ranges
- Added support for extended ranges (10000+)
"""

import time
from enum import IntEnum
from typing import Dict,List,Any
from structlog import get_logger

# Import the refactored system (update this path as needed)
import universal_integer_system as uis


logger = get_logger (__name__)


class StreamlinedDiscoveryTranslator:
    """
    The single, comprehensive discovery system for integer codes.
    Updated to work with the refactored architecture.
    """

    def __init__ (self):
        print ("🔍 Building streamlined discovery system...")

        # Core data structures
        self._code_registry = {}
        self._translation_cache = {}
        self._system_cache = {}
        self._range_definitions = self._build_accurate_range_definitions ()

        # Essential statistics only
        self._stats = {
            'total_translations':0,
            'cache_hits':0,
            'discovery_time':0.0,
            'discovery_errors':0
            }

        # Discover all codes automatically
        self._discover_all_codes ()

        total_codes = len (self._code_registry)
        print (f"✅ Discovered {total_codes} integer codes")
        print (f"🎯 System ready - automatic translation active")

    def _discover_all_codes (self) -> None:
        """
        Core discovery engine that finds all IntEnum classes automatically.
        This is the heart of the maintenance-free system.
        """
        discovery_start = time.perf_counter ()
        errors = []

        # Scan the refactored integer system module
        for name in dir (uis):
            try:
                obj = getattr (uis,name)

                # Check if this is an IntEnum class we should register
                if (isinstance (obj,type) and
                        issubclass (obj,IntEnum) and
                        obj != IntEnum and
                        hasattr (obj,'__members__') and
                        len (obj.__members__) > 0):

                    # Register every code in this enum
                    for enum_item in obj:
                        self._code_registry [enum_item.value] = {
                            'name':enum_item.name.lower (),
                            'enum_class_name':obj.__name__,
                            'system':self._determine_system_from_code (enum_item.value)
                            }

            except (AttributeError,TypeError,ValueError) as e:
                errors.append (f"{name}: {type (e).__name__} - {str (e)}")
                continue
            except Exception as e:
                errors.append (f"{name}: Unexpected error - {str (e)}")
                continue

        self._stats ['discovery_time'] = time.perf_counter () - discovery_start
        self._stats ['discovery_errors'] = len (errors)

        if errors:
            logger.warning (f"Discovery completed with {len (errors)} errors:")
            for error in errors [:5]:  # Show first 5 errors
                logger.warning (f"  {error}")
            if len (errors) > 5:
                logger.warning (f"  ... and {len (errors) - 5} more errors")

    def _determine_system_from_code (self,code: int) -> str:
        """
        Determine which system a code belongs to based on actual range allocation.
        Updated for new architecture.
        """
        for system_name,range_info in self._range_definitions.items ():
            if range_info ["start"] <= code <= range_info ["end"]:
                return system_name
        return "unknown_range"

    @staticmethod
    def _build_accurate_range_definitions () -> Dict [str,Dict [str,Any]]:
        """
        Range definitions based on the REFACTORED structure.
        This matches the new clean architecture.
        """
        return {
            # SECTION 1: Universal Foundation (0-999)
            "universal_foundation":{
                "start":0,"end":99,
                "description":"Universal Status/Priority/Severity/Result"
                },
            "system_events":{
                "start":100,"end":199,
                "description":"Core System Events"
                },
            "user_events":{
                "start":200,"end":299,
                "description":"User Interaction Events"
                },
            "workflow_events":{
                "start":300,"end":399,
                "description":"Workflow and Process Events"
                },
            "error_events":{
                "start":400,"end":499,
                "description":"Error and Exception Events"
                },
            "communication_events":{
                "start":500,"end":599,
                "description":"Inter-service Communication"
                },
            "state_change_events":{
                "start":600,"end":699,
                "description":"Entity State Changes"
                },
            "integration_events":{
                "start":700,"end":799,
                "description":"External System Integration"
                },
            "reserved_extension":{
                "start":800,"end":899,
                "description":"Reserved for Extensions"
                },
            "system_metadata":{
                "start":900,"end":999,
                "description":"System Metadata Events"
                },

            # SECTION 2: Authentication & Authorization (1000-1999)
            "auth_system":{
                "start":1000,"end":1999,
                "description":"Authentication & Authorization"
                },

            # SECTION 3: Infrastructure & Containers (2000-3999)
            "infrastructure":{
                "start":2000,"end":3999,
                "description":"Infrastructure & Containers"
                },

            # SECTION 4: Data & Storage (4000-4999)
            "data_storage":{
                "start":4000,"end":4999,
                "description":"Data & Storage Systems"
                },

            # SECTION 5: AI & Machine Learning (5000-5999)
            "ai_ml":{
                "start":5000,"end":5999,
                "description":"AI & Machine Learning"
                },

            # SECTION 6: Business Logic (6000-6999)
            "business_logic":{
                "start":6000,"end":6999,
                "description":"Business Logic & Workflows"
                },

            # SECTION 7: Monitoring (7000-7999)
            "monitoring":{
                "start":7000,"end":7999,
                "description":"Monitoring & Observability"
                },

            # SECTION 8: Integration (8000-8999)
            "integration":{
                "start":8000,"end":8999,
                "description":"Integration & External Systems"
                },

            # SECTION 9: Application (9000-9999)
            "application":{
                "start":9000,"end":9999,
                "description":"Application-Specific"
                },

            # SECTION 10: Extended Ranges (10000+)
            "industry_specific":{
                "start":10000,"end":14999,
                "description":"Industry-Specific Codes"
                },
            "behavioral_ai":{
                "start":15000,"end":19999,
                "description":"Behavioral Prediction & Advanced AI"
                },
            "company_specific":{
                "start":20000,"end":29999,
                "description":"Company-Specific Extensions"
                },
            "future_expansion":{
                "start":30000,"end":99999,
                "description":"Future Expansion Space"
                }
            }

    def translate_code (self,code: int) -> str:
        """
        Main translation method - the core function your system calls.
        Fast cached lookup with automatic fallback for unknown codes.
        """
        self._stats ['total_translations'] += 1

        # Fast path: check cache first
        if code in self._translation_cache:
            self._stats ['cache_hits'] += 1
            return self._translation_cache [code]

        # Lookup in discovered codes
        if code in self._code_registry:
            translation = self._code_registry [code] ['name']
        else:
            # Unknown code - create intelligent fallback
            system = self._determine_system_from_code (code)
            translation = f"unknown_{system}_{code}"

        # Cache the result
        self._translation_cache [code] = translation
        return translation

    def get_system_for_code (self,code: int) -> str:
        """Get system classification with caching for performance."""
        if code in self._system_cache:
            return self._system_cache [code]

        if code in self._code_registry:
            system = self._code_registry [code] ['system']
        else:
            system = self._determine_system_from_code (code)

        self._system_cache [code] = system
        return system

    def format_code_with_context (self,code: int) -> str:
        """Format code with system context for debugging and logs."""
        name = self.translate_code (code)
        system = self.get_system_for_code (code)
        return f"{code}({name}) [{system}]"

    def get_code_info (self,code: int) -> Dict [str,Any]:
        """Get comprehensive information about a specific code."""
        if code in self._code_registry:
            info = self._code_registry [code].copy ()
            info ['code'] = code
            info ['formatted'] = self.format_code_with_context (code)
            return info

        # Return info even for unknown codes
        return {
            'code':code,
            'name':f"unknown_{self._determine_system_from_code (code)}_{code}",
            'system':self._determine_system_from_code (code),
            'enum_class_name':'Unknown',
            'formatted':self.format_code_with_context (code)
            }

    def find_codes_by_name (self,search_term: str) -> List [Dict [str,Any]]:
        """Find codes whose names contain the search term."""
        results = []
        search_term_lower = search_term.lower ()

        for code,info in self._code_registry.items ():
            if (search_term_lower in info ['name'] or
                    search_term_lower in info ['enum_class_name'].lower ()):
                results.append (self.get_code_info (code))

        return sorted (results,key=lambda x:x ['code'])

    def get_system_summary (self) -> Dict [str,Any]:
        """Get summary of all systems showing actual usage."""
        summary = {}

        for system,range_info in self._range_definitions.items ():
            start,end = range_info ["start"],range_info ["end"]
            total_capacity = end - start + 1

            # Count actually defined codes in this range
            codes_in_range = [
                code for code in self._code_registry.keys ()
                if start <= code <= end
                ]

            codes_used = len (codes_in_range)
            codes_available = total_capacity - codes_used
            utilization = (codes_used/total_capacity)*100 if total_capacity > 0 else 0

            summary [system] = {
                "range":f"{start}-{end}",
                "description":range_info ["description"],
                "total_capacity":total_capacity,
                "codes_used":codes_used,
                "codes_available":codes_available,
                "utilization":f"{utilization:.1f}%",
                "defined_codes":sorted (codes_in_range) [:10]  # Show first 10 only
                }

        return summary

    def get_statistics (self) -> Dict [str,Any]:
        """Get essential performance statistics."""
        total_translations = self._stats ['total_translations']
        cache_hits = self._stats ['cache_hits']
        cache_hit_rate = (cache_hits/total_translations*100) if total_translations > 0 else 0

        return {
            'total_codes_registered':len (self._code_registry),
            'total_translations_performed':total_translations,
            'cache_hits':cache_hits,
            'cache_hit_rate_percent':f"{cache_hit_rate:.1f}%",
            'discovery_time_ms':f"{self._stats ['discovery_time']*1000:.2f}",
            'discovery_errors':self._stats ['discovery_errors']
            }

    # =============================================================================
    # GUARD RAILS FOR CODE ADDITION
    # =============================================================================

    def suggest_code_allocation (self,concept_description: str,estimated_size: int = 10) -> Dict [str,Any]:
        """
        Suggest where to allocate codes for new concepts with guard rails.
        Updated for new architecture.
        """
        # Input validation guard rails
        if not concept_description or len (concept_description.strip ()) == 0:
            return {"error":"Concept description cannot be empty"}

        if len (concept_description) > 200:
            return {"error":"Concept description too long (max 200 characters)"}

        if estimated_size <= 0 or estimated_size > 100:
            return {"error":"Estimated size must be between 1 and 100"}

        concept_lower = concept_description.lower ()

        # Smart categorization based on concept description - updated for new ranges
        if any (word in concept_lower for word in ["auth","login","permission","role","security"]):
            suggested_system = "auth_system"
            rationale = "Authentication-related concepts belong in auth system"
        elif any (word in concept_lower for word in ["container","docker","kubernetes","infrastructure"]):
            suggested_system = "infrastructure"
            rationale = "Infrastructure concepts belong in infrastructure range"
        elif any (word in concept_lower for word in ["database","storage","cache","backup"]):
            suggested_system = "data_storage"
            rationale = "Data-related concepts belong in data storage"
        elif any (word in concept_lower for word in ["ai","ml","neural","learning","agent"]):
            suggested_system = "ai_ml"
            rationale = "AI/ML concepts belong in AI & ML range"
        elif any (word in concept_lower for word in ["business","workflow","process","rule"]):
            suggested_system = "business_logic"
            rationale = "Business concepts belong in business logic"
        elif any (word in concept_lower for word in ["monitor","health","metric","alert","log"]):
            suggested_system = "monitoring"
            rationale = "Monitoring concepts belong in monitoring range"
        elif any (word in concept_lower for word in ["api","integration","webhook","external"]):
            suggested_system = "integration"
            rationale = "Integration concepts belong in integration range"
        elif any (word in concept_lower for word in ["ui","frontend","mobile","app"]):
            suggested_system = "application"
            rationale = "Application concepts belong in application range"
        else:
            suggested_system = "company_specific"
            rationale = "Custom concepts can use company-specific extension range"

        system_info = self._range_definitions.get (suggested_system,{})

        # Check available space with guard rails
        start_range = system_info.get ("start",0)
        end_range = system_info.get ("end",0)

        # Count existing codes in this range
        existing_codes = [
            code for code in self._code_registry.keys ()
            if start_range <= code <= end_range
            ]

        available_space = (end_range - start_range + 1) - len (existing_codes)

        # Guard rail: Check if there's enough space
        if available_space < estimated_size:
            return {
                "error":f"Insufficient space in {suggested_system}",
                "available_space":available_space,
                "requested_size":estimated_size,
                "suggested_alternative":"Consider using company_specific or future_expansion range"
                }

        # Find a contiguous block of available codes
        used_codes = set (existing_codes)
        start_code = None

        for potential_start in range (start_range,end_range - estimated_size + 2):
            if all (code not in used_codes for code in range (potential_start,potential_start + estimated_size)):
                start_code = potential_start
                break

        return {
            "suggested_system":suggested_system,
            "rationale":rationale,
            "range_start":start_range,
            "range_end":end_range,
            "suggested_start_code":start_code,
            "estimated_codes_needed":estimated_size,
            "available_space":available_space,
            "system_description":system_info.get ("description","Unknown system"),
            "validation_passed":True
            }

    def validate_code_addition (self,code: int,name: str,system: str) -> Dict [str,Any]:
        """
        Validate a proposed code addition with comprehensive guard rails.
        Ensures immutability and prevents conflicts.
        """
        validation_errors = []

        # Guard rail 1: Code immutability check
        if code in self._code_registry:
            validation_errors.append (
                f"Code {code} already exists with name '{self._code_registry [code] ['name']}' - codes are immutable"
                )

        # Guard rail 2: Range validation
        if system not in self._range_definitions:
            validation_errors.append (f"System '{system}' is not a valid system")
        else:
            range_info = self._range_definitions [system]
            if not (range_info ["start"] <= code <= range_info ["end"]):
                validation_errors.append (
                    f"Code {code} is outside valid range for system '{system}' ({range_info ['start']}-{range_info ['end']})"
                    )

        # Guard rail 3: Name validation
        if not name or len (name.strip ()) == 0:
            validation_errors.append ("Name cannot be empty")

        if len (name) > 100:
            validation_errors.append ("Name too long (max 100 characters)")

        # Guard rail 4: Name uniqueness within system
        for existing_code,existing_info in self._code_registry.items ():
            if (existing_info ['name'] == name.lower () and
                    existing_info ['system'] == system):
                validation_errors.append (
                    f"Name '{name}' already exists in system '{system}' with code {existing_code}"
                    )

        # Guard rail 5: Semantic naming validation
        if not name.replace ('_','').replace ('-','').isalnum ():
            validation_errors.append ("Name contains invalid characters (only letters, numbers, _, - allowed)")

        return {
            "valid":len (validation_errors) == 0,
            "errors":validation_errors,
            "code":code,
            "name":name,
            "system":system
            }

    # =============================================================================
    # COMPATIBILITY METHODS
    # =============================================================================

    def status_name (self,status_code: int) -> str:
        """Get status name from code: 2 -> 'INITIALIZED'"""
        return self.translate_code (status_code).upper ()

    def status_code (self,name: str) -> int:
        """Get status code from name: 'INITIALIZED' -> 2"""
        name_lower = name.lower ()
        for code,info in self._code_registry.items ():
            if (info ['name'] == name_lower and
                    info ['system'] == 'universal_foundation'):
                return code
        return 0

    @staticmethod
    def is_terminal_status (status_code: int) -> bool:
        """Check if the status is terminal."""
        # Updated terminal statuses for new system
        terminal_statuses = {
            21,22,23,24,25,26,  # Completion states
            30,31,32,33,34,35,36,37,38
            }  # Error states
        return status_code in terminal_statuses

    @staticmethod
    def is_error_status (status_code: int) -> bool:
        """Check if status represents an error."""
        # Error states in new system (30-39)
        error_statuses = {30,31,32,33,34,35,36,37,38}
        return status_code in error_statuses

    @staticmethod
    def severity_name (severity_code: int) -> str:
        """Get severity name from UniversalSeverity codes (70-89)."""
        severity_mapping = {
            70:"TRACE",72:"DEBUG",74:"VERBOSE",76:"INFO",
            78:"NOTICE",80:"WARNING",82:"ERROR",84:"CRITICAL",
            86:"ALERT",88:"EMERGENCY"
            }
        return severity_mapping.get (severity_code,"UNKNOWN")

    @staticmethod
    def priority_name (priority_code: int) -> str:
        """Get priority name from UniversalPriority codes (50-69)."""
        priority_mapping = {
            50:"LOWEST",52:"LOW",54:"BELOW_NORMAL",56:"NORMAL",
            58:"ABOVE_NORMAL",60:"HIGH",62:"URGENT",64:"CRITICAL",
            66:"EMERGENCY",68:"SYSTEM"
            }
        return priority_mapping.get (priority_code,"UNKNOWN")

    @property
    def range_definitions (self):
        """returns range definitions """
        return self._range_definitions


# =============================================================================
# GLOBAL INSTANCE AND CONVENIENCE FUNCTIONS
# =============================================================================

# Create the global translator - this is your main interface
streamlined_translator = StreamlinedDiscoveryTranslator ()


# Convenience functions for backward compatibility
def translate_code (code: int) -> str:
    """Translate integer code to human-readable name."""
    return streamlined_translator.translate_code (code)


def get_system_for_code (code: int) -> str:
    """Get system classification for code."""
    return streamlined_translator.get_system_for_code (code)


def format_code_with_context (code: int) -> str:
    """Format code with system context."""
    return streamlined_translator.format_code_with_context (code)


def find_codes_by_name (search_term: str) -> List [Dict [str,Any]]:
    """Find codes by name search."""
    return streamlined_translator.find_codes_by_name (search_term)


def get_system_summary () -> Dict [str,Any]:
    """Get summary of all systems."""
    return streamlined_translator.get_system_summary ()


def get_translation_statistics () -> Dict [str,Any]:
    """Get performance statistics."""
    return streamlined_translator.get_statistics ()


def suggest_code_for_concept (concept: str,size: int = 10) -> Dict [str,Any]:
    """Suggest code allocation for autonomous learning."""
    return streamlined_translator.suggest_code_allocation (concept,size)


def validate_code_range (code: int,system: str) -> bool:
    """Validate if code belongs to specified system range."""
    range_definitions = streamlined_translator.range_definitions
    if system not in range_definitions:
        return False
    range_info = range_definitions [system]
    return range_info ["start"] <= code <= range_info ["end"]


# Add this to your discovery.py file after the existing convenience functions
# and before the "TESTING AND VERIFICATION" section

# =============================================================================
# REQUEST HANDLING INTERFACE
# =============================================================================

def handle_request(request) -> Dict[str, Any]:
    """
    Main request handler for the Universal Integer Discovery System.

    This function provides a unified interface for all discovery operations.
    It can handle various types of requests and returns structured responses.

    Args:
        request: Can be:
            - int: Direct code translation
            - str: Name search, system query, or command
            - dict: Structured request with specific operations

    Returns:
        Dict containing the response with status, data, and metadata
    """
    try:
        # Handle integer code requests
        if isinstance(request, int):
            return _handle_code_request(request)

        # Handle string requests (names, commands, searches)
        elif isinstance(request, str):
            return _handle_string_request(request)

        # Handle structured dictionary requests
        elif isinstance(request, dict):
            return _handle_structured_request(request)

        # Handle list requests (batch operations)
        elif isinstance(request, list):
            return _handle_batch_request(request)

        else:
            return {
                "status": "error",
                "error": f"Unsupported request type: {type(request).__name__}",
                "supported_types": ["int", "str", "dict", "list"]
            }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Request processing failed: {str(e)}",
            "request_type": type(request).__name__
        }


def _handle_code_request(code: int) -> Dict[str, Any]:
    """Handle direct integer code translation requests."""
    try:
        translation = translate_code(code)
        system = get_system_for_code(code)
        formatted = format_code_with_context(code)
        code_info = streamlined_translator.get_code_info(code)

        return {
            "status": "success",
            "request_type": "code_translation",
            "code": code,
            "translation": translation,
            "system": system,
            "formatted": formatted,
            "detailed_info": code_info
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Code translation failed: {str(e)}",
            "code": code
        }


def _handle_string_request(request: str) -> Dict[str, Any]:
    """Handle string-based requests (searches, commands, names)."""
    request_lower = request.lower().strip()

    # Command handling
    if request_lower.startswith("help") or request_lower == "?":
        return _get_help_response()

    elif request_lower.startswith("stats") or request_lower == "statistics":
        return {
            "status": "success",
            "request_type": "statistics",
            "data": get_translation_statistics()
        }

    elif request_lower.startswith("summary") or request_lower == "systems":
        return {
            "status": "success",
            "request_type": "system_summary",
            "data": get_system_summary()
        }

    elif request_lower.startswith("search "):
        search_term = request[7:]  # Remove "search " prefix
        results = find_codes_by_name(search_term)
        return {
            "status": "success",
            "request_type": "name_search",
            "search_term": search_term,
            "results": results,
            "count": len(results)
        }

    elif request_lower.startswith("suggest "):
        concept = request[8:]  # Remove "suggest " prefix
        suggestion = suggest_code_for_concept(concept)
        return {
            "status": "success",
            "request_type": "code_suggestion",
            "concept": concept,
            "suggestion": suggestion
        }

    elif request_lower.startswith("validate "):
        # Parse validation request: "validate 1234 test_name system_name"
        parts = request[9:].split()
        if len(parts) >= 3:
            try:
                code = int(parts[0])
                name = parts[1]
                system = parts[2]
                validation = streamlined_translator.validate_code_addition(code, name, system)
                return {
                    "status": "success",
                    "request_type": "validation",
                    "validation_result": validation
                }
            except ValueError:
                return {
                    "status": "error",
                    "error": "Invalid validation format. Use: validate <code> <name> <system>"
                }
        else:
            return {
                "status": "error",
                "error": "Validation requires: code, name, and system"
            }

    # Check if it's a numeric string (code lookup)
    elif request.isdigit():
        code = int(request)
        return _handle_code_request(code)

    # Default: treat as name search
    else:
        results = find_codes_by_name(request)
        return {
            "status": "success",
            "request_type": "name_search",
            "search_term": request,
            "results": results,
            "count": len(results)
        }


def _handle_structured_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle structured dictionary requests with specific operations."""
    operation = request.get("operation", "unknown")

    if operation == "translate":
        code = request.get("code")
        if code is not None:
            return _handle_code_request(code)
        else:
            return {"status": "error", "error": "Missing 'code' parameter"}

    elif operation == "search":
        term = request.get("term") or request.get("search_term")
        if term:
            results = find_codes_by_name(term)
            return {
                "status": "success",
                "request_type": "name_search",
                "search_term": term,
                "results": results,
                "count": len(results)
            }
        else:
            return {"status": "error", "error": "Missing 'term' parameter"}

    elif operation == "suggest":
        concept = request.get("concept")
        size = request.get("size", 10)
        if concept:
            suggestion = suggest_code_for_concept(concept, size)
            return {
                "status": "success",
                "request_type": "code_suggestion",
                "concept": concept,
                "size": size,
                "suggestion": suggestion
            }
        else:
            return {"status": "error", "error": "Missing 'concept' parameter"}

    elif operation == "validate":
        code = request.get("code")
        name = request.get("name")
        system = request.get("system")

        if all([code is not None, name, system]):
            validation = streamlined_translator.validate_code_addition(code, name, system)
            return {
                "status": "success",
                "request_type": "validation",
                "validation_result": validation
            }
        else:
            return {
                "status": "error",
                "error": "Missing required parameters: code, name, system"
            }

    elif operation == "system_info":
        system_name = request.get("system")
        if system_name:
            summary = get_system_summary()
            if system_name in summary:
                return {
                    "status": "success",
                    "request_type": "system_info",
                    "system": system_name,
                    "info": summary[system_name]
                }
            else:
                return {
                    "status": "error",
                    "error": f"System '{system_name}' not found",
                    "available_systems": list(summary.keys())
                }
        else:
            return {"status": "error", "error": "Missing 'system' parameter"}

    elif operation == "range_check":
        code = request.get("code")
        system = request.get("system")
        if code is not None and system:
            valid = validate_code_range(code, system)
            return {
                "status": "success",
                "request_type": "range_check",
                "code": code,
                "system": system,
                "valid": valid
            }
        else:
            return {"status": "error", "error": "Missing 'code' or 'system' parameter"}

    else:
        return {
            "status": "error",
            "error": f"Unknown operation: {operation}",
            "available_operations": [
                "translate", "search", "suggest", "validate",
                "system_info", "range_check"
            ]
        }


def _handle_batch_request(request: List[Any]) -> Dict[str, Any]:
    """Handle batch requests (list of operations)."""
    results = []

    for i, item in enumerate(request):
        try:
            result = handle_request(item)
            result["batch_index"] = i
            results.append(result)
        except Exception as e:
            results.append({
                "status": "error",
                "error": f"Batch item {i} failed: {str(e)}",
                "batch_index": i
            })

    return {
        "status": "success",
        "request_type": "batch",
        "total_requests": len(request),
        "results": results,
        "summary": {
            "successful": len([r for r in results if r.get("status") == "success"]),
            "failed": len([r for r in results if r.get("status") == "error"])
        }
    }


def _get_help_response() -> Dict[str, Any]:
    """Generate help response with available commands."""
    return {
        "status": "success",
        "request_type": "help",
        "help": {
            "description": "Universal Integer Discovery System - Request Handler",
            "supported_inputs": {
                "integer": "Direct code translation (e.g., 1000)",
                "string_commands": {
                    "help or ?": "Show this help",
                    "stats": "Show system statistics",
                    "summary": "Show system summary",
                    "search <term>": "Search codes by name",
                    "suggest <concept>": "Suggest code allocation",
                    "validate <code> <name> <system>": "Validate code addition"
                },
                "structured_requests": {
                    "format": {"operation": "...", "parameters": "..."},
                    "operations": [
                        "translate", "search", "suggest", "validate",
                        "system_info", "range_check"
                    ]
                },
                "batch_requests": "List of any supported request types"
            },
            "examples": {
                "code_lookup": 1000,
                "name_search": "search auth",
                "suggestion": "suggest new payment system",
                "structured": {
                    "operation": "translate",
                    "code": 1000
                },
                "batch": [1000, "search user", {"operation": "stats"}]
            }
        }
    }


# =============================================================================
# ENHANCED CONVENIENCE FUNCTIONS
# =============================================================================

def process_request(request) -> Dict[str, Any]:
    """Alias for handle_request - for backward compatibility."""
    return handle_request(request)


def query_system(query) -> Dict[str, Any]:
    """Alias for handle_request with query-focused naming."""
    return handle_request(query)


def discover_by_request(request) -> Dict[str, Any]:
    """Alias for handle_request with discovery-focused naming."""
    return handle_request(request)


# =============================================================================
# INTERACTIVE REQUEST PROCESSOR
# =============================================================================

def interactive_session():
    """
    Start an interactive session for testing the request handler.
    Useful for development and debugging.
    """
    print("🚀 Universal Integer Discovery System - Interactive Session")
    print("Type 'help' for commands, 'quit' to exit")
    print("-" * 60)

    while True:
        try:
            user_input = input("\n> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not user_input:
                continue

            # Process the request
            response = handle_request(user_input)

            # Pretty print the response
            if response.get("status") == "success":
                print("✅ Success:")
                _pretty_print_response(response)
            else:
                print("❌ Error:")
                print(f"   {response.get('error', 'Unknown error')}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Session error: {e}")


def _pretty_print_response(response: Dict[str, Any]):
    """Pretty print response data for interactive session."""
    request_type = response.get("request_type", "unknown")

    if request_type == "code_translation":
        print(f"   Code: {response['code']}")
        print(f"   Translation: {response['translation']}")
        print(f"   System: {response['system']}")
        print(f"   Formatted: {response['formatted']}")

    elif request_type == "name_search":
        print(f"   Search: '{response['search_term']}'")
        print(f"   Found: {response['count']} results")
        for result in response['results'][:5]:  # Show first 5
            print(f"     → {result['code']}: {result['name']} [{result['system']}]")
        if response['count'] > 5:
            print(f"     ... and {response['count'] - 5} more")

    elif request_type == "code_suggestion":
        suggestion = response['suggestion']
        if 'error' not in suggestion:
            print(f"   Concept: {response['concept']}")
            print(f"   Suggested System: {suggestion['suggested_system']}")
            print(f"   Start Code: {suggestion['suggested_start_code']}")
            print(f"   Available Space: {suggestion['available_space']}")
        else:
            print(f"   Error: {suggestion['error']}")

    elif request_type == "statistics":
        stats = response['data']
        print(f"   Total Codes: {stats['total_codes_registered']}")
        print(f"   Discovery Time: {stats['discovery_time_ms']}")
        print(f"   Cache Hit Rate: {stats['cache_hit_rate_percent']}")

    else:
        # Generic pretty print for other types
        data = response.get('data', response)
        if isinstance(data, dict) and len(data) < 10:
            for key, value in data.items():
                if key not in ['status', 'request_type']:
                    print(f"   {key}: {value}")


# =============================================================================
# REQUEST HANDLER TEST FUNCTION
# =============================================================================

def test_handle_request():
    """Test the handle_request function with various input types."""
    print("🧪 Testing handle_request function...")
    print("=" * 50)

    # Test cases
    test_cases = [
        # Integer requests
        1000,
        2000,
        99999,  # Non-existent code

        # String requests
        "help",
        "stats",
        "search auth",
        "suggest new AI agent system",
        "1000",  # Numeric string
        "user",  # Name search

        # Structured requests
        {"operation": "translate", "code": 1000},
        {"operation": "search", "term": "system"},
        {"operation": "suggest", "concept": "blockchain integration", "size": 15},
        {"operation": "validate", "code": 50000, "name": "test_code", "system": "future_expansion"},
        {"operation": "system_info", "system": "auth_system"},
        {"operation": "range_check", "code": 1500, "system": "auth_system"},

        # Batch request
        [1000, "search user", {"operation": "stats"}],

        # Error cases
        None,
        {"operation": "unknown"},
        {"operation": "translate"},  # Missing code
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i:2d}. Testing: {test_case}")
        try:
            response = handle_request(test_case)
            status = response.get("status", "unknown")
            if status == "success":
                print(f"    ✅ {status} - {response.get('request_type', 'N/A')}")
            else:
                print(f"    ❌ {status} - {response.get('error', 'N/A')}")
        except Exception as e:
            print(f"    💥 Exception: {e}")

    print("\n✅ handle_request testing complete!")


if __name__ == "__main__":
    # If running this file directly, run tests and start interactive session
 # Existing test
    print("\n" + "=" * 60 + "\n")
    test_handle_request()  # New handle_request test

    # Optionally start interactive session
    print("\nWould you like to start an interactive session? (y/n): ", end="")
    if input().lower().startswith('y'):
        interactive_session()
# =============================================================================
# TESTING AND VERIFICATION
# =============================================================================

def run_essential_test ():
    """
    Essential test to verify the streamlined system works correctly.
    Tests core functionality and new guard rails.
    """
    print ("=== STREAMLINED DISCOVERY SYSTEM TEST ===\n")

    # Test 1: Core translation
    print ("🧪 Core Translation Test:")
    test_codes = [0,11,100,200,1000,2000,4000,5000,7000,8000,9000]
    for code in test_codes:
        translation = translate_code (code)
        formatted = format_code_with_context (code)
        system = get_system_for_code (code)
        print (f"   {formatted}")
    print ()

    # Test 2: Guard rails validation
    print ("🛡️ Guard Rails Test:")
    validation = streamlined_translator.validate_code_addition (11,"test_duplicate","universal_foundation")
    print (f"   Duplicate code validation: {validation ['valid']} (should be False)")
    if not validation ['valid']:
        print (f"   Error: {validation ['errors'] [0]}")

    validation = streamlined_translator.validate_code_addition (99999,"test_out_of_range","universal_foundation")
    print (f"   Out of range validation: {validation ['valid']} (should be False)")
    print ()

    # Test 3: Code suggestion
    print ("🤖 Code Suggestion Test:")
    test_concepts = [
        "new authentication method for mobile apps",
        "container health monitoring system",
        "AI agent memory management",
        "custom business workflow engine"
        ]

    for concept in test_concepts:
        suggestion = suggest_code_for_concept (concept,5)
        if 'error' not in suggestion:
            print (f"   '{concept [:30]}...':")
            print (f"     → System: {suggestion.get ('suggested_system')}")
            print (f"     → Start at: {suggestion.get ('suggested_start_code')}")
            print (f"     → Available: {suggestion.get ('available_space')} codes")
    print ()

    # Test 4: System summary
    print ("📊 System Summary (Top Systems):")
    summary = get_system_summary ()

    # Sort by utilization
    sorted_systems = sorted (
        [(k,v) for k,v in summary.items () if v ['codes_used'] > 0],
        key=lambda x:x [1] ['codes_used'],
        reverse=True
        ) [:5]

    for system,info in sorted_systems:
        print (f"   {system}: {info ['codes_used']} codes used ({info ['utilization']})")
    print ()

    # Test 5: Performance statistics
    print ("⚡ Performance:")
    stats = get_translation_statistics ()
    print (f"   Discovered: {stats ['total_codes_registered']} codes")
    print (f"   Discovery time: {stats ['discovery_time_ms']}ms")
    print (f"   Cache hit rate: {stats ['cache_hit_rate_percent']}")
    print ()

    print ("✅ UPDATED DISCOVERY SYSTEM READY!")


if __name__ == "__main__":
    run_essential_test ()