# Twitter Unfollow Inactive Friends
Script to detect inactive friends on twitter. The script works with the following python packages:
* Tweepy
* configmanager

The required dependencies are on the **requirements.txt** file. To install them run:
```
python -m pip install -r requirements.txt
```

## Script Configuration
### Configuration file location
The project comes with an example.ini file that you can use to fill with your own Twitter API credentials.
Don't forget to change the following line on the script:
```
config.read('..\..\TwitterAPI\config.ini')
```
It should point to wherever you save your .INI file with the authorization tokens. 
### Configuration parameters
* **API.Key and API.Secret**: Think of these as the user name and password that represents your Twitter developer app when making API requests.
* **Bearer.Token**: OAuth 2.0 Bearer Token authenticates requests on behalf of your developer App.
* **Access.Token and Access.Secret**: user-specific credentials used to authenticate OAuth 1.0a API requests.
* **General.ScreenName**: your twitter account screen name.
* **General.BatchSize**: the maximum number of friend acconts you wish to be able to remove on each run.
* **General.DaysInactive**: the time threshold to consider a friend as inactive, in days.

## The script
The program starts by importing the required modules for execution:
```
import configparser
import tweepy
from datetime import date
```
The first is for reading the configuration file, the second is to work with the Twitter API and the third is to be able to find the difference in days between two given date.

Before calling the twitter API, you must have the Twitter Developer account and a set of App's keys and tokens. Read more about it on the [official portal](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).

On the begining of the program, the Twitter App keys and tokens are read from the INI file:
```
config = configparser.ConfigParser()
config.read('..\..\TwitterAPI\config.ini')
```
The path should point to your INI file. The contents must follow the structure presented on the **example.ini** sample:
```
[API]
Key = <your api key>
Secret = <your api secret>

[Bearer]
Token = <your bearer token, for >

[Acess]
Token = <your access token>
Secret = <your access secret>

[General]
ScreenName = <the target user>
BatchSize = 10
DaysInactive = 5
```
After reading the INI file, we pass the tokens for authrozation and create the API object:
```
auth = tweepy.OAuthHandler(config['API']['Key'], config['API']['Secret'])
auth.set_access_token(config['Acess']['Token'], config['Acess']['Secret'])

api = tweepy.API(auth, wait_on_rate_limit=True)
```
The Twitter API has thresholds for the allowed rate on API calls. The **wait_on_rate_limit** flag configures a sleep time when the allowed rate is reached.

The script then tests calling the API by getting the User object and initializes an empty list of inactive friends:
```
user = api.get_user(screen_name=config['General']['ScreenName'])
inactive_friends = [];
```
Next we go through all the friends and check their last status. If they haven't tweeted for more than the configured DaysInactive parameter, their account is added to the inactive friends list:
```
for friend in tweepy.Cursor(api.get_friends, screen_name=user.screen_name).items(): 
        tweets_list= api.user_timeline(screen_name = friend.screen_name, count = 1)
        tweet= tweets_list[0] # last status of this friend (tweepy.models.Status)

        delta = date.today() - tweet.created_at.date()
        if (delta.days > int(config['General']['DaysInactive'])):
            inactive_friends.append(friend)
```
If the program has already reached the maximum number of intended inactive friends to remove, it exits the loop:
```
if (len(inactive_friends) >= int(config['General']['BatchSize'])):
    break
```
If there were inactive friends detected, the user's consent for removal is confirmed and those account will be unfollowed:
```
    if (len(inactive_friends) > 0):
        print('The following % s friends are inactive for more than 5 days:' % len(inactive_friends))
        for friend in inactive_friends:
            print(friend.screen_name)

        print('Unfollowing %s inactive users..' % len(inactive_friends))
        answer = input("Are you sure? [Y/n]").lower()
        if answer and answer[0] == "y":
            for friend in inactive_friends:
                print("Unfollowing " + friend.screen_name)
                friend.unfollow()
```
Please note, when creating the Twitter app on the developer portal, you must define it as read/write, otherwise the unfollow command will fail with an error. 