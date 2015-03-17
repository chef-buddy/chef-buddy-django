import csv
from chef_buddy.models import IngredientFlavorCompound, UserFlavorCompound

def seed_ingredients():
    with open("chef_buddy/raw_data/master_fc_ing.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row[0])
            print(row[1])
            created = IngredientFlavorCompound(
                ingredient_id=row[0],
                flavor_id=row[1],
                )
            created.save()

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