import tweepy
import re
import csv
import json
import codecs

def load_credentials():
	with open("key.json") as f:
		cred = json.load(f)

	return cred

def load_api(cred):
	auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
	auth.set_access_token(cred['access_token'], cred['access_token_secret'])

	return tweepy.API(auth)

def load_users(filename):
	users = []
	with open(filename) as f:
		for line in f:
			users.append(line.rstrip('\n'))

	return users

def save_to_file(filename):
	with codecs.open(filename, "wb", encoding='utf-8') as csvfile:
		fieldnames = ['username', 'content']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for result in results:
			content = re.sub(r"http\S+", "", result.text)
			content = content.replace("\n", " ").strip()
			content = ' '.join(content.split())
			if content != "":
				writer.writerow({'username': result.user.screen_name, 'content': content})

# MAIN METHODS

def main():
	cred = load_credentials()
	api = load_api(cred)

	users = load_users("userlist")

	results = []
	# query builder
	for user in users:
		try:
			print "Currently working: " + user
			for status in tweepy.Cursor(api.user_timeline, id=user, count=100).items(600):
				try:
					results.append(status)
				except Exception as e:
					raise e
					break
		except Exception as e:
			print e.message
			break
			
	save_to_file("dataset_emoji.csv");


if __name__ == '__main__':
	main()