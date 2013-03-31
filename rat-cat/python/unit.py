#!/usr/bin/env python
# Created 3MAR2013 
# Authors:
# 	Ethan
# 
# This handler facilitates choosing the player character. It renders a template that allows the user to choose one of 6 
# characters, and then forwards the user to the next screen with that information. 

from handler import *
from time import time
import python.scores as ps
import python.playerinfo as pi

class UnitHarness(Handler):
	'''
		UnitHarness
		Inherits from handler. Used to respond to http requests for the /unit url
		Performs basic Unit tests on each python file. Generates statistics and information for each
	'''
	#Array to hold information about tests. Will
	tests=[{"name" :"Unit Test Harness", "passed" : True, "message" : "Test harness has been called correctly"}]

	def get(self):
		'''
			get
			Standard get method. Renders template.
		'''
		self.tests=[{"name" :"Unit Test Harness", "passed" : True, "message" : "Test harness has been called correctly"}]
		self.testScores()
		self.testPlayerInfo()
		self.render("unit.html",tests=self.tests)
		

	def addTest(self,name,passed=False,message="No Message Set"):
		self.tests.append({"name" : name, "passed" : passed, "message" : message})

	def testScores(self):
		'''
			testScores
			Tests the scores.py file's Handler's methods
		'''

		test = ps.ScoresHandler()

		#Retrieve the top scores
		#use clock() on windows, time() on nix
		sTime = time()
		eTime = 0.0
		try:
			topTen,sortKey = test.getTopScores()
			eTime = time()
		except Exception, e:
			self.addTest("scores.py", False, "Failed to retrieve top scores")
		else:
			self.addTest("scores.py", True, "Retrieved top scores in %2.5f seconds " % (eTime - sTime))

		#We can't really call render methods because those will cause
		#the gae to die.

	def testPlayerInfo(self):
		'''
			testPlayerInfo
			Tests the playerinfo.py file's validation function
		'''

		test = pi.PlayerInfoHandler()

		passed = True
		message = ""

		name=""
		age=""

		vPass,e = test.validateInput(name,age)
		if(vPass):
			message = message + "Failed to return invalid to empty arguments\n"
			passed = False
		else:
			pass

		name="Fuck"
		age=""

		vPass,e = test.validateInput(name,age)
		if(vPass):
			message = message + "Failed to return invalid to bad age argument\n"
			passed = False
		else:
			pass

		age="0"

		vPass,e = test.validateInput(name,age)
		if(vPass):
			message = message + "Failed to return invalid on profanity check\n"
			passed = False
		else:
			pass

		name="Test"
		
		vPass,e = test.validateInput(name,age)
		if(vPass):
			passed = passed and True
		else:
			message = message + "Failed to return valid on valid input arguments"

		if passed:
			message = "Validation Function working correctly"
		self.addTest("Player Info Validation",passed,message)




	