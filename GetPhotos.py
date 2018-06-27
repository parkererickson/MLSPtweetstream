
# coding: utf-8

# In[1]:


from twitter import Api
import config
import wget
import json
import pymysql
import boto3

# In[2]:


api = Api(config.consumer_key,
          config.consumer_secret,
          config.access_token_key,
          config.access_token_secret)
    


# In[3]:


rds_host  = config.db_endpoint
name = config.db_username
password = config.db_password
db_name = config.db_name
port = 3306


# In[4]:


conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)


# In[5]:


USERS = ['@mlstylephoto']


# In[ ]:



for line in api.GetStreamFilter(track=USERS):
    tweet = line
    media = tweet.get('extended_entities', {}).get('media', [])
    user = tweet.get('user', {}).get('screen_name', [])
    time = str(tweet.get('created_at'))
    tweet_id = tweet.get('id')
    complete = 0
    print(tweet_id)
    if (len(media) == 0):
        pass
    else:
        pic = [item['media_url'] for item in media]
        url_1 = str(pic[0].encode("utf-8"))
        url_2 = str(pic[1].encode("utf-8"))
	try:
		ec2 = boto3.client('ec2', region_name = 'us-east-2')
		ec2.start_instances(InstanceIds=['i-08230cf0b47f62e76'])
	except:
		pass
        with conn.cursor() as cur:
            cur.execute('insert into Queue (Time, Picture, StylePic, Username, Tweet_ID, Complete) values("'+time+'","'+url_1+'","'+url_2+'","'+str(user)+'","'+str(tweet_id)+'","'+str(complete)+'")')
            conn.commit()
