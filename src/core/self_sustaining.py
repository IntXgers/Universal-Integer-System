#!/usr/bin/env python3
"""
Real Self-Sustaining Integer Service
====================================
Actually working implementation that extends your discovery system.
No fake functions - real code that works with your existing system.
"""

import json
import time
from typing import Dict,Any,Optional,List
from dataclasses import dataclass,field
from datetime import datetime
import os

# Import your ACTUAL discovery system
from src.core.discovery import StreamlinedDiscoveryTranslator,streamlined_translator


@dataclass
class UnknownCodeRecord:
    """Track unknown codes we've encountered"""
    code: int
    first_seen: float
    last_seen: float
    count: int = 1
    contexts: List [Dict [str,Any]] = field (default_factory=list)


@dataclass
class CodeProposal:
    """A proposed new code"""
    code: int
    name: str
    system: str
    concept: str
    proposed_at: float
    status: str = 'pending'  # pending, approved, rejected


class RealSelfSustainingService:
    """
    A REAL service that actually works with your discovery system.
    No magic - just practical extensions.
    """

    def __init__ (self,discovery: Optional [StreamlinedDiscoveryTranslator] = None):
        # Use the actual discovery system
        self.discovery = discovery or streamlined_translator

        # Track unknown codes we encounter
        self.unknown_codes: Dict [int,UnknownCodeRecord] = {}

        # Track code proposals  
        self.proposals: Dict [int,CodeProposal] = {}

        # Simple stats
        self.stats = {
            'translations':0,
            'unknown_encountered':0,
            'proposals_created':0
            }

        # Load any previously saved unknown codes
        self._load_unknown_codes ()

    def translate_with_learning (self,code: int,context: Optional [Dict [str,Any]] = None) -> Dict [str,Any]:
        """
        Translate a code, but track if it's unknown.
        This ACTUALLY WORKS with your real discovery system.
        """
        self.stats ['translations'] += 1

        # Use your real discovery system
        translation = self.discovery.translate_code (code)
        system = self.discovery.get_system_for_code (code)

        # Check if it's unknown
        if translation.startswith ('unknown_'):
            self.stats ['unknown_encountered'] += 1
            self._track_unknown_code (code,context)

            return {
                'code':code,
                'translation':translation,
                'system':system,
                'status':'unknown',
                'times_seen':self.unknown_codes [code].count,
                'first_seen':datetime.fromtimestamp (self.unknown_codes [code].first_seen).isoformat ()
                }

        return {
            'code':code,
            'translation':translation,
            'system':system,
            'status':'known'
            }

    def _track_unknown_code (self,code: int,context: Optional [Dict [str,Any]] = None):
        """Actually track unknown codes we encounter"""
        if code not in self.unknown_codes:
            self.unknown_codes [code] = UnknownCodeRecord (
                code=code,
                first_seen=time.time (),
                last_seen=time.time ()
                )
        else:
            self.unknown_codes [code].count += 1
            self.unknown_codes [code].last_seen = time.time ()

        if context:
            self.unknown_codes [code].contexts.append (
                {
                    'timestamp':time.time (),
                    'context':context
                    }
                )

    def propose_code_for_concept (self,concept: str,name: str,size: int = 1) -> Dict [str,Any]:
        """
        Propose a code for a new concept using the REAL discovery system.
        """
        # Use your actual suggest_code_allocation method
        suggestion = self.discovery.suggest_code_allocation (concept,size)

        if 'error' in suggestion:
            return {
                'status':'error',
                'error':suggestion ['error']
                }

        # Get the suggested code
        suggested_code = suggestion.get ('suggested_start_code')
        if not suggested_code:
            # Find next available in range
            start = suggestion ['range_start']
            end = suggestion ['range_end']

            # Use your real code registry to find gaps
            used_codes = set (
                code for code in self.discovery._code_registry.keys ()
                if start <= code <= end
                )

            for potential_code in range (start,min (start + 1000,end)):
                if potential_code not in used_codes:
                    suggested_code = potential_code
                    break

        if suggested_code:
            # Create a proposal
            proposal = CodeProposal (
                code=suggested_code,
                name=name,
                system=suggestion ['suggested_system'],
                concept=concept,
                proposed_at=time.time ()
                )

            self.proposals [suggested_code] = proposal
            self.stats ['proposals_created'] += 1

            return {
                'status':'proposed',
                'code':suggested_code,
                'name':name,
                'system':suggestion ['suggested_system'],
                'rationale':suggestion ['rationale'],
                'proposal_id':suggested_code
                }

        return {
            'status':'error',
            'error':'No available codes in suggested range'
            }

    def get_unknown_codes_report (self) -> Dict [str,Any]:
        """Get a report of all unknown codes we've seen"""
        return {
            'total_unknown':len (self.unknown_codes),
            'unknown_codes':[
                {
                    'code':record.code,
                    'count':record.count,
                    'first_seen':datetime.fromtimestamp (record.first_seen).isoformat (),
                    'last_seen':datetime.fromtimestamp (record.last_seen).isoformat (),
                    'system':self.discovery.get_system_for_code (record.code)
                    }
                for record in sorted (
                    self.unknown_codes.values (),
                    key=lambda x:x.count,
                    reverse=True
                    ) [:20]  # Top 20
                ]
            }

    def get_proposals_report (self) -> Dict [str,Any]:
        """Get all pending proposals"""
        return {
            'total_proposals':len (self.proposals),
            'pending_proposals':[
                {
                    'code':p.code,
                    'name':p.name,
                    'system':p.system,
                    'concept':p.concept,
                    'proposed_at':datetime.fromtimestamp (p.proposed_at).isoformat (),
                    'status':p.status
                    }
                for p in self.proposals.values ()
                if p.status == 'pending'
                ]
            }

    def export_proposals_for_implementation (self) -> str:
        """
        Export proposals as Python code that can be added to the integer system.
        This maintains immutability - proposals go in a new file.
        """
        pending = [p for p in self.proposals.values () if p.status == 'pending']
        if not pending:
            return "# No pending proposals"

        # Group by system
        by_system = {}
        for p in pending:
            if p.system not in by_system:
                by_system [p.system] = []
            by_system [p.system].append (p)

        code = [
            "# Proposed Integer Codes",
            f"# Generated: {datetime.now ().isoformat ()}",
            "# Add these to your integer system after review",
            "",
            "from enum import IntEnum",
            ""
            ]

        for system,proposals in by_system.items ():
            class_name = f"Proposed{system.title ().replace ('_','')}Codes"
            code.append (f"class {class_name}(IntEnum):")
            code.append (f'    """Proposed codes for {system} system"""')
            code.append ("")

            for p in sorted (proposals,key=lambda x:x.code):
                # Clean name for Python identifier
                clean_name = p.name.upper ().replace ('-','_').replace (' ','_')
                code.append (f"    {clean_name} = {p.code}  # {p.concept}")

            code.append ("")

        return '\n'.join (code)

    def _load_unknown_codes (self):
        """Load previously saved unknown codes"""
        try:
            cache_file = '../.unknown_codes_cache.json'
            if os.path.exists (cache_file):
                with open (cache_file,'r') as f:
                    data = json.load (f)
                    for code_str,record_data in data.items ():
                        code = int (code_str)
                        self.unknown_codes [code] = UnknownCodeRecord (
                            code=code,
                            first_seen=record_data ['first_seen'],
                            last_seen=record_data ['last_seen'],
                            count=record_data ['count'],
                            contexts=record_data.get ('contexts',[])
                            )
        except Exception as e:
            print (f"Could not load unknown codes cache: {e}")

    def save_unknown_codes (self):
        """Save unknown codes to disk for persistence"""
        try:
            cache_file = '../.unknown_codes_cache.json'
            data = {
                str (code):{
                    'first_seen':record.first_seen,
                    'last_seen':record.last_seen,
                    'count':record.count,
                    'contexts':record.contexts [-10:]  # Keep last 10 contexts
                    }
                for code,record in self.unknown_codes.items ()
                }

            with open (cache_file,'w') as f:
                json.dump (data,f,indent=2)
        except Exception as e:
            print (f"Could not save unknown codes cache: {e}")

    def get_statistics (self) -> Dict [str,Any]:
        """Get real statistics"""
        return {
            'service_stats':self.stats,
            'discovery_stats':self.discovery.get_statistics (),
            'unknown_codes':len (self.unknown_codes),
            'pending_proposals':len ([p for p in self.proposals.values () if p.status == 'pending'])
            }


