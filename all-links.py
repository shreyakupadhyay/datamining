from bs4 import BeautifulSoup
import requests,re


"""
check function to check whether the links is there in the all_links_array if it is there than do not insert the link into the list
and if it is not there insert into the list
"""

def check(results):
    global  val
    for link in results:
        #print link['href']
        if(link['href'] not in all_links_array):
            all_links_array.append(link['href'])
            val = val + 1

def get_links(html):
    global val
    htmltext = html.text
    try:
        soup = BeautifulSoup(htmltext)
        results = soup.findAll('a')
        check(results)
    except KeyError:
        print "Next"

"""
getting first set
"""
all_links_array = []
val = 1
base_url = 'http://www.alhosnu.ae/WS/Site/Home/Home.aspx'
html = requests.get(base_url)
get_links(html)

depth = 1


val = len(all_links_array)

"""
In this depth is set to 3 this can be done to any value. Here required value is 20
"""

"""
Here this type of categorisation is done for links on three basis it can be genralised to more types.
"""
count = 0
while(depth!=3):
    for k in range(count,update_count):
        print all_links_array[k]
        if(len(re.findall(re.compile('^'+ re.escape('/')),all_links_array[k]))!=0):
            get_links(requests.get('http://www.alhosnu.ae'+all_links_array[k]))
            print val , "VAL"
        elif(len(re.findall(re.compile('^'+re.escape('../')),all_links_array[k]))!=0):
            all_links_array[k] =  all_links_array[k].replace('../','/')
            get_links(requests.get('http://www.alhosnu.ae/WS/Site'+all_links_array[k]))
            print val , "VAL"
        elif(len(re.findall(re.compile('^http:'+re.escape('//')+'\D'),all_links_array[k]))!=0):
            get_links(requests.get(all_links_array[k]))
            print val , "VAL"
    print all_links_array
    print count , "COUNT"
    print update_count , "UP-COUNT"
    count = update_count
    update_count = val
    depth=depth+1
    print val , "VAL"
#"""
