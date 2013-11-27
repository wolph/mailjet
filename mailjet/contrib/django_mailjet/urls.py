"""
Defines basic urls.

django_mailjet_subscription_form
    Url to the basic form view: SubscriptionView.

django_mailjet_subscription_success
    Url to the basic success template.
"""

from django.conf.urls import patterns, url
from django.views import generic

import views

urlpatterns = patterns('newsletter.views',
    url(r'subscription/$', views.SubscriptionView.as_view(),
        name='django_mailjet_subscription_form'),
    url(r'subscription/success/$', generic.TemplateView.as_view(
        template_name='django_mailjet/subscription_success.html'),
        name='django_mailjet_subscription_success'),
)
