Introduction
============

`mailjet` is a library to access the Mailjet REST API.

- http://www.mailjet.com/
- http://mailjet.readthedocs.org/en/latest/
- http://pypi.python.org/pypi/mailjet/

Install
=======

To install simply execute `python setup.py install`.

The settings can be configured from a Django settings file through
`MAILJET_API_KEY` and `MAILJET_SECRET_KEY`. Or through environment variables
the same name.

i.e.

::

    export MAILJET_API_KEY=something
    export MAILJET_SECRET_KEY=something_else

Usage
=====

To fetch data:

    >>> import mailjet
    >>> print mailjet.Api.user.infos()
    {
        u'status': u'OK',
        u'infos': {
            u'username': u'user@domain.com',
            u'firstname': u'firstname',
            u'locale': u'en_US',
            u'lastname': u'lastname',
            u'company_name': u'company_name',
            u'contact_phone': None,
        },
    }

To put data:

    >>> list_ = api.lists.create(label='Test', name='test')
    >>> print list_
    {u'status': u'OK', u'list_id': ...}
    >>> print api.user.addcontact(
        contact='user@domain.com',
        id=list_['list_id'],
    )


