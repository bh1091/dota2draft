import requests
import json
import datetime
import time



class match_fetcher:
	def __init__(self):
		pass

	def run(self):
		for i in range(100):
			print "round " + str(i) + ' begin'
			filename = 'match_history/' + str(datetime.datetime.fromtimestamp(time.time())) + '.txt'
			save_file = open(filename,'w')
			match_list = self.get_match_list()
			self.get_match_detail(match_list, save_file)
			save_file.close()
			print "round " + str(i) + ' finished, sleep for 10 minutes'
			time.sleep(600)
		


	def get_match_list(self):
		url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?skill=3&key=D8023851199312FC130D5F896A60BD84'
		try:
			# print 'connecting'
			resp = requests.get(url)
			# print '1'
			# print resp.content
			json_match_list = json.loads(resp.content)
			# print '2'
			match_list = json_match_list['result']['matches']
			# print '3'
			return match_list
		except Exception, e:
			print "exception when get from url" + str(e)
			if str(e) == "HTTP Error 403: Forbidden":
				time.sleep(100)
	
	def get_match_detail(self, match_list, save_file):
		try:
			for match in match_list:
				if match['lobby_type']==0 or match['lobby_type']==7:
					match_id = match['match_id']
					url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id=' + str(match_id) + '&key=D8023851199312FC130D5F896A60BD84'
					try:
						resp = requests.get(url)
						json_match = json.loads(resp.content)
						self.save_match_result(json_match, save_file)
					except Exception, e:
						print "error when get match detail" + str(e)
						if str(e) == "HTTP Error 403: Forbidden":
							time.sleep(100)
							continue
		except Exception, f:
			print "error when getting match detail " + str(f)
			time.sleep(300)
		

	def save_match_result(self, json_match, save_file):
		if json_match['result']['radiant_win']:
			winner = 1
			print 'radiant_win'
		else:
			winner = 0
			print 'dire_win'
		player_list = json_match['result']['players']
		hero_list = []
		index = 0
		for player in player_list:
			hero_id = player['hero_id']
			if index>=5:
				hero_id = hero_id + 112
			hero_list.append(hero_id)
			print str(hero_id)
			index += 1
		# print 's' + str(len(hero_list))
		record = self.format_result(winner, hero_list)
		if 0 in hero_list:
			print 'not a 5v5 match, record abandoned'
		else:
			save_file.write(record+'\n')
			# print record
			

	def format_result(self, winner, hero_list):
		count = 0
		record = str(winner) + ' '
		for i in range(224):
			if i in hero_list:
				record = record + '1,'
				count += 1
			else:
				record = record + '0,'
		# print 'f' + str(count)
		return record[:-1]



				