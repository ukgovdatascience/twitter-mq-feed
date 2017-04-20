import json
import tweepy
import pika
import sys
import os

# Set your keys and secrets: go to dev.twitter.com to create new app and get these
# I choose to set them as environment variables, but can also put in .env file
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret os.environ.get('CONSUMER_SECRET')
access_key = os.environ.get('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')

# set up the tweepy api feed
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# define the keywords you wish to track eg.:
keywords = ['#rstat', '#python']

try: 
    # Connect to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) 
    channel = connection.channel() 

    # Create a queue called <your_queue_name> 
    channel.queue_declare(queue='<your_queue_name>') 

except Exception as err:
    print err

# this is where the twitter magic happens: the stream listener
class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        
        # initialise the Twitter stream
        self.api = api
        super(tweepy.StreamListener, self).__init__()

    # this class defines a number of events and actions, eg. below
    # when data is received from the API we call on_data() and on_error
    # is called when we get an error so we can print the code.
    def on_data(self, tweet):
    	try: 

            # send the tweet into the message queue
            channel.basic_publish(exchange='',
                                  routing_key='<your_queue_name>',
                                  body=tweet)

        except Exception as err:
            print err

    def on_error(self, status_code):
	   print 'An error has occurred! Status = %s' % status_code
       return True # Don't kill the stream

    def on_timeout(self):
	   print 'Snoozing...ZzZzZzzzz'
       return True # Don't kill the stream

    def on_disconnect(self, notice):
       print 'Disconnected: %s' % notice
	   return False # Don't kill the stream

# start the stream, using the stream listener class that we define above
sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))

# start filtering the stream
sapi.filter(track=keywords, stall_warnings=True)
