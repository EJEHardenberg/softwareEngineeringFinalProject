#!/usr/bin/env python
# Created 3MAR2013 
# Authors:
# 	Phelan
# 
# This handler processes user information entry. It renders a form for the user to input their name and age, then adds that
# to the database and forwards the user to the next page. 
from handler import *
from datetime import *
import hashlib
#re = regular expresion module
import re
from python.datastore import Players
from python.datastore import Games
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class PlayerInfoHandler(Handler):
	'''
		Handler for requests for the playerInformation.html page.
		Inherits from handler.
		Used to response to get or post requests.
	'''
	def renderPlayerInfo(self, name="", age="", error=""):
		'''
			renderPlayerInfo
			Used to render the appropriate template, with variables set for the name, age and error values.
			These are passed here in order to display error messages and make the form sticky.
			parameters:
				name, the name submitted to the template
				age, the age submitted to the template
				error, the error message submitted to the template
		'''
		self.render("playerInformation.html", name=name, age=age, error=error)

	def get(self):
		'''
			get
			Standard Get response method. Calls renderPlayerInfo.
		'''
		self.renderPlayerInfo()

	def validateInput(self,name,age):
		#validation for age and profanity	
		validAge = re.match("^[0-9]+$",age,re.M|re.I)
		swearWords = ["fuck", "shit", "suck my dick, I'm a shaaaaaark"]
		vulgarity = re.compile(r'\b%s\b' % '\\b|\\b'.join(swearWords), flags=re.IGNORECASE)
		error = ""

		if (name and age and validAge):
			#success. 
			# This is where we add their information to the database, as well as moving them to the next page.
			if vulgarity.search(name):
				error = "dang, get a bar of soap up in that biz!"
			else:
				return True,error
		else:
			if validAge:
				error = "We need both your name and your age!"
			else:
				error = "You must enter a number for your age"
		return False,error

	def post(self):
		'''
			post
			Respond to post requests from form. Pulls the name and age from the form and validates it. 
			On success, the user's information is added to the database and the system directs them to the next step.
		'''
		#get the parameters from the post
		name = self.request.get("name")
		age = self.request.get("age")
		#hash user info 
		time = str(datetime.now())
		m = hashlib.sha224()
		m.update(name)
		m.update(age)
		m.update(time)
		m.digest()
		
		valid,error=self.validateInput(name,age)
		sessionId = m.hexdigest()

		if valid:
			# add a new player to the datastore
			playerObj = Players(name=name, age=int(age), sessionId=sessionId)
			playerObj.put()
			# add a corresponding new game to the datastore
			gameObj = Games(sessionId=sessionId)
			gameObj.put()

			# redirect, with sessionID as a GET parameter
			self.redirect("/characterchoice" + "?sessionId=" + sessionId)
		else:
			self.renderPlayerInfo(name, age, error)