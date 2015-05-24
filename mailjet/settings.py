
'''
The global settings prefix can be changed by modifying the `SETTINGS_PREFIX`
variable. These settings can be overwritten by modifying the Django settings
(in that case the `SETTINGS_PREFIX` is used) or by modifying this file.
'''
# SETTINGS_PREFIX = 'MAILJET_'

'''The Mailjet authentication data'''
# API_KEY = None
# SECRET_KEY = None

'''The timeout for the POST/GET requests'''
# TIMEOUT = 10

'''The API version, currently only 0.1 is suported'''
# VERSION = 0.1

'''The url to fetch from, this is based on the version but this is not
required'''
# URL = 'https://api.mailjet.com/%(VERSION)s/'

