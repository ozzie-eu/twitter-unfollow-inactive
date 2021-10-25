import configparser
import tweepy
from datetime import date

def main():
    #Read security tokens from external .ini file
    config = configparser.ConfigParser()
    config.read('..\..\TwitterAPI\config.ini')
    print('Read configuration file.')
    print(config.sections())

    #Pass tokens for authorization
    auth = tweepy.OAuthHandler(config['API']['Key'], config['API']['Secret'])
    auth.set_access_token(config['Acess']['Token'], config['Acess']['Secret'])

    #Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    #Get the user object
    user = api.get_user(screen_name=config['General']['ScreenName'])

    print(user.screen_name)
    print(config['General']['ScreenName'] + ' has ' + str(user.followers_count) + ' friends')

    #List to put the inactive friends in
    inactive_friends = [];

    for friend in tweepy.Cursor(api.get_friends, screen_name=user.screen_name).items(): 
        print('friend: ' + friend.screen_name)
        tweets_list= api.user_timeline(screen_name = friend.screen_name, count = 1)
        tweet= tweets_list[0] # last status of this friend (tweepy.models.Status)

        print('Last tweet:')
        print(tweet.created_at) #datetime object for the tweet
        print()

        delta = date.today() - tweet.created_at.date()
        #If the last status is older than the threshold on the .ini file,
        #the friend's name is added to the inactive friends list.
        if (delta.days > int(config['General']['DaysInactive'])):
            inactive_friends.append(friend)
        
        if (len(inactive_friends) >= int(config['General']['BatchSize'])):
            break

    #output the result
    if (len(inactive_friends) > 0):
        print('The following % s friends are inactive for more than 5 days:' % len(inactive_friends))
        for friend in inactive_friends:
            print(friend.screen_name)

        print('Unfollowing %s inactive users..' % len(inactive_friends))

        #To unfollow wothout prompt, comment the following 2 lines
        answer = input("Are you sure? [Y/n]").lower()
        if answer and answer[0] == "y":
            for friend in inactive_friends:
                print("Unfollowing " + friend.screen_name)
                friend.unfollow()


if __name__ == "__main__":
    main()