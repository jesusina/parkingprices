#zipcrawl.py

#Go to urls of the format:

#https://boston.craigslist.org/search/prk?search_distance=0&postal=XXXXX&availabilityMode=0
#where XXXXX is a zipcode from a list
#make a list of all dollar value of parking spaces
#write output to a file of the form
#XXXXX \'t price
#

#datascrawl.py Start at a given base url passed at the command prompt
#and go from link to link, recording for each artist, the year the artist started, and the number of grammies 
#earned. Format: artist, year, grammies

import sys
import re
#import urllib2
#import urllib
from urllib.request import urlopen
#import urlparse
#try:
#    import matplotlib.pyplot as plt
#except:
    #raise
#import networkx as nx
import unicodedata

tocrawl=set([])
#ziplist=["02118","02119", "02120", "02130", "02134","02135","02445","02446","02447","02467","02108","02114","02115","02116","02215","02128","02129","02150","02151","02152","02124","02126","02131","02132","02136","02109","02110","02111","02113","02121","02122","02125","02127","02210","02458","02460","02465","02466","02472","02155","02149","02145","02144","02143","02138","02139", "02141"]
#was for boston
#ziplist0=[60007, 60018, 60068, 60106, 60131, 60176, 60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610, 60611, 60612, 60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620, 60621, 60622, 60623, 60624, 60625, 60626, 60628, 60629, 60630, 60631, 60632, 60633, 60634, 60636, 60637, 60638, 60639, 60640, 60641, 60642, 60643, 60644, 60645, 60646, 60647, 60649, 60651, 60652, 60653, 60654, 60655, 60656, 60657, 60659, 60660, 60661, 60706, 60707, 60714, 60804, 60827]


ziplist=[]
h=open("philly_zips_col2.csv,'r')
for line in h:
    ziplist.append(str(line.split(',')[0]))
    #5print("added: ",int(line.split(',')[0]))
#tocrawl = set([sys.argv[1]])
#for zip0 in ziplist:
#    urlname="https://chicago.craigslist.org/search/prk?search_distance=0&postal="+str(zip0)+"&availabilityMode=0"
#    tocrawl.add(urlname)
#tocrawl=set(['http://www.www.allmusic.com/artist/nirvana-mn0000357406'])
crawled = set([])
#keywordregex = re.compile('<meta\s*name=["\']keywords["\']\s*content=[\'|"](.*?)[\'|"]\s*>')
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'|"].*?>')
birthregex=re.compile('\d\d\d\d')
#grammyregex=re.compile('"grammy-award"')
#bandregex = re.compile('\">(.*?)</a>')
#<span class="result-meta">

priceregex= re.compile('result-meta[\'|"]>\n\s*<span\sclass=[\'|"]result-price[\'|"]>\$(\d*?)</span>')
allbands=[]
f = open("zip_2bedprice_phl.txt",'w')
g = open("zip_price2bed_raw_csvphl.csv",'w')
#G=nx.DiGraph()
avelist=[]
#while len(crawled)>-1:
cutoff=10000
for zip0 in ziplist:
    #https://boston.craigslist.org/search/aap?search_distance=0&postal=02127&min_bedrooms=2&max_bedrooms=2&availabilityMode=0
    urlname="https://philadelphia.craigslist.org/search/aap?search_distance=0&postal="+zip0+"&min_bedrooms=2&max_bedrooms=2&availabilityMode=0"
    try:
  #     crawling = tocrawl.pop()
        crawling=urlname
        #print crawling
    except KeyError:
        raise StopIteration
    ##url = urlparse.urlparse(crawling)

    response = urlopen(urlname)
    #url=urlopen(crawling)
    #print "url2=", url[2]
    #except:
#        continue
    msg = response.read()
    msgutf=msg.decode("utf-8")
 #   print(msgutf)
 #   startPos = msg.find('<body')
    prices=priceregex.findall(msgutf)
    #print("prices", prices)
    for eachprice in prices:
        #print("price: ", eachprice)
        if float(eachprice) > cutoff or len(eachprice)<2: # good cutoff for parking spots
            prices.remove(eachprice)
            while eachprice in prices:
                prices.remove(eachprice)
            print("removed ", eachprice," from ", zip0)
            print(prices)
    
    print ("number of prices in zip: ", zip0, len(prices))
    
    pricelist=[]
    for eachprice in prices:
        pricelist.append(float(eachprice))
        if float(eachprice) < cutoff:
            f.write(zip0+'\t'+ str(eachprice)+'\n')
    if len(pricelist)!=0:
        avelist.append([float(zip0),sum(pricelist)/len(pricelist)])
#        f.write("Average for" + zip0+": " + str(sum(pricelist)/len(pricelist)))
g.write("Zip code, Price($)"+'\n')
for mytuple in avelist:
    g.write(str(mytuple[0])+',' + str(mytuple[1])+ '\n')

f.close()
g.close()

