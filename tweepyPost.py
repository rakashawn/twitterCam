#from Geeksforgeeks
# Tweet Using python
# sudo install pip tweepy
# create a twitter App
# https://apps.twitter.com

#import the module
import tweepy

#personal details
consumer_key = "your consumer_key"
consumer_secret = "your consumer_secret"
access_token = "your access_token"
access_token_secret = "your access_token_secret"

#Authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

#Authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Update the status
api.update_status(status = "Hello World !")

# wait for 600 seconds
time.sleep(600)

#Posting a tweet with a media filename

#same auth as above

api = tweepy.API(auth)
tweet = "Text part of the Tweet"
image_path = "path of the image"

#to attach the media file
status = api.update_status_with_media(image_path, tweet)
api.update_status(status = tweet)
