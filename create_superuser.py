#!/usr/bin/env python
"""
Create superuser automatically during deployment.
This script is safe to run multiple times - it won't create duplicates.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Superuser credentials
USERNAME = 'aseeb'
PASSWORD = 'Dr.aseeb123'
EMAIL = 'aseeb@electioncart.com'

def create_superuser():
    """Create superuser if it doesn't exist."""
    try:
        if User.objects.filter(username=USERNAME).exists():
            print(f'✓ Superuser "{USERNAME}" already exists. Skipping creation.')
            return
        
        user = User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
        print(f'✓ Superuser "{USERNAME}" created successfully!')
        print(f'  Username: {USERNAME}')
        print(f'  Email: {EMAIL}')
        
    except Exception as e:
        print(f'✗ Error creating superuser: {e}')
        raise

if __name__ == '__main__':
    create_superuser()
