VK_TOKEN = None

MONGO_CONFIG = {
    'HOST': 'mongodb',
}

try:
    from local_settings import *
except ImportError:
    pass
