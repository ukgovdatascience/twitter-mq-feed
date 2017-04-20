# twitter-mq-feed

A sets of scripts that gets data from the Twitter real-time API, passes it to a message-queue (e.g. RabbitMQ) and stores tweets into MongoDB.

Usually scripts like this directly push tweets into a database from the API, but this causes problems when there are too many tweets to process directly, e.g. when you use many keywords or the rate of tweets coming in is higher than the rate at which they are inserted into the database. To deal with this you can insert tweets into a message queue - this will hold tweets until another script reads them from the queue and inserts them into a database. This way you can deal with high rates of tweets without crashing your script. 

## dependencies

Servers: 
+ mongodb server up and running (>=3.4; https://docs.mongodb.com/manual/installation/)
+ RabbitMQ server up and running (https://www.rabbitmq.com/install-debian.html)

For both, binaries are in the repositories of most distro's, but may be somewhat out-dated (yet functional). 

Libraries: 
+ pika (to communicate with the RabbitMQ server)
+ pymongo (to connect to the mongodb server)
+ tweepy (to access the twitter API)

These can be installed using pip: 

`(sudo) pip install pika`

## Setting the Twitter credentials

To start you need to create a consumer key and secret, and an access key and secret. Go to http://dev.twitter.com, log on and go to the apps tab. The consumer key and secret should be there, but there should be an option to also create access key and secret. Once you have those four values you can use them in the script. 

I chose to set the twitter credentials (the key and secret) in my Linux environment. You can set these by typing in the console: 

`export CONSUMER_KEY = "<your_consumer_key>'`

To make it persist after reboots you can put it in your .bashrc or other shell initialisation script, see: https://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables

Alternatively you can include them in the script themselves or create a .env file with key/value pairs. 

## How to run

First, there are several places in the script where you need to plug in your values, marked with pointy brackets. 

Once you have done this, you need to run two files for this to work. 

1. **sender.py** is the script that connects to the twitter API and queues messages into the RabbitMQ server. 
2. **receiver.py** reads tweets from the queue and inserts them into the mongodb server

It should not matter which script you run first, as the receiver will just listen out for messages once started. 




