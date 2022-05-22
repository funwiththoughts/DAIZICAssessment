#Goal 1: Identify the top 5 Soundcloud artists on Reddit for each of the past 3 months, using the pushshift API.

from urllib.request import urlopen
import unicodedata
import time

#Breakdown of subgoals:
#1. Get all Soundcloud links from each of the past 3 months
#2. For each month, make a list of artists featured
#3. Define a metric for comparing artists
#4. Identify the top 5 artists by the selected criteria, for each month

#Subgoal 1-2: Get all Soundcloud links from each of the past 3 months and make a list of artists included

#Get all artists with links from a specific number of months ago:
def artistsForMonth(monthsAgo):
    artistSet = set()
    linkurl = ""
    if(monthsAgo == 1):
        linkurl = "https://api.pushshift.io/reddit/search/submission/?url=soundcloud.com&after=30d&size=500&sort_type=score"
    else:
        startDate = monthsAgo*30
        endDate = (monthsAgo-1)*30 #Pushshift doesn't allow searching dates by month, so the month needs to be converted into a range of days before it can be used
        linkurl = "https://api.pushshift.io/reddit/search/submission/?url=soundcloud.com&after="+str(startDate)+"d&before="+str(endDate)+"d&size=500&sort_type=score" #Get the most popular artist links from the month, as many as allowed
    response = urlopen(linkurl)
    txt = response.read() #Read list of all Soundcloud-linking Reddit posts from the past 3 months, or as many as possible
    links = txt.splitlines()
    links = [link for link in links if b"soundcloud.com/" in link] #Filter out everything but the URLs for now
    
    for link in links:
        split = link.split(b'/') #Split the url up based on slashes
        artist = str(split[3]) #With links formatted as https://soundcloud.com/{artist}/..., the artist's name should be after the fourth slash
        artist = artist[2:len(artist)-1] #Due to being converted from bytes, each string will have "b'" at the start and "'" at the end, but we can get rid of these
        if(artist[len(artist)-2:len(artist)] == "\","):
            artist = artist[0:len(artist)-2]
        artist = "".join(ch for ch in artist if unicodedata.category(ch)[0] not in ["C","Z"]) #URLS aren't allowed to contain control characters, so we will need to remove any that end up in the artist's name in order to use it for searching later
        artistSet.add(artist) #Add the artist to our set -- as it is a set rather than a list, it will automatically delete duplicate entries
    
    return artistSet


#Subgoal 3. Define a metric for comparing artists
#Criteria used for ranking: number of links, number of views per link, number of upvotes per link, ratio of upvotes to downvotes per link, number of comments per link
def score(artist,monthsAgo):
    artistScore = 0
    linkurl = "https://api.pushshift.io/reddit/search/submission/?url=soundcloud.com/"+artist
    if(monthsAgo == 1):
        linkurl += "&after=30d&size=500&sort_type=score"
    else:
        startDate = monthsAgo*30
        endDate = (monthsAgo-1)*30
        linkurl += "&after="+str(startDate)+"d&before="+str(endDate)+"d&size=500&sort_type=score" #Get links the same way as before, but specifying the artist's name as a part of the URL
    
    while True:
        try:
            response = urlopen(linkurl)
            txt = response.read() #Read list of all Soundcloud-linking Reddit posts from the past 3 months, or as many as possible
            lines = txt.splitlines()
            break
        except:
            time.sleep(20) #Wait to avoid overloading the API with requests
    
    urls = [line for line in lines if b'"url": "https://soundcloud.com' in line] #Get each link
    commentNums = [line for line in lines if b"num_comments" in line]
    postScores = [line for line in lines if b'"score":' in line]
    upvoteRatios = [line for line in lines if b"upvote_ratio" in line] #Get each link, plus the number of comments, score and ratio for each
    
    for i in range(0,len(urls)):
        commentNum = str(commentNums[i].split(b':')[1]) #As the API will return the data with format "num_comments: {number}", we'll need to split at the colon to get the actual number -- similar methods will be used for the score and ratio
        commentNum = int(commentNum[2:len(commentNum)-2]) #Once again, we have to get rid of byte-type signifiers and the ending comma before using the integer
        postScore = str(postScores[i].split(b':')[1]) #As the API will return the data with format "num_comments: {number}", we'll need to split at the colon to get the actual number -- similar methods will be used for the score and ratio
        postScore = int(postScore[2:len(postScore)-2]) #Once again, we have to get rid of byte-type signifiers and the ending comma before using the integer
        upvoteRatio = str(upvoteRatios[i].split(b':')[1])
        upvoteRatio = float(upvoteRatio[2:len(upvoteRatio)-2])
        artistScore += postScore*upvoteRatio + commentNum*0.75 #Comment number is less informative than score and vote ratio since it's not feasible within this timeframe to determine how many comments are positive, hence the discount factor
    
    return artistScore

#Subgoal 4. Identify the top 5 artists for each month
def getTopArtists(monthsAgo,num):
    artistList = list(artistsForMonth(monthsAgo))
    artistList.sort(key=lambda artist: score(artist,monthsAgo),reverse=True) #Sort artists by score in descending order
    return artistList[0:num] #Return the top five
    
for i in range(1,4):
    print("i = ",i)
    print(getTopArtists(i,5))

#Results:
#Top 5 artists from last month: ['harvey-twyman', 'who_bigd', 'noticiashispanas', 'user-427000492', 'drwnhoe']
#Top 5 artists from 2 months ago: ['jeanbejuggin', 'who_bigd', 'noticiashispanas', 'musicbysimms', 'compacartel']
#Top 5 artists from 3 months ago: ['hunnacxsh', 'who_bigd', 'noticiashispanas', 'radioebenezerrd', 'track']
