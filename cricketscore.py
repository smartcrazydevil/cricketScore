from bs4 import BeautifulSoup
from urllib.request import urlopen
import subprocess
import time
import sys
import calendar
country = input("Live Score of Country ")      #getting from user the country
baseUrl = "http://www.espncricinfo.com"
livematch = {}
month = dict((v,k) for k,v in enumerate(calendar.month_abbr))

def totalMatch(baseUrl,county):
	url = baseUrl+"/ci/engine/match/index.html?search="+country
	html = urlopen(url)
	soup = BeautifulSoup(html,'html.parser')
	result = soup.find_all("section",class_="default-match-block")
	if(len(result)==0):                                        #checking the user has typed a valid country
		print("Sorry, Today is no match for this country!")
		sys.exit()
	else:
		res = soup.find_all("div",class_="match-info")
		dat = res[0].text.split()
		testMatch = dat[1].split('-') #checking for test match
		if(len(testMatch)>1):
			matchDate=matchDate = str(dat[2])+'-'+str(month[dat[0]])+'-'+str(testMatch[1])
		else:
			matchDate = str(dat[2])+'-'+str(month[dat[0]])+'-'+str(dat[1])
		today = time.strftime('%Y-%m-%d')
		if matchDate<today:   # check if the match is over and is not a test match
			victory = soup.find_all("div",class_="match-status")
			print("Latest Match Summary played on ",matchDate,"\n"," ".join(soup.find_all('div',class_='innings-info-1')[0].text.split()),"  ",
				" ".join(soup.find_all('div',class_='innings-info-2')[0].text.split()),victory[0].text.strip())
			sys.exit()
		else:
			for i,j in enumerate(result):
				team1 = " ".join(j.find_all('div',class_='innings-info-1')[0].text.split())
				team2 = " ".join(j.find_all('div',class_='innings-info-2')[0].text.split())
				livematch[j.find_all('a')[0]['href']]="''"+team1+"'' VS ''"+team2+"''"
			return(result)

def displayMatch():        #displaying the current matches going on
	for i,j in enumerate(livematch):
		print("Match:",i+1,"=>",livematch[j])
	

def sendmessage(scr):       #sending notification to ubuntu desktop
	subprocess.Popen(['notify-send',scr])
	return

def matchUrl():   # getting user input the display the notification for that particular match
	result = totalMatch(baseUrl,country)
	userChoice = displayMatch()
	cho = int(input("Enter the Match Number to get the notiifcation (Eg : 1)"))
	return(cho)


def getScore():    # function toshow the notification of the desired match
	newurl = baseUrl+list(livematch.keys())[int(choice)-1]
	getSocre = urlopen(newurl)
	newsoup = BeautifulSoup(getSocre,'html.parser')
	res = newsoup.title.text
	scr = res.split('|')[0]
	sendmessage(scr)

if __name__ == "__main__":
	choice = matchUrl()
	while True:
		getScore()
		time.sleep(60.0)      #will get the score after 60s

