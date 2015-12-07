""" mirror.py
http://www.amazon.com/
"""
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import os
import re
import sys
import urllib2
import urllib

class PageParser(HTMLParser):
    """ class to parse an html page
        html: parsed html ready to save to file
        urls: urls to use for recursive search
    """
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self)
        self.html = ""
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.html += "<" + tag + " "
        for attr in attrs:
            #format urls for recursion
            if attr[0] == 'href':
                #relative to root
                if attr[1].startswith(".."):
                    self.urls.append(attr[1][3:])
                #outbound links
                elif attr[1].startswith("http://"):
                    None
                #links going deeper
                elif attr[1].startswith("/"):
                    self.urls.append("{fp}" + attr[1])
                #same directory as current link
                else:
                    self.urls.append("{fp}/" + attr[1])
            self.html += attr[0] + "=\"" + attr[1] + "\" "
        self.html += ">"

    def handle_endtag(self, tag):
        self.html += "</" + tag + ">"

    def handle_startendtag(self, tag, attrs):
        self.html += "<" + tag + " "
        for attr in attrs:
            if attr[0] == 'href':
                #relative to root
                if attr[1].startswith(".."):
                    self.urls.append(attr[1][3:])
                #outbound links
                elif attr[1].startswith("http://"):
                    None
                #links going deeper
                elif attr[1].startswith("/"):
                    self.urls.append("{fp}" + attr[1])
                #same directory as current link
                else:
                    self.urls.append("{fp}/" + attr[1])
            self.html += attr[0] + "=\"" + attr[1] + "\" "
        self.html += "/>"


    def handle_data(self, data):
        self.html += data.decode('utf-8')

    def handle_comment(self, data):
        self.html += "<!--" + data + "-->"

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.html += c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.html += c

    def handle_decl(self, data):
        self.html += "<!" + data + ">"




class Page(object):
    """ represents the page of a url
        url: url (relative to the page it was found on)
        fp: filepath (what should precede url to make a valid link)
        siteRoot: site root 
    """
    def __init__(self, url, fp):
        self.url = url
        self.fp = fp
        self.fileRoot = "site"
        self.siteRoot = "https://www.amazon.com"

    def save(self):
        url = self.url
        #add and update fp if necessary
        url = re.sub("{fp}", self.fp, url)
        last = url.rfind("/")
        self.fp = url[:last]
        filepath = url.split("/")



        url = self.siteRoot + "/" + url

        #case for the index page
        if len(filepath) == 1 and not filepath[0]:
            filepath.append("index.html")
 

        filename = filepath[-1]
                #create filepath to save on disk
        if not filepath[0]:
            filepath = os.path.join(self.fileRoot, *filepath[1:-1])
        else:
            filepath = os.path.join(self.fileRoot, *filepath[:-1])
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        #final write path
        filepath = os.path.join(filepath, filename)

        if os.path.isfile(filepath):
            return
                #write to file
        f = open(filepath, 'w')

        print "Processing:" , url
        r = urllib2.urlopen(url)
        if ".html" in filename:
            parser = PageParser()
            parser.feed(r.read())
            html = parser.html.encode('ascii', 'replace')
            f.write(html)
            f.close()
            
        else:
            f.write(r.read())
            f.close()


count = 0

def Save(str, url):
    try:
            global count
            URL = url
            STR = "site\\%s\\"%str+ "%d"%(count) + ".%s"%str
            urllib.urlretrieve(URL, STR)
            file = urllib.urlopen(URL)
            file.close()
           
            print url
            
            count += 1
    except:
        pass

def CutandSave(str, list):
    line = ""

    for i in range(len(list)):
        line = list[i]
        b = line.split("\"")
 
        extension = "." + str
        for j in range(len(b)):
            if extension in b[j]:
                c = b[j].split("?")
                for k in range(len(c)):
                    Save(str, c[k])
    



print "Enter extension(jpg, png etc.)"
str = raw_input()

os.makedirs("site\\%s"%str)

page = Page("", "")
dir = os.listdir("site");

if "index.html" not in dir:
    page.save()
   
pageSource = 'site\\index.html'
print pageSource
f = open(pageSource, 'r')
lines = f.readlines()
CutandSave(str,lines)

print count
f.close();

