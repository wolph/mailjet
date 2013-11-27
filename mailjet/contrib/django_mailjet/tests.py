import time

from django.test import TestCase

import mailjet

from .forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def list_name_and_label(self):
        ts = int(time.time())

        result = (u'Test%s' % ts, u'test%s' % ts)

        self.temporary_lists.append(result)

        return result

    def setUp(self):
        self.temporary_lists = []
        self.list_name, self.list_label = self.list_name_and_label()

        self.api = mailjet.Api()

    def tearDown(self):
        lists = self.api.lists.all()['lists']

        for temporary_list in self.temporary_lists:
            for l in lists:
                if l['name'] == temporary_list[0]:
                    self.api.lists.delete(method='POST', id=l['id'])

    def test_add_contact(self):
        form = SubscriptionForm(
            data={'email': 'james@example.com'}, list_name=self.list_name,
            list_label=self.list_label)

        self.assertTrue(
            form.is_valid(), 'Form should be valid for test to continue')

        form.add_contact()

        for c in self.api.lists.contacts(id=form.list_id)['result']:
            if c['email'] == 'james@example.com':
                return

        self.fail('Contact was not created')

    def test_settings_override(self):
        name_fixture, label_fixture = self.list_name_and_label()

        with self.settings(MAILJET_LIST_NAME=name_fixture):
            form = SubscriptionForm()
            self.assertEqual(name_fixture, form.list_name)

            form = SubscriptionForm(list_name=self.list_name)
            self.assertEqual(self.list_name, form.list_name)

        # self.settings context manager cannot be used to override 2 settings
        with self.settings(MAILJET_LIST_LABEL=label_fixture):
            form = SubscriptionForm()
            self.assertEqual(label_fixture, form.list_label)

            form = SubscriptionForm(list_label=self.list_label)
            self.assertEqual(self.list_label, form.list_label)

    def test_save(self):
        def contact_in_list(email):
            for c in self.api.lists.contacts(id=form.list_id)['result']:
                if c['email'] == email:
                    return True
            return False

        form = SubscriptionForm(
            data={'email': 'james@example.com'}, list_name=self.list_name,
            list_label=self.list_label)
        self.assertTrue(
            form.is_valid(), 'Form should be valid for test to continue')
        self.assertFalse(
            contact_in_list('james@example.com'),
            'Contact must not be in list for test to continue')

        form.save()
        self.assertTrue(contact_in_list('james@example.com'))

        form = SubscriptionForm(
            data={'email': 'rick@example.com'}, list_name=self.list_name,
            list_label=self.list_label)
        self.assertTrue(
            form.is_valid(), 'Form should be valid for test to continue')
        self.assertFalse(
            contact_in_list('rick@example.com'),
            'Contact must not be in list for test to continue')

        form.save()
        self.assertTrue(contact_in_list('rick@example.com'))

    def test_clean_email(self):
        form = SubscriptionForm(
            data={'email': 'james@example.com'}, list_name=self.list_name,
            list_label=self.list_label)

        self.assertTrue(
            form.is_valid(), 'Form should be valid for test to continue')

        form.save()

        form = SubscriptionForm(
            data={'email': 'james@example.com'}, list_name=self.list_name,
            list_label=self.list_label)

        self.assertFalse(
            form.is_valid(), 'Form should detect duplicate email')
