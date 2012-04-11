from mailjet import default_settings
import os
import pprint

# Try to use Django settings if these are available
try:
    from django.conf import settings as django_settings
except ImportError:
    django_settings = None

# Also try the local settings, mostly used for testing
try:
    from mailjet import settings as local_settings
except ImportError:
    local_settings = None


__all__ = ['settings']

class Setting(object):
    def __init__(self, key, name=None,
            prefix=default_settings.SETTINGS_PREFIX, processors=None):
        '''Settings object that automatically fetches the settings from the 
        django settings, local overrides or local defaults
        
        key -- the variable name to look for
        name -- optional: the variable to write to, defaults to `key`
        prefix -- when looking in the django settings, use this prefix
        processors -- post-processing for the settings
        '''
        self.name = name or key
        self.key = key
        self.prefix = prefix
        self.processors = self.get_processors(processors)
        
    @classmethod
    def get_processors(cls, processors):
        if not processors:
            # None or empty list
            processors = []
        elif isinstance(processors, list):
            # List is allowed
            pass
        elif isinstance(processors, tuple):
            # Tuples need to be converted
            processors = list(processors)
        else:
            # Convert the rest into a list
            processors = [processors]
        
        return list(processors)
    
    def _get(self, settings, key):
        prefixed_key = self.prefix + key
        if prefixed_key in os.environ:
            return os.environ[prefixed_key]
        
        elif hasattr(django_settings, prefixed_key):
            return getattr(django_settings, prefixed_key)
        
        else:
            for settings in (local_settings, default_settings):
                if hasattr(settings, key):
                    return getattr(settings, key)
            
    def __call__(self, settings):
        value = self._get(settings, self.key)
        
        for processor in self.processors:
            value = processor(settings=settings, setting=self, value=value)
        
        return value

class ExecutablePathMixin(object):
    def _get(self, settings, key):
        paths = super(ExecutablePathMixin, self)._get(settings, key)
        for path in paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path

class WritablePathMixin(object):
    def _get(self, settings, key):
        paths = super(WritablePathMixin, self)._get(settings, key)
        for path in paths:
            if os.path.isfile(path) and os.access(path, os.W_OK):
                return path

class StringFormattingMixin(object):
    def _get(self, settings, key):
        value = super(StringFormattingMixin, self)._get(settings, key)
        return value % settings

class WritablePathSetting(WritablePathMixin, Setting): pass
class ExecutablePathSetting(ExecutablePathMixin, Setting): pass
class FormattedSetting(StringFormattingMixin, Setting): pass
class FormattedExecutablePathSetting(StringFormattingMixin,
    ExecutablePathSetting): pass
class FormattedWritablePathSetting(StringFormattingMixin,
    WritablePathSetting): pass

class Settings(object):
    _settings_cache = {}
    _settings = (
        FormattedSetting('API_KEY'),
        FormattedSetting('SECRET_KEY'),
        Setting('TIMEOUT'),
        Setting('VERSION'),
        FormattedSetting('URL'),
    )
    
    def __init__(self):
        if not self._settings_cache:
            for setting in self._settings:
                self._settings_cache[setting.name] = setting(self)
            self._settings = ()

    def __getattr__(self, key):
        if key in self._settings_cache:
            return self._settings_cache[key]
        else:
            value = getattr(django_settings, key)
        
        self._settings_cache[key] = value
        return value
        
    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setattr__(self, key, value):
        self._settings_cache[key] = value
    
    def __repr__(self):
        return '<%s %s>' % (
            self.__class__.__name__,
            pprint.pformat(self._settings_cache),
        )

settings = Settings()

