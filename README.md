# Twitter Unfollow Inactive Friends
Script to detect inactive friends on twitter. The script works with the following python packages:
* Tweepy
* configmanager

The required dependencies are on the **requirements.txt** file.

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
* **General.BatchSize**: the number of friend acconts you wish to scan on each run.
* **General.DaysInactive**: the time threshold to consider a friend as inactive, in days.

