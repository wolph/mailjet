from django.conf.urls import patterns, url
from django.views import generic

import views

urlpatterns = patterns('newsletter.views',
    url(r'subscription/$', views.SubscriptionView.as_view(),
        name='newsletter_subscription'),
    url(r'subscription/success/$', generic.TemplateView.as_view(
        template_name='newsletter/subscription_success.html'),
        name='newsletter_subscription_success'),
)
