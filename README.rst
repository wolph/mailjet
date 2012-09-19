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
    >>> print mailjet.Api().user.infos()
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

    >>> import mailjet
    >>> api = mailjet.Api()
    >>> list_ = api.lists.create(label='Test', name='test')
    >>> print list_
    {u'status': u'OK', u'list_id': ...}
    >>> print api.user.addcontact(
        contact='user@domain.com',
        id=list_['list_id'],
        method='POST',
    )

FAQ
==========================================

How do I give reserved python keywords as parameters?
------------------------------------------------------

As expained in #1:

::

    c = dict()
    c['method'] ='POST'
    c['subject'] = 'Test'
    c['list_id'] = list_['list_id']
    c['lang'] = 'en'
    c['from'] = 'noreply@foo.com'
    c['from_name'] = 'foo'
    c['footer'] = 'default'
    campaign_ = api.message.createcampaign(**c)

