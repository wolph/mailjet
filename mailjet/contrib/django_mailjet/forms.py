from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms

import mailjet


class SubscriptionForm(forms.Form):
    """ Simple subscription form """
    email = forms.EmailField()

    def __init__(self, list_name=None, list_label=None, *args, **kwargs):
        """
        If `list_name` and `list_label` are None, then
        `settings.MAILJET_LIST_NAME` and `settings.MAILJET_LIST_LABEL` will be
        used.
        """
        self.list_name = list_name or settings.MAILJET_LIST_NAME
        self.list_label = list_label or settings.MAILJET_LIST_LABEL

        super(SubscriptionForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """ Raise ValidationError if the contact exists. """
        contacts = self.api.lists.contacts(id=self.list_id)['result']

        for contact in contacts:
            if contact['email'] == self.cleaned_data['email']:
                raise forms.ValidationError(
                    _(u'This email is already subscribed'))

        return self.cleaned_data['email']

    def save(self):
        """ Call `add_contact()` """
        self.add_contact()

    def add_contact(self):
        """ Create a contact with using the email on the list. """
        self.api.lists.addcontact(
            contact=self.cleaned_data['email'], id=self.list_id, method='POST')

    @property
    def api(self):
        """ Get or create an Api() instance using django settings. """
        api = getattr(self, '_api', None)

        if api is None:
            self._api = mailjet.Api()

        return self._api

    @property
    def list_id(self):
        """ Get or create the list id. """
        list_id = getattr(self, '_list_id', None)

        if list_id is None:
            for l in self.api.lists.all()['lists']:
                if l['name'] == self.list_name:
                    self._list_id = l['id']

            if not getattr(self, '_list_id', None):
                self._list_id = self.api.lists.create(
                    label=self.list_label, name=self.list_name,
                    method='POST')['list_id']

        return self._list_id
