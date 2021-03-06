from bs4 import BeautifulSoup
import requests
import re
import csv
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36"}

html = requests.get('http://www.alhosnu.ae/WS/Site/AcademicApp/FacultiesAndDepartments.aspx',headers = headers)
htmltext = html.text
soup = BeautifulSoup(htmltext,'lxml')
results_courses = soup.findAll('td',attrs={'class':'SideMenuSection'})

length_results = len(results_courses)
"""
extracting links to courses websites
"""
all_results_links = []
for i in range(0,length_results):
    #regex = re.escape('<a href="Department.aspx?fid=&amp;')+'(.+?)'+re.escape('" class="NormalLinkLight" style="line-height:22px;">')+'(.+?)'+re.escape('</a>')
    regex = re.escape('<a class="NormalLinkLight" href="Department.aspx?fid=&amp;')+'(.+?)'+re.escape('" style="line-height:22px;">')+'(.+?)'+re.escape('</a>')
    pattern = re.compile(regex)
    results_links = re.findall(pattern,str(results_courses[i]))
    all_results_links.append(results_links)
    #print results_links
print len(all_results_links)
"""
professors sid
"""

all_prof_sid = []
length_all_results_links = len(all_results_links)
for i in range(0,length_all_results_links):
    pro_links = requests.get('http://www.alhosnu.ae/WS/Site/AcademicApp/Department.aspx?fid=&'+all_results_links[i][0][0],headers = headers)
    #print pro_links.text
    soup_prof = BeautifulSoup(pro_links.text,'lxml')
    results_prof = soup_prof.findAll('a',attrs={'class':'BlackLink'})
    #print results_prof
    length_results_prof = len(results_prof)
    for j in range(1,length_results_prof):
        regex_prof = re.escape('<a class="BlackLink" href="')+'(.+?)'+re.escape('"></a>')
        pattern_regex_prof = re.compile(regex_prof)
        results_regex_prof = re.findall(pattern_regex_prof,str(results_prof[j]))
        if(len(results_regex_prof)!=0):
            all_prof_sid.append(results_regex_prof)
        

"""
individual professors data
"""
c = csv.writer(open("data.csv", "wt"))
#pro_indiv_link = requests.get('http://www.alhosnu.ae/WS/Site/AcademicApp/StaffMember.aspx?sid=69fb82da-a176-40c5-8fa9-21e94558457b',headers = headers)
length_all_prof_sid = len(all_prof_sid)
for i in range(0,length_all_prof_sid):
    pro_indiv_link = requests.get('http://www.alhosnu.ae/WS/Site/AcademicApp/'+all_prof_sid[i][0],headers = headers)
    soup_indiv_link = BeautifulSoup(pro_indiv_link.text,'lxml')
    results_indiv_link = soup_indiv_link.findAll('td',attrs={'class':'BlackLink'})
    results_indiv_link_post = soup_indiv_link.findAll('div',attrs={'class':'BlackLink'})
    results_indiv_link_name = soup_indiv_link.findAll('td',attrs={'class':'InnerPageHeader'})
    
    print results_indiv_link_name[0].text
    print results_indiv_link_post[0].text
    try:
        c.writerow([results_indiv_link_name[0].text,results_indiv_link_post[0].text])
    except UnicodeEncodeError:
        print 'yes'
    for tag in results_indiv_link:
        print tag.text,"TAG"
    try:
        c.writerow([results_indiv_link[1].text,results_indiv_link[3].text,results_indiv_link[5].text,results_indiv_link[7].text,results_indiv_link[9].text])
    except UnicodeEncodeError:
        print 'yes'

