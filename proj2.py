#proj2.py
import requests
from bs4 import BeautifulSoup
import pprint
#import urllib.request, urllib.parse, urllib.error


base_url = 'http://www.nytimes.com'  #make a request to nyt
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser") #parse 





#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

### Your Problem 1 solution goes here
first10= []
for h in soup.find_all("h2", class_= "story-heading"): #find all headings 
	#print (h)
	if h.a:
		y = (h.a.text.replace("\n", " ").strip())  
		first10.append(y)
	else:
		x = (h.contents[0].strip())
		first10.append(y)

print("The first ten story headings on NYT are.......\n ")
for story in first10[:10]:
	print(story)


#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

### Your Problem 2 solution goes here

base_url2 = 'https://www.michigandaily.com/'
r2 = requests.get(base_url2)
soup2 = BeautifulSoup(r2.text, "html.parser")


mostread= []
# for header in soup2.find_all("li", class_= "first"):
# 	#print(header)
# 	if header.a:
# 		x =(header.a.get_text())
		
# 	else:
# 		pass
	
for header in soup2.find_all("li"):
	#print (header)
	if header.a:
		x =(header.a.get_text())
		#print (x)
		y= x.split()
		if len(y)>2:
			mostread.append(x)
		
	else:
		pass

# for header in soup2.find_all("li", class_= "last"):
# 	if header.a:
# 		y= (header.a.get_text())
# 		mostread.append(y)
# 	else:
# 		pass



print ("Most read stories on the Daily are.......\n")
for line in mostread:
	print(line)

#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

### Your Problem 3 solution goes here

#print out the alt text for each image. If there is no alt text, print “No alternative text provided!”

newmanurl = "http://newmantaylor.com/gallery.html"
rr = requests.get(newmanurl)
prof_soup = BeautifulSoup(rr.text, "html.parser")


# for tag in prof_soup.find_all(True):
#     print(tag.name)


imgs = prof_soup("img") #find all img tags 

for img in imgs:	
	print(img.get('alt', 'No alternative text provided!')) #eithr get the alt= blah blah, if no "alt", print the message 

	# if img.alt:
	# 	y =img.alt.get_text()
	# 	print (y)
	# else:
	# 	print("No alternative text provided!")


#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

### Your Problem 4 solution goes here

basepage = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4" #probably a better way to do this .. baseurl + &page= + range[:5] ? using range somehow? len(range)? 
page2 = basepage + "&page=1"
page3 = basepage + "&page=2"
page4 = basepage + "&page=3"
page5 = basepage + "&page=4"
page6 = basepage + "&page=5"

urllist = [basepage, page2, page3, page4, page5, page6]


#get requests on each page ....



###PART 4.1: Get faculty contact pages!!!!####
def get_faculty_contacts(urllist):  #create a function so I dont have to write out all these steps every time 
	fac = []  #create dict
	for url in urllist:
		req = requests.get(url)
		facsoup= BeautifulSoup(req.text, "html.parser") 
		# go to the <div class = "field-item even"> and get <a href= >
		#p = facsoup.find_all("div", class_= "field-item even")  #make soup for all these
		#print (p)
		tags = facsoup("a")
		for item in tags:
			#if item.a: #if there is "a" value
				#i = item.href.get_text()
			i = item.get('href', None)  #have to get "href" value , NOT the title of the link in between tags which is "a" value, i.e. <a href=/10009> Contact Details </a>
			# print ("href test output..... " + str(i) )
			base = "https://www.si.umich.edu/"
			contacturl = base + str(i)
			if "node" in contacturl:
				#print ("href test output..... " + str(i) )
				fac.append(contacturl)
			#else: #if nonetype skip 
				#pass
	return fac 

contact_url_list = get_faculty_contacts(urllist)
print ("....Crawling Fac Pages....")
#print (contact_url_list)


###PART 4.2: Visit each faculty contact page, collect emails!!!!###

def get_fac_email(list1):  #have function that takes in a list of emails 
	mail = [] #make a new empty list
	for contact in list1: #for each fac page
		r = requests.get(contact) #make the request
		soup = BeautifulSoup(r.text, "html.parser") #and the soup
		# go to the <div class = "field-item even"> and get <a > 
		e = soup.find_all("div", class_= "field-item even")
		for i in e:
			if i.a: #if there is a value
				x = i.a.get_text()
				if "@" in x:
					mail.append(x)  #put what you get back in a list 
			else: #if nonetype then skip
				pass
	return mail#return the list

#print ("___Getting FACULTY EMAILS___")
fac_emails = get_fac_email(contact_url_list)
#print (fac_emails)
print ("Faculty Email List\n")
for prof in fac_emails:
	print (fac_emails.index(prof) +1, end=' ')
	print (" ", prof)

