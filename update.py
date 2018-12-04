import requests, datetime, threading, time, infinity
import sendgrid
import os
from sendgrid.helpers.mail import *

# PID = 14348

with open("cookie.txt") as f:
	cookies = {"session": f.read().strip()}

with open("key.txt") as f:
	key = f.read().strip()

url ="https://adventofcode.com/2018/leaderboard/private/view/371128.json"

subject = "Standings"
msg = "<h1>Advent of Code Standings</h1><h4>1. {winner}: {winner_points}<br>2. {second}: {second_points}<br><br> So far today David has completed {david_stars} parts and Dad has completed {dad_stars}.<br>Inspiration? https://libraryofbabel.info/random.cgi <br>Check out my terribly inefficient solutions https://github.com/Djsurry/AoC2018</h4><br><p>This code updates every 2 hours or on change in leaderboard</p>"


class Leaderboard(threading.Thread):
	def __init__(self):
		super().__init__()
		self.refresh()
		self.lastSent = infinity.Infinity()
		self.lastWinner = None

	def refresh(self):
		try:
			self.json = requests.get(url, cookies=cookies).json()
		except:
			self.json = {}
		self.codes = {n: self.json["members"][n]["name"] for n in self.json["members"].keys()}

	def sendEmail(self, winner, winner_points, second, second_points, david_stars, dad_stars):
		tos = ["dsurry@wearelcc.ca", "djsurry@gmail.com", "patrick.surry@gmail.com"]
		for to in tos:
		    sg = sendgrid.SendGridAPIClient(apikey=key)
		    from_email = Email("djsurry@wearelcc.ca")
		    to_email = Email(to)
		    content = Content("text/html",msg.format(
		    	winner=winner,
		    	winner_points=winner_points,
		    	second_points=second_points,
		    	second=second,
		    	david_stars=david_stars,
		    	dad_stars=dad_stars
		    ))
		    mail = Mail(from_email, subject, to_email, content)
		    response = sg.client.mail.send.post(request_body=mail.get())


	def run(self):
		while True:
			self.refresh()
			if not self.json:
				time.sleep(600)
				continue
			stars = self.status()
			rankings = self.rankings()
			if not self.lastWinner or rankings[0] != self.lastWinner:
				print("[*] Winner changed. Sending update email")
				self.sendEmail(self.codes[rankings[0]], self.json["members"][rankings[0]]["local_score"], self.codes[rankings[1]], self.json["members"][rankings[1]]["local_score"], stars["Djsurry"], stars["patricksurry"])
				self.lastSent = time.time()
			if time.time()-self.lastSent > 60*60*120 and datetime.datetime.now().hour > 6 and datetime.datetime.now().hour < 22:
				print("[*] Sending update email")
				self.sendEmail(self.codes[rankings[0]], self.json["members"][rankings[0]]["local_score"], self.codes[rankings[1]], self.json["members"][rankings[1]]["local_score"], stars["Djsurry"], stars["patricksurry"])
				self.lastSent = time.time()

			time.sleep(600)

	def status(self):
		
		return {self.json["members"][n]["name"]: len(self.json["members"][n]["completion_day_level"][str(datetime.datetime.now().day)]) for n in self.codes}

	def rankings(self):
		return [i for i in sorted([n for n in self.codes.keys()], reverse=True, key=lambda x: int(self.json["members"][x]["local_score"]))]

l = Leaderboard()
l.start()



