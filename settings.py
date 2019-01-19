SITE_URL = 'https://www.amazon.com/'

USERNAME = 'username'
PASSWORD = 'password'

PROXY = '127.0.0.1:1080'
PROXY_ORIGIN = '127.0.0.1'

LOGIN_USERS = [
    {
        'username': 'username',
        'password': 'password',
        'proxy': 'proxy',
        'proxy_origin': 'proxy_origin'
    },
]

PRODUCTS = 'product_link'
DYNAMIC_PRODUCTS = 'dynamic_product_link'

WHITE_LIST = ['name', ]


try:
    from local_settings import *
except ImportError:
    pass
