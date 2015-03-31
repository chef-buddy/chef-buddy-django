import csv
from chef_buddy.models import IngredientFlavorCompound, UserFlavorCompound, StaticRecipe

def seed_ingredients():
    with open("chef_buddy/raw_data/master_fc_ing.csv") as f:
        reader = csv.reader(f)
        print('bulk creating...')
        IngredientFlavorCompound.objects.bulk_create([IngredientFlavorCompound(ingredient_id=row[0],
                                                                               flavor_id=row[1],
                                                                               score=row[2])
                                                                               for row in reader])

def seed_users():
    with open("chef_buddy/raw_data/user_fc.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row[0])
            print(row[1])
            created = UserFlavorCompound(
                user_id=row[0],
                flavor_id=row[1],
                score=row[2]
                )
            created.save()


def seed_recipes():
    with open("chef_buddy/raw_data/static_recipes.csv") as f:
        reader = csv.reader(f)
        print('bulk creating...')
        recipe_list = []
        ingredient_list = []
        for row in reader:
            recipe = StaticRecipe(id=row[0],recipeName=row[1], imageUrlsBySize=row[2],
                                  sourceDisplayName=row[3])
            recipe_list.append(recipe)
            ingredient = [StaticIngredient(recipe_num_id=recipe.id, ingredient=ing) for ing in row[4].split(';')]
            ingredient_list.extend(ingredient)
        StaticIngredient.objects.bulk_create(ingredient_list)
        StaticRecipe.objects.bulk_create(recipe_list)
