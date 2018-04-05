+----------------------------------------------------------------------------+
|                                  READ THIS FIRST!!                         |
+============================================================================+
| This repository isn't compatible with the current Mailjet API (v3) and, as |
| a consequence, is considered deprecated and won't undergo further          |
| development. As such, this repository isn't under active maintenance.      |
+----------------------------------------------------------------------------+

Introduction
============

`Mailjet <http://www.mailjet.com>`__ is a real-time Cloud Emailing
platform and this is a python library to access the `Mailjet Web
API <https://mailjet.com/docs/api>`__.

Installation
============

-  Clone this repository:

``git clone https://github.com/WoLpH/mailjet``

-  ``cd`` into the cloned directory and execute:

``python setup.py install``.

The settings can be configured from a Django settings file through
``MAILJET_API_KEY`` and ``MAILJET_SECRET_KEY``, or through environment
variables with the same name.

i.e.

.. code:: py

    export MAILJET_API_KEY='YOUR_API_KEY'
    export MAILJET_SECRET_KEY='YOUR_SECRET_KEY'

Alternatively, you can just pass the API key and Secret key as
parameters when initializing the mailjet API as follows:

.. code:: py

    import mailjet

    mailjet_api = mailjet.Api(api_key='YOUR_API_KEY', secret_key='YOUR_SECRET_KEY')

Usage
=====

-  To get your account and profile information:

.. code:: py

    import mailjet

    mailjet_api = mailjet.Api(api_key='YOUR_API_KEY', secret_key='YOUR_SECRET_KEY')
    account_info = mailjet_api.user.infos()

``acount_info`` would now be assigned the following python dict:

.. code:: py

    {
        'status': 'OK',
        'infos': {
            'username': 'user@domain.com',
            'firstname': 'firstname',
            'locale': 'en_US',
            'lastname': 'lastname',
            'company_name': 'company_name',
            'contact_phone': None,
        }
    }

-  Create a new list of contacts, following on from the previous
   example:

.. code:: py

    contact_list = mailjet_api.lists.create(
        label='test',
        name='testlist',  # Only alphanumeric characters are allowed!
        method='POST'
    )

``contact_list`` will now contain a dictionary with the status and list
id as below:

.. code:: py

    {
        'status': 'OK',
        'contact_id': 000000000
    }

-  You can now add contacts to your list using the ``contact_id``:

.. code:: py

    mailjet_api.lists.addcontact(
        contact='example@example.com',
        id=contact_list['list_id'],
        method='POST'
    )

FAQ
===

How do I give reserved python keywords as parameters?
-----------------------------------------------------

Methods such as creating a campaign require you to use reserved python
keywords, such as ``from`` - hence, in order to overcome this, do the
following:

.. code:: py

    params = dict()
    params['method'] ='POST'
    params['subject'] = 'My first campaign'
    params['list_id'] = contact_list['list_id']
    params['lang'] = 'en'
    params['from'] = 'noreply@example.com'
    params['from_name'] = 'Your name'
    params['footer'] = 'default'
    campaign = mailjet_api.message.createcampaign(**params)

How do I debug errors?
----------------------

The errors produced by the ``mailjet`` library (or actually, produced by
the ``urllib2`` library) are still normal http responses. So if you wish
to read the actual response, do something like this:

.. code:: py

    try:
        contact_list = mailjet_api.lists.create(
            label='test',
            name='Test list',  # Incorrect because of the space in the name
            method='POST'
        )
    except Exception, e:
        print 'Mailjet response: %r, %r' % (e, e.read())
