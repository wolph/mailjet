Django integration
------------------

Introduction
============

``mailjet.contrib.django_mailjet`` provides generic tools to plug basic
mailjet support in your project.

Advanced users may use
``mailjet.contrib.django_mailjet.forms.SubscriptionForm`` directly
without installing anything.

Installation
============

In ``settings.py``:

-  set ``MAILJET_LIST_NAME`` and ``MAILJET_LIST_LABEL``, note that it
   may not contain non-alphanumeric characters, those are used as
   defaults for
   ``mailjet.contrib.django_mailjet.forms.SubscriptionForm``,
-  add to ``INSTALLED_APPS``: ``mailjet.contrib.django_mailjet`` for
   templates to be loadable.

Include ``mailjet.contrib.django_mailjet.urls`` in ``urls.py``, ie.:

.. code:: py

        url(r'^newsletter/', include('mailjet.contrib.django_mailjet.urls')),

Users may now subscribe to your mailing list on ``/newsletter/``.
