import requests
from bs4 import BeautifulSoup as BS
import smtplib
import mysql.connector
import datetime
from email.mime.text import MIMEText

fileName = 'series.txt'
dbName = "TVQUERIES"
tableName = "UserInputs"

months = {'Jan.':'01','Feb.':'02','Mar.':'03','Apr.':'04','May':'05','Jun.':'06','Jul.':'07','Aug.':'08','Sep.':'09','Oct.':'10','Nov.':'11','Dec.':'12'}

currentDate = datetime.datetime.today().strftime('%Y-%m-%d')
currentYear = datetime.datetime.today().strftime('%Y')

def createDB():
	f = open('sqlinfo.txt','r')
	user,passwd = f.readline().split(' ')
	f.close()
	mydb = mysql.connector.connect(
	  host="localhost",
	  user=user,
	  passwd=passwd
	)
	myCursor = mydb.cursor()
	myCursor.execute("CREATE DATABASE IF NOT EXISTS %s"%dbName)
	myCursor.execute("USE %s"%dbName)
	myCursor.execute("CREATE TABLE IF NOT EXISTS %s (email VARCHAR(255), series VARCHAR(255))"%tableName)

def saveToDB(value):
	f = open('sqlinfo.txt','r')
	user,passwd = f.readline().split(' ')
	f.close()
	mydb = mysql.connector.connect(
	  host="localhost",
	  user=user,
	  passwd=passwd,
	  database = dbName
	)
	myCursor = mydb.cursor()
	sql = "INSERT INTO UserInputs (email,series) VALUES (%s, %s)"
	myCursor.execute(sql,value)
	mydb.commit()

def case1(date,f):
	print("Status:Next episode airs on %s\n"%date,file = f)

def case2(year,f):
	print("Status:The next season begins in %s\n"%year,file = f)

def case3(f):
	print('Status:The show has finished streaming all its episodes.\n',file = f)

def sendMail(content,userEmail):
	f = open('emailinfo.txt','r')
	emailId,emailPasswd = f.readline().split(' ')
	f.close()
	content['Subject'] = 'Status for given TV Series'
	mail = smtplib.SMTP('smtp.gmail.com',587)
	mail.ehlo()
	mail.starttls()
	mail.login(emailId,emailPasswd)
	mail.sendmail(emailId,userEmail,content.as_string())
	mail.close()

def getLink(searchQuery):
	googleSearch = "https://www.google.com/search?q=" + searchQuery + "tv series imdb"
	page = requests.get(googleSearch)
	soup = BS(page.text, "html.parser")
	return (soup.find('cite').text)

def getPageSoup(link):
	page = requests.get(link)
	pageSoup = BS(page.text,"html.parser")
	return pageSoup

def mergeLinks(link, nextLink):
	i = 0
	while not nextLink.startswith(link[i:]):
		i+=1
	nextLink = link[:i]+nextLink
	return nextLink

def formatDate(date):
	d,m,y = date.split(' ')
	formattedDate = y+'-'+months[m]+'-'+'0'*(2-len(d))+d
	return formattedDate

def main():
	createDB()
	userEmail = input('Email:')
	tvList = input('T.V. Series:').split(',')
	saveToDB([userEmail,','.join(tvList)])
	f = open(fileName,'w')
	for series in tvList:
		link = getLink(series)
		pageSoup = getPageSoup(link)
		name = (pageSoup.find("div",{"class":"title_wrapper"})).h1.text.strip()
		print('Tv Series Name: %s'%name, file = f)
		status = pageSoup.find("a",{"title":"See more release dates"}).text.strip()
		if(status.find(')')-status.find('(')==10):
			case3(f)
		else:
			nextLink = ((pageSoup.find("div",{"class":"seasons-and-year-nav"})).find('a')).get('href')
			nextLink = mergeLinks(link, nextLink)
			nextPageSoup = getPageSoup(nextLink)
			airdates = nextPageSoup.findAll("div",{"class":"airdate"})
			flag = True
			for airdate in airdates:
				date = airdate.text.strip()
				if(len(date)>4):
					date = formatDate(date)
					if(date>currentDate):
						case1(date,f)
						flag = False
						break
				elif(len(date)==4):
					if(date>= currentYear):
						case2(date,f)
						flag = False
						break
			if flag:
				case3(f)

	f = open(fileName,"r")
	content = MIMEText(f.read())
	sendMail(content,userEmail)
	f.close()

if __name__ == '__main__':
	main()