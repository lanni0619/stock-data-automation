import logging
import logging.config

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
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'level': 'DEBUG',
            'filename': 'log.txt',  # Specify the filename here
            'mode': 'a',  # Specify the file mode here
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'apscheduler': {
            'level': 'WARNING',  # lower apscheduler level
            'handlers': [],
            'propagate': False,
        },
        'matplotlib':{
            'level': 'WARNING',
            'handlers': [],
            'propagate': False,   
        }
    },
})

# https://stackoverflow.com/questions/8269294/python-logging-only-log-from-script