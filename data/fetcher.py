import requests
import json

class match_fetcher:
	def __init__(self):
		pass

	def get_match_list(self, match_id):
		url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?start_at_match_id=' + match_id + '&key=D8023851199312FC130D5F896A60BD84'
		try:
			resp = requests.get(url)
			json_match_list = json.load(resp.content)
			match_list = json_match_list['result']['matches']
			return match_list
		except Exception, e:
			print "exception when get from url" + str(e)
			if str(e) == "HTTP Error 403: Forbidden":
				time.sleep(100)
				continue
	
	def get_match_detail(self, match_list):
		for match in match_list:
			if match['lobby_type']==0 or match['lobby_type']==7:
				match_id = match['match_id']
				