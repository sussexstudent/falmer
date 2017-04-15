import os

if os.environ.get('FALMER_ENV') == 'production':
    print('Settings: production')
    from .production import *
else:
    print('Settings: development')
    from .development import *
