from django.test import TestCase, Client
from django.urls import reverse
from .models import *

class ListViewUnitTests(TestCase):

    def setUp(self):
        """
        set-up client environment
        """
        self.client = Client()

    def test_no_records_found(self):
        """
        If there are no customer records found in db, List view should return 'No records found
        Message'
        """
        last_ten_customer_records = ClientInfo.objects.order_by('-Date_Time')[:10]
        request = self.client.get(reverse('Home-Page'))
        self.assertEqual(len(request.context['customer_reference_details']), len(last_ten_customer_records))
