import logging
import logging.config

logging.basicConfig(
    filename="log.txt",
    # filemode='w',
    encoding='utf-8',
)

logging.config.dictConfig({
    'version': 1,
    'formatters': { 
        'standard': {
            'format': '[%(asctime)s,%(msecs)03d][%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d-%H:%M:%S' },
    },
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'apscheduler': {
            'level': 'WARNING',  # 把 apscheduler 壓低
            'handlers': [],
            'propagate': False,
        },
    },
})

# https://stackoverflow.com/questions/8269294/python-logging-only-log-from-script