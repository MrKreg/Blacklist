DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': ':memory:',
    }
}
