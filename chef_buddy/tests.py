import json
from django.test import TestCase
from .views import recipe_ingr_parse, recipes_to_fc_id, store_user_fc, find_user_fc_ids, user_to_recipe_counter, store_recipe_fc
from chef_buddy.models import Recipe, IngredientFlavorCompound, UserFlavorCompound

with open('chef_buddy/fixtures/yummly_response.json') as json_data:
    data = json.load(json_data)
    recipe_list = data['matches']

    class EngineTest(TestCase):
        def setUp(self):
            r1 = Recipe(recipe_id="Honey-Oat-Bread-1033378", flavor_id=10)
            r2 = Recipe(recipe_id="Honey-Oat-Bread-1033378", flavor_id=20)
            fc1 = IngredientFlavorCompound(ingredient_id='salt', flavor_id=10)
            fc2 = IngredientFlavorCompound(ingredient_id='salt', flavor_id=20)
            r1.save()
            r2.save()
            fc1.save()
            fc2.save()

        def tearDown(self):
            pass

        def test_test(self):
            self.assertEqual(1, 1)

        def test_recipe_ingr_pasre(self):
            recipe_dict = recipe_ingr_parse(recipe_list)
            self.assertIn("salt", recipe_dict["Honey-Oat-Bread-1033378"])

        def test_recipes_to_fcid(self):
            recipe_dict = recipes_to_fc_id(recipe_list)
            self.assertIn(10, recipe_dict["Honey-Oat-Bread-1033378"])

        def test_store_userfc_positive(self):
            ufc1 = UserFlavorCompound(user_id=1, flavor_id=10, score=1)
            ufc1.save()
            store_user_fc(1, "Honey-Oat-Bread-1033378", 1)
            user_compounds = UserFlavorCompound.objects.filter(user_id=1)
            self.assertEqual(user_compounds[0].flavor_id, 10)
            self.assertEqual(user_compounds[1].flavor_id, 20)
            self.assertEqual(user_compounds[0].score, 2)
            self.assertEqual(user_compounds[1].score, 1)

        def test_store_userfc_negative(self):
            ufc1 = UserFlavorCompound(user_id=1, flavor_id=10, score=1)
            ufc1.save()
            store_user_fc(1, "Honey-Oat-Bread-1033378", -1)
            user_compounds = UserFlavorCompound.objects.filter(user_id=1)
            self.assertEqual(user_compounds[0].flavor_id, 10)
            self.assertEqual(user_compounds[1].flavor_id, 20)
            self.assertEqual(user_compounds[0].score, 0)
            self.assertEqual(user_compounds[1].score, -1)

        def test_store_userfc_zero(self):
            ufc1 = UserFlavorCompound(user_id=1, flavor_id=10, score=1)
            ufc1.save()
            store_user_fc(1, "Honey-Oat-Bread-1033378", 0)
            user_compounds = UserFlavorCompound.objects.filter(user_id=1)
            self.assertEqual(user_compounds[0].flavor_id, 10)
            self.assertEqual(user_compounds[0].score, 1)

        def test_find_userfcids(self):
            ufc1 = UserFlavorCompound(user_id=2, flavor_id=10, score=1)
            ufc2 = UserFlavorCompound(user_id=2, flavor_id=20, score=1)
            ufc1.save()
            ufc2.save()
            ids = find_user_fc_ids(2)
            self.assertEqual(ids, {10:1, 20:1})

        def test_user_to_recipe_counter(self):
            ufc1 = UserFlavorCompound(user_id=2, flavor_id=10, score=3)
            ufc2 = UserFlavorCompound(user_id=2, flavor_id=20, score=5)
            ufc1.save()
            ufc2.save()
            recipe_fc = recipes_to_fc_id(recipe_list)
            user_fc = find_user_fc_ids(2)
            scores = user_to_recipe_counter(recipe_fc, user_fc)
            self.assertIn(('Honey-Oat-Bread-1033378', 2), scores)

        def test_store_recipe_fcid(self):
            store_recipe_fc("bread", [5, 8, 9])
            recipe_fcs = Recipe.objects.filter(recipe_id="bread")
            for fc in recipe_fcs:
                self.assertIn(fc.flavor_id, [5, 8, 9])
