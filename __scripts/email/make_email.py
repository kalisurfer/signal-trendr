import jinja2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "newsletter.html"

template = templateEnv.get_template( TEMPLATE_FILE )

# Specify any input variables to the template as a dictionary.
templateVars = {'games': [{'name': 'Game 1',
			      'img_url': 'http://imgur.com/RE2Y0v1',
			      'description': 'Description is here'},
			     {'name': 'Game 2'},]}
			     
# models.Game.find({"recent_rank": {"$gt": 0}}, {_id: 1, title: 1, day_sum: 1, recent_rank: 1, delta_24_recent_rank: 1}, {sort: {delta_24_recent_rank: 1}}).exec(function(err, trends24) {
			     
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
gameCollection = db.games
listing = gameCollection.find({"recent_rank": {"$gt": 0}}, 
     ).sort('delta_24_recent_rank', 1);

outputText = template.render( {"games": listing[0:10]} )

print outputText