'''
Created on Oct 20, 2013

@author: Jon
'''

import requests, time
import csv

class MyClass():
    '''
    This is a port of the Kickscraper Rubygem to Python. 
    It's designed to work under a slightly different set of constraints, but it works similarly.
    
    When called, it generates an api token for you and pulls all your custom-signed urls from the basic api call. These are saved throughout the session
    Currently this doesn't actually do anything with the results... it's meant to be called by another script
    '''

    def __init__(self,email,password):
        '''
        This generates an oauth api token that the program uses to make the initial call. Currently the token is only useful for that one call, but it is kept in case
        '''
        self.cat = []
        self.cats = []
        self.successful = False
        self.access_token = ""
        url = "https://api.kickstarter.com"
        self.headers = {'Accept' : "application/json, text/javascript; charset=utf-8"}#, 'User-Agent' : "PyKick/XXX"}
        auth_url = url+"/xauth/access_token?client_id=2II5GGBZLOOZAA5XBU1U0Y44BU57Q58L8KOGM7H0E0YFHP3KTG"
        token_response = ""
        try:
            token_response = requests.post(auth_url, headers = self.headers, verify = False, data = {'email' : email, 'password' : password })
            print "token response"
            print token_response.json()
            self.access_token = token_response.json()["access_token"]
            print "access token"
            print self.access_token
            time.sleep(2)
            url_url = "https://api.kickstarter.com/v1/?oauth_token="+self.access_token
            url_response = requests.get(url_url,headers = self.headers)
            self.successful = True
            return None
        except:
            print token_response.status_code    
            return None
    
    def track_category(self, cat_name = "video%20games", cat_id = 35):
		'''
		This instantiates a category class with the name of the proper category and allows a user to call all updated and newly-found projects from that category
		
		Currently it imports and exports to csv; if you want to plug it into an API or db just replace those calls. 
		It is inefficient, too, it should only call "live" projects from the db when that is plugged in. Currently it just overwrites the whole thing.
		
		Example flow:
		1. Pull all prjects with "live" from db
		2. Pull pages from Kickstarter until you hit those projects.
		3. Upload new and updated project data to db page by page
		4. Once you get past those projects, if you encounter a dead project, end loop (IE: if state is dead and id not in pulled_ids, end)

		Formatting used:
		id:#,
		creator:{<copied directly>},
		location:{<copied directly>},
		state:"live"/"finished",
		deadline:#,
		launched_at:#,
		name:"",
		blurb:"",
		link:"",
		goal:##.#,
		pledged:##.#,
		backers_count:##,
		currency:"",
		curreny_symbol:"",
		currency_trailing_code:T/F,
		'''
			
		csvout = open("csvout.csv",'wb')
		fieldnames = []
		
		'''
			Table is called kickgames
			_id
			creator
			created_at (launched_at)
			end_at (deadline)
			title (name)
			description (blurb)
			link
			urls[]
			goal
			pledged
		'''


		'''actual code'''
		game_page = 1
		total_hits = 1
		hits_parsed = 0
		more_to_discover = True
		projs = []
		while (more_to_discover is True) and (hits_parsed < total_hits):
			hits_parsed = hits_parsed + 20 #naive assumption that projects length is always going to be 
			discover_category = requests.get("http://www.kickstarter.com/discover/categories/" + cat_name, headers = self.headers, params = {"page":game_page})
			dscCat = discover_category.json()
			total_hits = dscCat["total_hits"]
			print discover_category.status_code
			if discover_category.status_code != 200:
				more_to_discover = False
				print discover_category.text
			else:
				for project in dscCat["projects"]:
					try:
						thisProj = {}
						thisProj["id"] 					= project["id"]
						thisProj["creator"] 		= project["creator"]
						thisProj["location"] 		= project["location"]
						thisProj["state"] 			= project["state"]
						thisProj["deadline"] 		= project["deadline"]
						thisProj["launched_at"] = project["launched_at"]
						thisProj["name"] 				= project["name"]
						thisProj["blurb"]				= project["blurb"]
						thisProj["link"] 				= project["urls"]["web"]["project"]
						thisProj["goal"]				= project["goal"]
						thisProj["pledged"]			= project["pledged"]
						thisProj["currency"]		= project["currency"]
						thisProj["currency_symbol"]		= project["currency_symbol"]
						thisProj["currency_trailing_code"]		= project["currency_trailing_code"]
						projs.append(thisProj)
						fieldnames = thisProj.keys()
						print thisProj
					except:
						print
						print "failure!!"
						print discover_category.text
						print "failure!!"
						print
						time.sleep(15)
				game_page = game_page+1
				time.sleep(4)
			
		csvwriter = csv.DictWriter(csvout,fieldnames)
		csvwriter.writeheader()
		csvwriter.writerows(projs)

mc = MyClass("login@login.login","secrectpassword!")   
mc.track_category()
#mc.refresh_categories()
#mc.track_category()
#mc.cat[0].getProjects()