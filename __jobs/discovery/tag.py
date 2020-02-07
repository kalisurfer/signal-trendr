'''
Created on Sep 28, 2013

Job: this script leverages the nltk natural language library to tokenize tweets from our list.  grabs the tweets.csv it then messages.append(s out the keyword occurances along with their number of coccurances)
'''

import sys
from nltk import sent_tokenize, collocations, metrics
from nltk import RegexpTokenizer
from nltk.corpus import stopwords, webtext
from nltk import pos_tag
import csv
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback



SENDER_ADDRESS = "robot@decoursey.net"
HOST = "rrt5-kbxp.accessdomain.com"
USERNAME = "robot@decoursey.net"
PASSWORD = "1@m@R0b0t"
USE_SSL = True
PORT = 587


def tag_and_discover(argv = None):
  messages = []
  english_stops = set(stopwords.words('english'))
  
  csvinfile = open('tweets.csv','rb')
  
  filter_stops = lambda w: len(w) < 3 or w in english_stops
  
  
  
  documents = []
  reader = csv.DictReader(csvinfile)
  for row in reader: 
    
    token_sentence = RegexpTokenizer("[@]?[\w]+('\w)*|[\S]").tokenize(row["CONTENT"].lower()) 
    documents.append(token_sentence)
    #messages.append(token_sentence)
    #messages.append(pos_tag(token_sentence))
    #for word in token_sentence:
      #if word not in english_stops:
        #messages.append(word)
  english_stops.add("http")
  english_stops.add("game")
  english_stops.add("@youtube")
  english_stops.add("iphone")
  english_stops.add("video")
  english_stops.add("play")
  english_stops.add("new")
  english_stops.add("win")
  english_stops.add("playing")
  english_stops.add("time")
  #english_stops.add("battlefield")
  bcf1 = collocations.TrigramCollocationFinder.from_documents(documents)
  bcf2 = collocations.BigramCollocationFinder.from_documents(documents)
  bcf2.apply_word_filter(filter_stops)
  bcf1.apply_word_filter(filter_stops)
  messages.append("++++++++++++++++Bigram++++++++++++++++++++++++++++++++++")
  messages.append(bcf2.nbest(metrics.BigramAssocMeasures.likelihood_ratio,40))
  messages.append("++++++++++++++++Trigram++++++++++++++++++++++++++++++++++")
  messages.append(bcf1.nbest(metrics.TrigramAssocMeasures.likelihood_ratio,40))
  messages.append("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  messages.append("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

  emailM = "++++++++++++++++Bigram++++++++++++++++++++++++++++++++++ \n"
  emailM = ''.join(emailM + str(bcf2.nbest(metrics.BigramAssocMeasures.likelihood_ratio,40)))
  emailM = ''.join("\n" + "++++++++++++++++Trigram++++++++++++++++++++++++++++++++++ \n" + str(bcf1.nbest(metrics.TrigramAssocMeasures.likelihood_ratio,40)))

  #send email
  # messages.append(send_mail("[keyword] matches in the last hour", "sean.net@gmail.com", emailM, None))
  
  # bcf2p1 = bcf1.ngram_fd.viewitems()
  # '''
  # for item in bcf2p1:
  #   if (item[len(item) - 1] >= 2):
  #     #messages.append(item[len(item) - 1], "<<======")
  #     messages.append(item)
  # '''
  messages = [str(message) for message in messages]
  return "\r\n".join(messages)

if __name__ == '__main__': 
	tag_and_discover(sys.argv)


