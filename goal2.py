#Goal 2: Identify some Reddit accounts that stand out.

from urllib.request import urlopen
import time

#Choice for accounts to identify: Accounts that were early to post about more than one of the artists who became top-5 artists later.

TwoMonthsList = ['jeanbejuggin', 'who_bigd', 'noticiashispanas', 'musicbysimms', 'compacartel']
OneMonthList = ['harvey-twyman', 'who_bigd', 'noticiashispanas', 'user-427000492', 'drwnhoe']

possibleInterestingUsers = []

for artist in TwoMonthsList:
    linkurl = "https://api.pushshift.io/reddit/search/submission/?url=soundcloud.com/"+artist +"&after=90d&before=60d&size=500&sort_type=score" #Look at people who posted about top-5 artists from 2 months ago, 3 months ago
    userSet = set() #Want no duplicates for now
    
    print(linkurl)
    
    response = urlopen(linkurl)
    txt = response.read()
    lines = txt.splitlines()
    
    users = [line for line in lines if b'"author":' in line] #Usernames formatted as "author" by API
    for user in users:
        username = str(user.split(b': ')[1]) #The methodology for extracting the username from data is the same as extracting number of comments in goal 1
        username = username[2:len(username)-2]
        userSet.add(username)
        
    possibleInterestingUsers += list(userSet) #add the entire set to the list of potential interesting users

for artist in OneMonthList:
    linkurl = "https://api.pushshift.io/reddit/search/submission/?url=soundcloud.com/"+artist +"&after=90d&before=30d&size=500&sort_type=score" #Same as before, but here we look at people who posted about top-5 artists from one month ago, 2-3 months ago
    userSet = set() #Want no duplicates for now
    
    response = urlopen(linkurl)
    txt = response.read()
    lines = txt.splitlines()
    
    users = [line for line in lines if b'"author":' in line] #Usernames formatted as "author" by API
    for user in users:
        username = str(user.split(b': ')[1]) #The methodology for extracting the username from data is the same as extracting number of comments in goal 1
        username = username[2:len(username)-2]
        userSet.add(username)
        
    possibleInterestingUsers += list(userSet) #add the entire set to the list of potential interesting users

interestingUsers = set() #Now we check which of the possibly interesting users ended up being early on more than one artist
for user in possibleInterestingUsers:
    if possibleInterestingUsers.count(user) > 1:
        interestingUsers.add(user) #If the user was early to post about more than one artist, add them to the list

print(interestingUsers)

#Only interesting users identified: {'"Maurice_TheDemon"', '"noticias_hispanas"'}
