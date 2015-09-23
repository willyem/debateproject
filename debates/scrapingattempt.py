import requests
import bs4
import json
from lxml import html
import urllib
import urllib2
#from pymongo import MongoClient
#from pymongo.errors import DuplicateKeyError, CollectionInvalid
#import datetime as dt
links = []

for i in range(13):
    link = 'http://intelligencesquaredus.org/debates/past-debates?start=%s' % (i*9)
    page = requests.get(link)
    tree = html.fromstring(page.text)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    clicks = soup.select('.readmore')
    for link in clicks:
        links.append(link['href'])

#pdfurls = []


def findall(string, query):
    indices = []
    while True:
        index = string.find(query)
        string = string[index+1:]
        if index == -1:
            break
        else:
            indices.append(index)
    return indices
        
list_of_pdfs = [] 

for link in links: 
    url = 'http://intelligencesquaredus.org' + link
    page = requests.get(url)
    start = page.text.find('images/debates/past/transcripts')
    ends = findall(page.text, '.pdf')

    for index in ends:
        if index > start:
            end = index
            break

    list_of_pdfs.append('http://intelligencesquaredus.org/images/debates/past/transcripts/'+page.text[start+len('images/debates/past/transcripts/'):end+len('.pdf')])


#for pdf in list_of_pdfs: 
#    print pdf


for pdf in list_of_pdfs: 
    pdffile = urllib2.urlopen(pdf).read()                                  #function for opening desired url
    file_name = pdf.split('/')[-1]                                #Example : for given url "www.cs.berkeley.edu/~vazirani/algorithms/chap6.pdf" file_name will store "chap6.pdf"
    f = open(file_name, 'wb')                                     #opening file for write and that too in binary mode.
    f.write(pdffile)
    f.close()


   # tree = html.fromstring(page.text)
   # soup = bs4.BeautifulSoup(page.content, 'html.parser')
   # print soup
   # debatetranscript = soup.select("a[title='Read Transcript']")
   # print debatetranscript[0]['href']
   # pdfurls.append(debatetranscript[1]['href'])

#print pdfurls
#print soup
#print tree