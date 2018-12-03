import requests, datetime, threading, time

f = open("cookie.txt")
cookies = {"session": f.read().strip()}
f.close()

url ="https://adventofcode.com/2018/leaderboard/private/view/371128.json"

subject = "Standings"

msg = "{winner} is winning with {winner_points}! Loser is {second} with {second_points}! Today David has {david_stars} and Dad has {dad_stars}\n Inspiration? https://libraryofbabel.info/random.cgi"

class Leaderboard(threading.Thread):
	def __init__(self):
		self.refresh()
		
	def refresh(self):
		self.json = requests.get(url, cookies=cookies).json()
		self.codes = {n: self.json["members"][n]["name"] for n in self.json["members"].keys()}

	def users(self):
		return list(self.codes.values())

	def update(self):
		while True:


	def status(self):
		
		return {self.json["members"][n]["name"]: len(self.json["members"][n]["completion_day_level"][str(datetime.datetime.now().day)]) for n in self.codes}

	def rankings(self):
		return {self.codes[i]:self.json["members"][i]["local_score"] for i in sorted([n for n in self.codes.keys()], reverse=True, key=lambda x: int(self.json["members"][x]["local_score"]))}

l = Leaderboard()
print(l.rankings())
print(l.status())


