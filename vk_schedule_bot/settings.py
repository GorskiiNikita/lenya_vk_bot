VK_TOKEN = None
VK_GROUP_ID = None
PATH_TO_LOG_FILE = None
VK_ADMIN_ID = None

MONGO_CONFIG = {
    'HOST': 'mongodb',
}


try:
    from local_settings import *
except ImportError:
    pass
