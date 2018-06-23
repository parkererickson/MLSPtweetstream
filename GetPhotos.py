
# coding: utf-8

# In[ ]:


from twitter import Api
import config
import wget
import json
import pymysql


# In[ ]:


api = Api(config.consumer_key,
          config.consumer_secret,
          config.access_token_key,
          config.access_token_secret)
    


# In[ ]:


rds_host  = config.db_endpoint
name = config.db_username
password = config.db_password
db_name = config.db_name
port = 3306


# In[ ]:


conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)


# In[ ]:


USERS = ['@mlstylephoto']


# In[ ]:

while True:
	try:
		tweet_id  = 115
		for line in api.GetStreamFilter(track=USERS):
    			tweet = line
    			media = tweet.get('extended_entities', {}).get('media', [])
   		 	user = tweet.get('user', {}).get('screen_name', [])
    			time = str(tweet.get('created_at'))
    			if (len(media) == 0):
        			pass
    			else:
        			tweet_id = tweet_id + 1
        			pic = [item['media_url'] for item in media]
        			url_1 = str(pic[0].encode("utf-8"))
        			url_2 = str(pic[1].encode("utf-8"))
        			with conn.cursor() as cur:
            				cur.execute('insert into NewTweets (Time, Picture, StylePic, Username, id) values("'+time+'","'+url_1+'","'+url_2+'","'+str(user)+'","'+str(tweet_id)+'")')
            				conn.commit()
	except:
		pass
