# import pandas as pd
# def import_ingre_fc():
#     #will want this to be done once and stored in db
#     fc_ingr_only = pd.read_csv('chef_buddy/raw_data/master_fc_ing.csv')
#     fc_ingr_only['matched'] = fc_ingr_only[['ingredient name', 'compound_id']].apply(tuple, axis=1)
#     ingredients_fc_id = {ingredient: [] for ingredient in fc_ingr_only['ingredient name']}
#     for ingredient, fc_id in list(fc_ingr_only['matched']):
#         if ingredient in ingredients_fc_id:
#                 ingredients_fc_id[ingredient].append(fc_id)
#     return ingredients_fc_id
#
# ingredient_to_fc_dict = import_ingre_fc()