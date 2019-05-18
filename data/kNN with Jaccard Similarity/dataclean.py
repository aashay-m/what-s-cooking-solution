#Clean up the data by tokenizing the ingredients, generating a list from tokens, and splitting the dataset into train and test sets

import json

tokenized = []
tokenTest = []

ingredientList = []
ingredientSet = set()
	
with open('../train.json') as raw_data:
	data = json.load(raw_data)
	#tokenize
	for recipe in data:
		tokenizedRecipe = dict()
		tokenizedRecipe['cuisine'] = recipe['cuisine']
		tokenizedRecipe['ingredients'] = []
		for ingredient in recipe['ingredients']:
			if ingredient not in ingredientSet:
				ingredientSet.add(ingredient)
				ingredientList.append(ingredient)
			tokenizedRecipe['ingredients'].append(ingredientList.index(ingredient))
		tokenizedRecipe['ingredients'].sort()
		tokenized.append(tokenizedRecipe)
	
with open('../test.json') as test_data:
	test = json.load(test_data)
	for recipe in test:
		tokenizedRecipe = dict()
		tokenizedRecipe['id'] = recipe['id']
		tokenizedRecipe['ingredients'] = []
		for ingredient in recipe['ingredients']:
			if ingredient in ingredientList:
				tokenizedRecipe['ingredients'].append(ingredientList.index(ingredient))
		tokenizedRecipe['ingredients'].sort()
		tokenTest.append(tokenizedRecipe)

with open('cleanTokenData.json', 'w') as outfile:
	json.dump(tokenized, outfile)

with open('cleanTokenTest.json', 'w') as outfile:
	json.dump(tokenTest, outfile)
				