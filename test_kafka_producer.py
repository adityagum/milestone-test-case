#!/usr/bin/env python3
"""
Test script to verify kafka producer serialization works correctly
"""
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.events.ticket_events import TicketReserveRequested
    
    # Test creating the event
    print("Testing TicketReserveRequested creation...")
    event = TicketReserveRequested.new(
        order_id="test-order-123",
        event_id_ref="event-456",
        user_id="user-789",
        quantity=2
    )
    print(f"[OK] Event created successfully: {event.event_id}")
    
    # Test serialization (what the kafka producer does)
    print("\nTesting serialization...")
    serialized_data = json.dumps(event.model_dump(mode="json")).encode("utf-8")
    print(f"[OK] Serialization successful, size: {len(serialized_data)} bytes")
    
    # Test deserialization to verify data integrity
    print("\nTesting deserialization...")
    deserialized_data = json.loads(serialized_data.decode("utf-8"))
    print(f"[OK] Deserialization successful")
    print(f"  Order ID: {deserialized_data['order_id']}")
    print(f"  Event ID: {deserialized_data['event_id']}")
    print(f"  Occurred At: {deserialized_data['occurred_at']}")
    print(f"  Full data: {deserialized_data}")
    
    print("\n[SUCCESS] All tests passed! Kafka producer should work correctly.")
    
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("Make sure all dependencies are installed and paths are correct")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    sys.exit(1)