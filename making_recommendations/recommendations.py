from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {
	'Lisa Rose':
	{
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'Superman Returns': 3.5,
		'You, Me and Dupree': 2.5,
		'The Night Listener': 3.0
	},

	'Gene Seymour':
	{
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 1.5,
		'Superman Returns': 5.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 3.5
	},

	'Michael Phillips':
	{
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.0,
		'Superman Returns': 3.5,
		'The Night Listener': 4.0
	},

	'Claudia Puig':
	{
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'The Night Listener': 4.5,
		'Superman Returns': 4.0,
		'You, Me and Dupree': 2.5
	},

	'Mick LaSalle':
	{
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'Just My Luck': 2.0,
		'Superman Returns': 3.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 2.0
	},

	'Jack Matthews':
	{
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'The Night Listener': 3.0,
		'Superman Returns': 5.0,
		'You, Me and Dupree': 3.5
	},
	
	'Toby':
	{
		'Snakes on a Plane':4.5,
		'You, Me and Dupree':1.0,
		'Superman Returns':4.0
	}
}

# Return a distance-based similarity score for person1 and person2
def distance_similarity_score(prefs, person1, person2):
	# return zero if the two people do not share any recommendation
	if set(prefs[person1].keys()).isdisjoint(prefs[person2].keys()):
		return 0
	else:
		# Add up the squares of all the differences
		sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2)
			for item in prefs[person1] if item in prefs[person2]])

		return 1 / (1 + sum_of_squares)
