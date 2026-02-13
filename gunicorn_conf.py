import multiprocessing
import os

# Binding
bind = "0.0.0.0:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Timeouts
timeout = 120
keepalive = 5

# Daemon
daemon = False

# Process Name
proc_name = "mrpfx_backend"
