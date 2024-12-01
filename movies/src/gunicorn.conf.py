import logging
import os
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
loglevel = "debug"
accesslog = "-"  # Логи запросов в консоль
errorlog = "-"  # Логи ошибок в консоль
timeout = 60
