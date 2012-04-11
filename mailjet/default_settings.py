'''These are the default settings, DON'T MODIFY THIS FILE!

If (some) of these settings need changing, do that in `settings.py` instead


The global settings prefix can be changed by modifying the `SETTINGS_PREFIX`
variable. These settings can be overwritten by modifying the Django settings
(in that case the `SETTINGS_PREFIX` is used) or by modifying `settings.py`
'''

SETTINGS_PREFIX = 'MAILJET_'
API_KEY = ''
SECRET_KEY = ''
TIMEOUT = 10
VERSION = 0.1
URL = 'https://api.mailjet.com/%(VERSION)s/'