# =============================================================================
# SIMPLE MESSAGE HANDLER THAT ACTUALLY WORKS
# =============================================================================

class SimpleMessageHandler:
    """
    A real message handler that works with any transport.
    No magic, just handles common operations.
    """

    def __init__ (self):
        self.service = RealSelfSustainingService ()

    def handle_message (self,message: Dict [str,Any]) -> Dict [str,Any]:
        """
        Handle messages. Simple, real operations only.
        """
        msg_type = message.get ('type','TRANSLATE')

        try:
            if msg_type == 'TRANSLATE':
                # Most common operation
                code = message.get ('code')
                context = message.get ('context')
                return self.service.translate_with_learning (code,context)

            elif msg_type == 'PROPOSE_CODE':
                # Propose a new code
                concept = message.get ('concept','')
                name = message.get ('name','')
                size = message.get ('size',1)
                return self.service.propose_code_for_concept (concept,name,size)

            elif msg_type == 'GET_UNKNOWN_CODES':
                # Report on unknown codes
                return self.service.get_unknown_codes_report ()

            elif msg_type == 'GET_PROPOSALS':
                # Get pending proposals
                return self.service.get_proposals_report ()

            elif msg_type == 'EXPORT_PROPOSALS':
                # Export proposals as code
                code = self.service.export_proposals_for_implementation ()
                return {
                    'status':'success',
                    'code':code
                    }

            elif msg_type == 'STATS':
                # Get statistics
                return self.service.get_statistics ()

            else:
                return {
                    'status':'error',
                    'error':f'Unknown message type: {msg_type}',
                    'valid_types':[
                        'TRANSLATE','PROPOSE_CODE','GET_UNKNOWN_CODES',
                        'GET_PROPOSALS','EXPORT_PROPOSALS','STATS'
                        ]
                    }

        except Exception as e:
            return {
                'status':'error',
                'error':str (e),
                'message_type':msg_type
                }


