from django.views import generic
from django.conf import settings
from django.core.urlresolvers import reverse_lazy, reverse
from django import shortcuts

from .forms import SubscriptionForm


class SubscriptionView(generic.FormView):
    form_class = SubscriptionForm
    template_name = 'django_mailjet/subscription.html'
    success_url = reverse_lazy('django_mailjet_subscription_success')

    def form_valid(self, form):
        form.save()
        return super(SubscriptionView, self).form_valid(form)
