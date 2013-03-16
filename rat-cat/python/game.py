#!/usr/bin/env python
# Created 4MAR2013 
# Authors:
# 	Phelan
# 
# This handler executes the actual game environment. 
from handler import *
from random import shuffle
import cgi
import logging
import simplejson as json

class GameHandler(Handler):
	'''
		GameHandler
		Main handler for rendering game elements in the templating system. Responds to get and post requests for the game url. Inherits from Hander for easy
		template rendering.
	'''
	def get(self):
		'''
			get
			You got your basic get method right here, but with a twist. 
			This method perfoms the intialization of the game state, creating the json objects that represent the game and
			json encoding them. It then renders them on the game template with jinja. 
		'''
		#perform initial creation and encoding of JSON object
		newState = self.initEncode()
		self.render("game.html", oldState='null', newState=newState)

	def post(self):
		'''
			post
			Responds to post requests for the resource.
			Takes in the json object from the view and, according to the state, executes the necessary data changes.
		'''
		# get the json object passed in by the view (assuming it is called currentState)
		# oldState = json.loads(self.request.get('state'))
		# logging.info(oldState)

		# send the object to the state parser, and get the new state of the gameboard
		# newState = parseState(oldState)

		# render the template with the new state
		# derp = json.dumps(oldState)

		#http://stackoverflow.com/questions/14520782/decoding-json-with-python-using-appengine
		#this works, the problem was that the json on the client side wasnt actually json
		jdata = json.loads(cgi.escape(self.request.body))
		logging.info(jdata)

		push = json.dumps(jdata)
		self.write(push)
		#this crap kind of works
		# self.write(self.request.body)
		# or
		# s = self.request.get('compCard')
		# self.write(s)


	def initEncode(self):
		'''
			initEncode
			Creates the initial JSON key:value pairs and encodes them to be sent to the game template.
			Returns:
				initialState, the initial state of the gameboard
		'''
		# make a list of lists of cards, flatten it, then shuffle it
		listOfLists = [ [0]* 4, [1]*4, [2]*4, [3]*4, [4]*4, [5]*4, [6]*4, [7]*4, [8]*4, [9]*9, [10]*3, [11]*3, [12]*3 ]
		deck = sum(listOfLists, [])
		shuffle(deck)

		newState = {"compCard" : [
						{"image" : str(deck.pop()), 'active' : 0, 'visible' : 0}, 
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 0}, 
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 0},
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 0}],  
					"playCard" : [
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 1}, 
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 0}, 
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 0},
						{'image' : str(deck.pop()), 'active' : 0, 'visible' : 1}], 
					"discard" : [], 
					"deck" : deck,
					"displayCard" : {'image' : "13", 'active' : 0}, 
					"knockState" : 0, 
					"state" : "waitingForDraw" 
				}
		# encode it
		return json.dumps(newState)

	def parseState(self, oldState):
		'''
			parseState
			Determines the state passed in by the view, then executes the appropriate function to handle that state.
			Parameters:
				oldState, the state passed in by the view
			Returns:
				newstate, the modified state
		'''

	# function to take in the json from the view
	# function to modify that json according to the state (switch statement here) <== this is the model
	# function to return the massaged data to the view
