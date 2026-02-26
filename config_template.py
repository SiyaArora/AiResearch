"""
Configuration Template for Tuition Remission Email Generator

INSTRUCTIONS:
1. Copy this file to config.py: cp config_template.py config.py
2. Update the values below with your actual credentials
3. Add config.py to .gitignore to prevent committing credentials
4. Import config in your script: from config import DATABASE_CONFIG
"""

# Database Configuration
DATABASE_CONFIG = {
    'username': 'your_oracle_username',
    'password': 'your_oracle_password',
    'host': 'your_database_host',          # e.g., 'oracledb.usfca.edu'
    'port': '1521',                        # Default Oracle port
    'service_name': 'your_service_name',   # e.g., 'PROD'
}

# Table Configuration
TABLE_NAME = 'contact_tuition'  # Update if your table has a different name

# Output Configuration
OUTPUT_DIRECTORY = 'tuition_emails_output'

# Email Configuration (optional - for future email sending functionality)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.usfca.edu',
    'smtp_port': 587,
    'use_tls': True,
    'sender_email': 'noreply@usfca.edu',
    'sender_name': 'USF Human Resources',
    'reply_to': 'tuitionremission@usfca.edu',
}

# Branding Configuration
BRAND_COLORS = {
    'primary': '#00543C',    # USF Green
    'accent': '#FDBB30',     # USF Gold
}

# Contact Information
CONTACT_INFO = {
    'department': 'Human Resources - Benefits Office',
    'address': '2130 Fulton Street, San Francisco, CA 94117',
    'phone': '(415) 422-6457',
    'email': 'tuitionremission@usfca.edu',
}
