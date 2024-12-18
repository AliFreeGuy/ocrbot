# your_project/logger.py

import logging
import logging.config
from logging.handlers import RotatingFileHandler

# تنظیمات لاگر
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',  # تغییر به RotatingFileHandler
            'filename': 'django_debug.log',
            'formatter': 'verbose',
            'maxBytes': 10 * 1024 * 1024,  # حداکثر حجم 10 مگابایت
            'backupCount': 5,  # تعداد فایل‌های پشتیبان (نسخه‌های قبلی)
        },
    },
    'loggers': {
        'my_logger': {  # نام لاگر شما
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# پیکربندی logging
logging.config.dictConfig(LOGGING)

# ایجاد یک logger
logger = logging.getLogger('my_logger')
