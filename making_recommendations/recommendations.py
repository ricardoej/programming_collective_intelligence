from math import sqrt

# Return a euclidean distance-based similarity score for person1 and person2
# You can read about other metrics for comparing items at
# http://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples.
def euclidean_distance_similarity_score(prefs, person1, person2):
	# return zero if the two people do not share any recommendation
	if set(prefs[person1].keys()).isdisjoint(prefs[person2].keys()):
		return 0

	# add up the squares of all the differences
	sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2)
		for item in prefs[person1] if item in prefs[person2]])

	# gives higher values for people who are similar
	return 1 / (1 + sum_of_squares)

# Return a person correlation-based similarity score for person1 and person2
# You can read about other metrics for comparing items at
# http://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples.
def person_correlation_similarity_score(prefs, person1, person2):
	# get the list of mutually rated items
	mutually_rated_items = list(set(prefs[person1].keys())
		.intersection(prefs[person2].keys()))

	# find the number of mutually rated items
	n = len(mutually_rated_items)

	# if they are no ratings in common, return 0
	if n == 0: return 0

	# add up all the preferences
	sum1 = sum([prefs[person1][item] for item in mutually_rated_items])
	sum2 = sum([prefs[person2][item] for item in mutually_rated_items])

	# sum up the squares
	sum1Sq = sum([pow(prefs[person1][item], 2) for item in mutually_rated_items])
	sum2Sq = sum([pow(prefs[person2][item], 2) for item in mutually_rated_items])

	# sum up the products
	pSum = sum([prefs[person1][item] * prefs[person2][item] for item in mutually_rated_items])

	# Calculate Pearson score
	num = pSum - (sum1 * sum2 / n)
	den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
	if den == 0: return 0

	return num / den

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=person_correlation_similarity_score):
	scores = [(similarity(prefs, person, other), other)
		for other in prefs if other != person]

	# sort the list so the highest scores appear at the top
	scores.sort()
	scores.reverse()

	# return n top results
	return scores[0 : n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=person_correlation_similarity_score):
	totals={}
	simSums={}
	
	for other in prefs:
		# don't compare me to myself
		if other != person:
			sim = similarity(prefs, person, other)

			# ignore scores of zero or lower
			if sim > 0:
				for item in prefs[other]:
					# only score movies I haven't seen yet
					if item not in prefs[person] or prefs[person][item] == 0:
						# Similarity * Score
						totals.setdefault(item, 0)
						totals[item] += prefs[other][item] * sim

						# Sum of similarities
						simSums.setdefault(item, 0)
						simSums[item] += sim

	# Create the normalized list
	rankings = [(total / simSums[item], item)
		for item, total in totals.items()]

	# Return the sorted list
	rankings.sort( )
	rankings.reverse( )
	return rankings

# Create a dictionary of items showing which other items they
# are most similar to.
def calculateSimilarItems(prefs, n=10):
	result={}
	
	# Invert the preference matrix to be item-centric
	itemPrefs = getItemCentricPrefs(prefs)

	for item in itemPrefs:
		# Find the most similar items to this one
		scores = topMatches(itemPrefs, item, n=n,
			similarity=euclidean_distance_similarity_score)

		result[item] = scores

	return result

# Invert the preference matrix to be item-centric
def getItemCentricPrefs(prefs):
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})

			# Flip item and person
			result[item][person] = prefs[person][item]
	return result

# Get recommended items by a user. This method uses a similarity dataset
# built earlier (itemMatch, created by calculateSimilarItems method).
# Thus, it do not have to calculate the similarities scores for all the
# other critics
# Item-based filtering is significantly faster than user-based when getting
# a list of recommendations for a large dataset, but it does have the
# additional overhead of maintaining the item similarity table

# Item-based filtering usually outperforms user-based filtering in sparse 
# datasets, and the two perform about equally in dense datasets.
# To learn more about the difference in performance between these
# algorithms, check out a paper called “Item-based Collaborative Filter-
# ing Recommendation Algorithms” by Sarwar et al. at http://citeseer.ist.
# psu.edu/sarwar01itembased.html.
def getRecommendedItems(prefs, itemMatch, user):
	userRatings = prefs[user]
	scores = {}
	totalSim = {}

	# Loop over items rated by this user
	for (ratedItem, rating) in userRatings.items():
		# Loop over items similar to this one
		for (similarity, similarItem) in itemMatch[ratedItem]:
			# Ignore if this user has already rated this item
			if similarItem in userRatings: continue

			# Weighted sum of rating times similarity
			scores.setdefault(similarItem, 0)
			scores[similarItem] += similarity * rating

			# Sum of all the similarities
			totalSim.setdefault(similarItem, 0)
			totalSim[similarItem] += similarity

		# Divide each total score by total weighting to get an average
		rankings=[(score / totalSim[ratedItem], ratedItem) 
			for ratedItem, score in scores.items()]

	# Return the rankings from highest to lowest
	rankings.sort( )
	rankings.reverse( )
	return rankings