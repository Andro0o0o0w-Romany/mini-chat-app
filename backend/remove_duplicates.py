#!/usr/bin/env python
"""
Script to remove duplicate 1-on-1 conversations.
Keeps the oldest conversation and deletes newer duplicates.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
django.setup()

from chat.models import Conversation, Participant
from django.db.models import Count


def find_and_remove_duplicates():
    """Find and remove duplicate 1-on-1 conversations."""
    print("🔍 Scanning for duplicate conversations...")
    print("-" * 60)
    
    # Get all non-group conversations
    conversations = Conversation.objects.filter(is_group=False).annotate(
        participant_count=Count('participants')
    ).filter(participant_count=2)
    
    # Group conversations by participant pairs
    conversation_pairs = {}
    
    for conv in conversations:
        # Get the two participants
        participants = list(conv.participants.all().values_list('user_id', flat=True))
        if len(participants) != 2:
            continue
        
        # Create a sorted tuple to represent the pair (order doesn't matter)
        pair_key = tuple(sorted(participants))
        
        if pair_key not in conversation_pairs:
            conversation_pairs[pair_key] = []
        conversation_pairs[pair_key].append(conv)
    
    # Find duplicates
    total_duplicates = 0
    total_kept = 0
    
    for pair_key, convs in conversation_pairs.items():
        if len(convs) > 1:
            # We have duplicates!
            user1_id, user2_id = pair_key
            
            # Sort by creation date (oldest first)
            convs_sorted = sorted(convs, key=lambda c: c.created_at)
            keep_conv = convs_sorted[0]
            duplicate_convs = convs_sorted[1:]
            
            print(f"\n📊 Found {len(duplicate_convs)} duplicate(s) for user pair ({user1_id}, {user2_id})")
            print(f"   ✅ Keeping conversation ID: {keep_conv.id} (created: {keep_conv.created_at})")
            
            for dup in duplicate_convs:
                message_count = dup.messages.count()
                print(f"   ❌ Deleting conversation ID: {dup.id} (created: {dup.created_at}, {message_count} messages)")
                dup.delete()
                total_duplicates += 1
            
            total_kept += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Cleanup complete!")
    print(f"   - Unique conversations kept: {total_kept}")
    print(f"   - Duplicate conversations removed: {total_duplicates}")
    print(f"   - Total conversations remaining: {Conversation.objects.filter(is_group=False).count()}")
    print("=" * 60)
    
    if total_duplicates == 0:
        print("\n✨ No duplicates found! Your database is clean.")
    else:
        print(f"\n🎉 Successfully removed {total_duplicates} duplicate conversation(s)!")


if __name__ == '__main__':
    try:
        find_and_remove_duplicates()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

