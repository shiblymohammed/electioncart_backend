"""
Gunicorn configuration file for production deployment
"""

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes
# Limit workers to maximum of 2 for memory optimization (Requirement 1.1, 1.2)
workers = min(int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1)), 2)
worker_class = 'sync'
# Reduce worker connections from 1000 to 500 for memory optimization (Requirement 1.5)
worker_connections = 500
# Set worker recycling to 500 requests to prevent memory leaks (Requirement 1.3)
max_requests = 500
max_requests_jitter = 25
# Reduce timeout from 30 to 20 seconds (Requirement 1.4)
timeout = 20
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'election_cart'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = None
# certfile = None
