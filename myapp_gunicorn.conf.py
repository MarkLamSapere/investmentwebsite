bind = "192.168.1.167:8000"  # Specify the host and port where Gunicorn should listen
workers = 4  # The number of worker processes
timeout = 60
loglevel = "info"
accesslog = "-"  # Log to stdout
errorlog = "/home/marklam/my_web_project/log/gunicorn_error.log"