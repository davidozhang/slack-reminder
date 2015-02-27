import requests

def sendReminder():
	#find your token https://api.slack.com/web
	payload = """{ "access_token":"xoxp-2162427386-3360743925-3869996840-aa2c89",
				"text":"I am text",
				"username":"Not Kevin",
				"channel": "@kevin.martin"

}"""
	r = requests.post("https://hooks.slack.com/services/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", payload)
	print r.text

sendReminder()
