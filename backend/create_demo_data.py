#!/usr/bin/env python
"""
Script to create demo data for testing the chat application
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
django.setup()

from accounts.models import User
from chat.models import Conversation, Participant, Message

def create_demo_data():
    print("Creating demo data...")
    
    # Create demo users
    users_data = [
        {
            'username': 'demo',
            'email': 'demo@example.com',
            'password': 'demo123',
            'first_name': 'Demo',
            'last_name': 'User'
        },
        {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'alice123',
            'first_name': 'Alice',
            'last_name': 'Smith'
        },
        {
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'bob123',
            'first_name': 'Bob',
            'last_name': 'Jones'
        },
        {
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'charlie123',
            'first_name': 'Charlie',
            'last_name': 'Brown'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        username = user_data['username']
        if User.objects.filter(username=username).exists():
            print(f"User '{username}' already exists, skipping...")
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(**user_data)
            print(f"✓ Created user: {username}")
        created_users.append(user)
    
    # Create demo conversations
    if len(created_users) >= 2:
        demo, alice, bob = created_users[0], created_users[1], created_users[2]
        
        # Conversation 1: Demo and Alice
        conv1 = Conversation.objects.create(
            created_by=demo,
            is_group=False
        )
        Participant.objects.create(conversation=conv1, user=demo)
        Participant.objects.create(conversation=conv1, user=alice)
        
        Message.objects.create(
            conversation=conv1,
            sender=demo,
            content="Hey Alice! How are you doing?"
        )
        Message.objects.create(
            conversation=conv1,
            sender=alice,
            content="Hi Demo! I'm doing great, thanks for asking!"
        )
        Message.objects.create(
            conversation=conv1,
            sender=demo,
            content="That's wonderful to hear! 😊"
        )
        
        print("✓ Created conversation between Demo and Alice")
        
        # Conversation 2: Demo and Bob
        conv2 = Conversation.objects.create(
            created_by=demo,
            is_group=False
        )
        Participant.objects.create(conversation=conv2, user=demo)
        Participant.objects.create(conversation=conv2, user=bob)
        
        Message.objects.create(
            conversation=conv2,
            sender=bob,
            content="Hey Demo! Want to grab lunch?"
        )
        Message.objects.create(
            conversation=conv2,
            sender=demo,
            content="Sure! What time works for you?"
        )
        
        print("✓ Created conversation between Demo and Bob")
        
        # Conversation 3: Group chat (if we have enough users)
        if len(created_users) >= 4:
            charlie = created_users[3]
            conv3 = Conversation.objects.create(
                name="Project Team",
                created_by=demo,
                is_group=True
            )
            Participant.objects.create(conversation=conv3, user=demo)
            Participant.objects.create(conversation=conv3, user=alice)
            Participant.objects.create(conversation=conv3, user=bob)
            Participant.objects.create(conversation=conv3, user=charlie)
            
            Message.objects.create(
                conversation=conv3,
                sender=demo,
                content="Welcome to the team chat, everyone!"
            )
            Message.objects.create(
                conversation=conv3,
                sender=alice,
                content="Thanks for creating this group!"
            )
            Message.objects.create(
                conversation=conv3,
                sender=bob,
                content="Great! Let's coordinate here."
            )
            
            print("✓ Created group conversation: Project Team")
    
    print("\n✅ Demo data created successfully!")
    print("\nYou can now login with:")
    print("  Username: demo")
    print("  Password: demo123")
    print("\nOr try other users: alice, bob, charlie (password: username + 123)")

if __name__ == '__main__':
    create_demo_data()

