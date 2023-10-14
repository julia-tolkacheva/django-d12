import logging


def info_level_filter(record):
    return True if record.levelno <= logging.INFO else False

def warn_level_filter(record):
    return True if record.levelno == logging.WARNING else False

def err_level_filter(record):
    return True if record.levelno >= logging.ERROR else False


django_logging_settings = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',  
        },
        'warn': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
        'err': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{',
        },
        'general': {
            'format': '{asctime} {levelname} module:*{module}* -> {message}',
            'style': '{',
        },
        'security': {
            'format': '{asctime} {levelname} module:*{module}* -> {message}',
            'style': '{',
        },       
        'mail': {
            'format': '{asctime} {levelname}  -> {message} / {pathname}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'info_level': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': info_level_filter,
        },
        'warn_level': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': warn_level_filter,
        },
        'err_level': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': err_level_filter,
        },
    },
    'handlers': {
        'console_info': {
            'level': 'DEBUG',
            'filters': ['require_debug_true','info_level'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_err': {
            'level': 'ERROR',
            'filters': ['require_debug_true','err_level'],
            'class': 'logging.StreamHandler',
            'formatter': 'err',
        },
        'console_warn': {
            'level': 'WARNING',
            'filters': ['require_debug_true','warn_level'],
            'class': 'logging.StreamHandler',
            'formatter': 'warn',
        },
        'file_general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'formatter': 'general',
            'filters': ['require_debug_false'],
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'err',
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'security',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_info','console_warn','console_err','file_general'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors','mail_admins'],
            'level': 'DEBUG',
        },
        'django.server': {
            'handlers': ['file_errors','mail_admins'],
            'level': 'DEBUG',
        },
        'django.template': {
            'handlers': ['file_errors'],
            'level': 'DEBUG',
        },
        'django.db_backends': {
            'handlers': ['file_errors'],
            'level': 'DEBUG',
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'INFO',
        },                 
    }
}