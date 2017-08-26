from math import sqrt

# Return a euclidean distance-based similarity score for person1 and person2
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