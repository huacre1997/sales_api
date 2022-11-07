from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate
from http import HTTPStatus

from apps.users.models import CustomUser
from apps.sales.api.views import OrderViewSet
import json
from rest_framework.test import APIClient
from django.conf import settings
from os.path import join


class OrderViewsetTestCase(TestCase):
    # Comando para cargar la data de prueba para los tests
    # python manage.py dumpdata songs > fixtures/songs.json

    # Asignamos los fixtures creados
    test_fixtures = [
        'warehouse',

    ]
    test_fixtures_list = []
    path_to_fixtures = join(str(settings.BASE_DIR), 'sales_api/fixtures/')
    print(path_to_fixtures)
    for test_fixture in test_fixtures:
        test_fixtures_list.append(
            path_to_fixtures + '{}.json'.format(test_fixture))
    fixtures = test_fixtures_list
    print(test_fixtures_list)
    fixtures = ["fixtures/crm.json", "fixtures/warehouse.json",
                "fixtures/sales.json"]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_superuser(
            password='123456',
            email='admin@test.com'
        )

    def test_order_sale_result(self):
        data = json.dumps({"date": "2022-06-20",
                           "status": "False", "cliente": 2, "delivery": {
                               "address": "xxxxxxx",
                               "date": "2022-05-19",
                               "district": 1
                           }, "details": [
                               {
                                   "product": 1,
                                   "quantity": 48
                               },
                               {
                                   "product": 2,
                                   "quantity": 10
                               },
                               {
                                   "product": 3,
                                   "quantity": 15
                               },
                               {
                                   "product": 4,
                                   "quantity": 12
                               },
                               {
                                   "product": 5,
                                   "quantity": 24
                               },
                               {
                                   "product": 6,
                                   "quantity": 15
                               },
                               {
                                   "product": 7,
                                   "quantity": 36
                               },
                               {
                                   "product": 8,
                                   "quantity": 18
                               },
                               {
                                   "product": 9,
                                   "quantity": 24
                               },
                               {
                                   "product": 10,
                                   "quantity": 10
                               },
                               {
                                   "product": 11,
                                   "quantity": 18
                               },
                               {
                                   "product": 12,
                                   "quantity": 12
                               },

                           ]})

        client = APIClient()

        client.force_authenticate(user=self.user)
        # response = OrderViewSet.as_view({'post': 'create'})(request)
        response = client.post(
            '/api/sales/order/', data=data, content_type='application/json')
        # Check if the first dog's name is Balto, like it is in the fixtures:
        for i in response.data["data"]["details"]:
            print(i)
        self.assertEqual(response.status_code, HTTPStatus.CREATED._value_)
        self.assertEqual(response.data["data"]["total"], 4548.40)
