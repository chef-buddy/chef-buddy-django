import csv
from chef_buddy.models import IngredientFlavorCompound

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