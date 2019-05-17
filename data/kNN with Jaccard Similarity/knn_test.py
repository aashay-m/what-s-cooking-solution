import json
import heapq
from collections import Counter

'''
Cleans up data for running
'''
def cleanData(data):
	train = [(recipe['cuisine'], set(recipe['ingredients'])) for recipe in data]
	return train

def cleanTestData(data):
	test = [(recipe['id'], set(recipe['ingredients'])) for recipe in data]
	return test

'''
Finds the nearest recipe based on the number of the same
ingredients between recipes
'''
def findNearest(item, train, n=1):
	#List of cuisine, distance value tuples
	topn = [(0, '') for i in range(n)]
	heapq.heapify(topn)
	
	distances = [0]*len(train)
	mying = item[1] #quick reference for tested item's ingredient set
	for i in range(len(train)):
		#length of intersection between both ingredient sets
		distances[i] = (1.0 * len(mying & train[i][1]) / len(mying | train[i][1]) , train[i][0])
		#Subsitute topn in list if applicable
		heapq.heappushpop(topn, distances[i])
	#Sort the list based on the "length" aka number of same ingredients in descending order
	#distances.sort(key=lambda x: -1*x[1])
	
	#Return cuisine of closest item
	#return distances[0][0]
	cuisines = [i[1] for i in topn]
	if len(cuisines) > len(set(cuisines)):
		return max(set(cuisines), key=cuisines.count)
	else:
		return heapq.nlargest(1, topn)[0][1]
	#print(distances[:10])
		

import csv

n = 3
with open('cleanTokenData.json') as data:
	train = cleanData(json.load(data))
	with open('cleanTokenTest.json') as test_data:
		test = cleanTestData(json.load(test_data))
		print('loaded and cleaned data, now processing')
		with open('knn_submission_'+str(n)+'.csv', mode='w') as submit_file:
			submit = csv.writer(submit_file)
			submit.writerow(['id', 'cuisine'])
			#for each test item, find the nearest neighbors and calculate most likely cuisine
			counter = 0
			for food in test:
				cuisine = findNearest(food, train, n)
				submit.writerow([food[0], cuisine])
				counter += 1
				if counter % 1000 == 0:
					print('count: ', counter)
