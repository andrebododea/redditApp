# -*- coding: utf-8 -*-
# https://praw.readthedocs.io/en/stable/index.html#main-page
import re
import praw
import urllib2
import json

# uses openlibrary api (https://openlibrary.org/dev/docs/api/search)
# creates an openlibrary search url and searches the database for all possible permutations of the search terms.
# if it finds a match for a title, it stores that title in a database.
def book_title_search(searchTerms):		
	permutations = []
	for i in xrange(0,len(searchTerms)+1):
		for j in xrange(i+1,len(searchTerms)+1):
			permutations.append(searchTerms[i:j])

	API_url = "http://openlibrary.org/search.json?title="
	for term in permutations:
		url = API_url
		for t in term:
			url += str(t)+'+'
		url = url[:-1] # removes the trailing '+'


		# TESTING
		print url
		# TESTING
	
                # makes the array of terms into a string, with each term serparated by spaces
                stringTerm = " ".join(term)

		json_data = urllib2.urlopen(url)
		data = json.load(json_data)
		# iterate through all returned values of the particular search
		for book in data["docs"]:
                        asciiTitle = book["title"].encode('ascii','ignore')
			
			if asciiTitle == stringTerm:
				print "we've got a match! --> " + asciiTitle +" ==? "+ stringTerm

# create the reddit object, r
r = praw.Reddit(user_agent = 'Test Script')

# gets a "submission object", using the submission_id
# a submission is basically a reddit post
# the submission referenced here is at url: https://www.reddit.com/r/books/comments/4o7lb0/i_just_read_the_old_man_and_the_wasteland_and_i/
submission = r.get_submission(submission_id='4o7lb0')

# we can flatten the comment forest to get a unordered list with the function praw.helpers.flatten_tree(). This is the easiest way to iterate through the comments and is preferable when you don’t care about a comment’s place in the comment forest
flat_comments = praw.helpers.flatten_tree(submission.comments)

array_of_words = []
# iterating through all the comments and making each comment into an array of words 
for comment in flat_comments:
	array = str(comment.body).split()
	titleWords = filter(str.istitle,array) # array only with the words that start with a capital letter
	
	# get rid of any non-alphanumeric characters except spaces and colons
	for i in xrange(len(titleWords)):
		titleWords[i] = re.sub(r'[^a-zA-Z0-9 :]', '', titleWords[i])
		print titleWords[i]
	
	print titleWords
	book_title_search(titleWords)

# Next step is to run the words from titleWords through a database of books to return titles of books and discard other words (nonsensical letters etc...)
