import logging
import os
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
# bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
bind = f"0.0.0.0:{os.getenv('PORT')}"
# loglevel = "debug"
loglevel = str(os.getenv("GURICORN_LOG_LEVEL"))
accesslog = "-"  # Логи запросов в консоль
errorlog = "-"  # Логи ошибок в консоль
timeout = 60

print(f"GURICORN_LOG_LEVEL: {str(os.getenv("GURICORN_LOG_LEVEL"))}")
