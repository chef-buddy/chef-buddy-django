import json
from django.test import TestCase, RequestFactory
from .views import random_recipe, show_top_recipe


class EngineTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        pass

    def test_call_api(self):
        request = self.factory.get('/api/v1/random_recipe/')
        response = random_recipe(request)
        self.assertEqual(response.status_code, 200)

    def test_show_top_recipe(self):
        data = {"user": "1", "liked": "1", "recipe": "Portobello-Mushroom-Schnitzel-1010037"}
        json_data = json.dump(data)
        print(json_data)
        print(type(json_data))
        request = self.factory.post('/api/v1/random_recipe/', json_data)
        response = random_recipe(request)
        self.assertEqual(response.status_code, 200)