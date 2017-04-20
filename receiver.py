#!/usr/bin/env python
import pika
import pymongo
import json

# Try to connect to the RabbitMQ server
try: 
	# create the connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) 
    channel = connection.channel() 

    # Create a queue called <your_queue_name> 
    channel.queue_declare(queue='<your_queue_name>') 

except Exception as err:
    print err

# try to connect to the mongodb server
try: 
	db = pymongo.MongoClient().<your_db_name>
except Exception as err:
    print err


# this is the callback function we will use to insert the tweets into mongodb
def callback(ch, method, properties, body):
	# can choose to print tweet here - prints the json
    # print(" [x] Received %r" % body)
    try: 

    	# insert the tweet into collection called 'tweets' 
    	# (so <your_db_name>.tweets.count() will tell you how many records)
        db.tweets.insert(json.loads(tweet))

    except Exception as err:
        print err

# read the message queue and pass to 'callback', defined above
channel.basic_consume(callback,
                      queue='<your_queue_name>',
                      no_ack=True)

# this will end up in KeyboardInterupt exception
print(' [*] Waiting for messages. To exit press CTRL+C')

# start working through the tweets
channel.start_consuming()