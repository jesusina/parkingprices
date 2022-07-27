#datascrawl.py Start at a given base url passed at the command prompt
#and go from link to link, recording for each artist, the year the artist started, and the number of grammies 
#earned. Format: artist, year, grammies

import sys
import re
import urllib2
import urlparse
try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
import unicodedata

tocrawl = set([sys.argv[1]])
#tocrawl=set(['http://www.www.allmusic.com/artist/nirvana-mn0000357406'])
crawled = set([])
keywordregex = re.compile('<meta\s*name=["\']keywords["\']\s*content=[\'|"](.*?)[\'|"]\s*>')
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'|"].*?>')
birthregex=re.compile('\d\d\d\d')
grammyregex=re.compile('"grammy-award"')
#bandregex = re.compile('\">(.*?)</a>')
allbands=[]
f = open("artist_info.dat",'w')
G=nx.DiGraph()

while len(crawled)>-1:
    try:
        crawling = tocrawl.pop()
        #print crawling
    except KeyError:
        raise StopIteration
    url = urlparse.urlparse(crawling)
    #print "url2=", url[2]
    try:
        response = urllib2.urlopen(crawling+'/awards')
    except:
        continue
    msg = response.read()
    startPos = msg.find('<title>')
    if startPos != -1:
        endPos = msg.find('</title>', startPos+7)
        if endPos != -1:
            title = msg[startPos+7:endPos]
            bandEndPos=title.find(' - Awards')
            title=title[:bandEndPos]
            print title
    #        allbands.append([title])
    startPos = msg.find('<dd class="birth">')
    if startPos != -1:
        endPos=msg.find('<dd class="death">', startPos+19)
        if endPos != -1:
            birthspace = msg[startPos+19:endPos]#the space on the page containing relevant 
        
      #print influencelist
    birthyear=birthregex.findall(birthspace)
    print birthyear[0]  
    grammys = len(grammyregex.findall(msg))
    print grammys
    f.write(str(title)+'\t'+ str(birthyear[0])+'\t'+str(grammys)+'\n')
    try:
        response=urllib2.urlopen(crawling+'/related')
    except:
        continue
    msg=response.read()
    #print crawling+ '/related'
    startPos = msg.find('<h2>influenced by</h2>')
    if startPos != -1:
        endPos=msg.find('</ul>', startPos+22)
        if endPos != -1:
            infospace = msg[startPos+22:endPos]#the space on the page containing relevant "influenced by" info 
    
    startPos=msg.find('<h2>followers</h2>')
    if startPos != -1:
        endPos=msg.find('</ul>', startPos+19)
        if endPos != -1:
            infospace = infospace + msg[startPos+19:endPos]#add followers to list of links to be explored, network links to title band not added here
      #print allbands[-1]
    links = linkregex.findall(infospace)#list of all related bands to explore
    crawled.add(crawling)
    if len(crawled)%100==0:
        print "I have crawled ", len(crawled), " pages"
    for link in (links.pop(0) for _ in xrange(len(links))):
        if link not in crawled:
            tocrawl.add(link)
            #print "coming up soon:", link
#pos=nx.spring_layout(G)
#pos = nx.graphviz_layout(G)
f.close()

#nx.draw_networkx_nodes(G,pos,node_size=20)

#nx.draw_networkx_edges(G,pos)

#nx.draw_networkx_labels(G,pos, font_size=10, font_family='sans-serif')

#nx.draw_shell(G)

#plt.axis('off')
#plt.savefig("the_graph.png")
#plt.show()