# =============================================================================
# EXAMPLE THAT ACTUALLY WORKS
# =============================================================================

def real_example ():
    """This actually works with your real discovery system"""

    handler = SimpleMessageHandler ()

    print ("=== REAL SELF-SUSTAINING SERVICE DEMO ===\n")

    # 1. Translate some codes
    print ("1. Translating codes:")
    for code in [11,2000,99999]:  # Known, known, unknown
        response = handler.handle_message (
            {
                'type':'TRANSLATE',
                'code':code,
                'context':{'source':'demo'}
                }
            )
        print (f"   Code {code}: {response ['translation']} (status: {response ['status']})")

    # 2. Propose a new code
    print ("\n2. Proposing new code:")
    response = handler.handle_message (
        {
            'type':'PROPOSE_CODE',
            'concept':'ai agent memory checkpoint',
            'name':'agent_memory_checkpoint',
            'size':1
            }
        )
    print (f"   {response}")

    # 3. Get unknown codes report
    print ("\n3. Unknown codes report:")
    response = handler.handle_message ({'type':'GET_UNKNOWN_CODES'})
    print (f"   Total unknown: {response ['total_unknown']}")

    # 4. Export proposals
    print ("\n4. Export proposals as code:")
    response = handler.handle_message ({'type':'EXPORT_PROPOSALS'})
    if response ['status'] == 'success':
        print (response ['code'])

    # 5. Save state
    handler.service.save_unknown_codes ()
    print ("\n✅ Unknown codes saved for next run")


# =============================================================================
# HOW TO USE WITH YOUR PULSAR SETUP
# =============================================================================

def integrate_with_pulsar (pulsar_message) -> Dict [str,Any]:
    """
    Real integration with your Pulsar consumer.
    Just decode message and pass to handler.
    """
    handler = SimpleMessageHandler ()

    # Decode Pulsar message
    message_data = json.loads (pulsar_message.data ().decode ('utf-8'))

    # Handle it
    response = handler.handle_message (message_data)

    # Add metadata
    response ['processed_at'] = time.time ()

    return response


if __name__ == "__main__":
    real_example ()