import json
from django.test import TestCase, RequestFactory
from .views import recipe_ingr_parse, recipes_to_fc_id, store_user_fc, find_user_fc_ids, rec_engine
from .models import Recipe, IngredientFlavorCompound, UserFlavorCompound

with open('chef_buddy/raw_data/yummly.json') as data_file:
    data = json.load(data_file)
    recipe_list = data['matches']

    class EngineTest(TestCase):
        def setUp(self):
            r = Recipe(recipe_id="Peanut-Butter-Chocolate-Melt-1038131", flavor_id='20')
            e = Recipe(recipe_id="Peanut-Butter-Chocolate-Melt-1038131", flavor_id='10')
            b = IngredientFlavorCompound(ingredient_id="butter", flavor_id='10')
            u = IngredientFlavorCompound(ingredient_id="butter", flavor_id='20')
            r.save()
            e.save()
            b.save()
            u.save()

        def tearDown(self):
            pass

        def test_data(self):
            self.assertEqual(data["totalMatchCount"], 910886)

        def test_recipe_parse(self):
            recipe_dict = recipe_ingr_parse(recipe_list)
            self.assertIsNotNone(len(recipe_dict))

        def test_recipe_fc_parse(self):
            fc_dict = recipes_to_fc_id(recipe_list)
            self.assertIsNotNone(len(fc_dict))

        def test_store_userfc(self):
            store_user_fc(1, "Peanut-Butter-Chocolate-Melt-1038131", 1)
            compounds = UserFlavorCompound.objects.filter(user_id=1)
            self.assertEqual(compounds[0].flavor_id, 10)
            self.assertEqual(compounds[1].flavor_id, 20)
            self.assertEqual(compounds[0].score, 1)

        def test_find_userfc(self):
            comp1 = UserFlavorCompound(user_id=2, flavor_id=4, score=1)
            comp2 = UserFlavorCompound(user_id=2, flavor_id=5, score=3)
            comp1.save()
            comp2.save()
            userfc_dict = find_user_fc_ids(2)
            self.assertEqual({4:1, 5:3}, userfc_dict)

        def test_rec_engine(self):
            recipe, recipe_fc = rec_engine(recipe_list, {10:1, 20:3})
            self.assertEqual(recipe['recipeName'], 'Buttery Garlic Bread')




