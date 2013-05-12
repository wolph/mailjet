import urllib
import urllib2
from mailjet.conf import settings

class Connection(object):
    def __init__(self, api_key=None, secret_key=None, timeout=None):
        self.api_key = api_key or settings.API_KEY
        self.secret_key = secret_key or settings.SECRET_KEY
        self.timeout = timeout or settings.TIMEOUT
        self.opener = None

    def get_opener(self, url):
        if not self.opener:
            # Add the authentication data to a password manager
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(
                'Mailjet API',
                settings.URL,
                self.api_key,
                self.secret_key,
            )
            password_mgr.add_password(
                'Provide an apiKey and secretKey',
                settings.URL,
                self.api_key,
                self.secret_key,
            )
            # Create a handler for this password manager
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            # Create an opener for the handler
            self.opener = urllib2.build_opener(handler)

        return self.opener

    def open(self, method, function, options=None, postdata=None):
        url = u'%s%s%s' % (settings.URL, method, function)
        default_options = {
            'output': 'json',
        }
        if options:
            default_options.update(options)

        url += '?' + urllib.urlencode(default_options)
        if postdata:
            poststring = urllib.urlencode(postdata.items())
        else:
            poststring = None

        opener = self.get_opener(url)
        return opener.open(url, poststring, self.timeout)

    @classmethod
    def get_connection(cls, api_key, secret_key):
        return Connection(api_key, secret_key)
  
