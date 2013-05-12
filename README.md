Introduction
============

Mailjet is a real-time Cloud Emailing platform and this is a python library to access the [Mailjet Web API](https://mailjet.com/docs/api).

Installation
============

* Clone this repository:

`git clone https://github.com/WoLpH/mailjet`

* `cd` into the cloned directory and execute:

`python setup.py install`.

The settings can be configured from a Django settings file through
`MAILJET_API_KEY` and `MAILJET_SECRET_KEY`, or through environment variables with the same name.

i.e.

```py
export MAILJET_API_KEY=something
export MAILJET_SECRET_KEY=something_else
```

Alternatively, you can just pass the API key and Secret key as parameters when initializing the mailjet API as follows:

```py
import mailjet

mailjet_api = mailjet.Api(api_key='YOUR_API_KEY', secret_key='YOUR_SECRET_KEY')
```

Usage
=====

* To get your account and profile information:

```py
import mailjet

mailjet_api = mailjet.Api()
account_info = mailjet_api.user.infos()
```

`acount_info` would now be assigned the following python dict:

```py
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
```

* Create a new list of contacts, following on from the previous example:

```py
contact_list = mailjet_api.lists.create(
    label='test',
    name='Test list',
    method='POST'
    )
```

`contact_list` will now contain a dictionary with the status and list id as below:

```py
{
    'status': u'OK',
    'contact_id': 000000000
}
```

* You can now add contacts to your list using the `contact_id`:

```py
mailjet_api.lists.addcontact(
    contact='example@example.com',
    id=contact_list['list_id'],
    method='POST'
)
```

FAQ
======================================================

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

