'''
Created on Sep 28, 2013
'''

import sys
from nltk import sent_tokenize, collocations, metrics
from nltk import RegexpTokenizer
from nltk.corpus import stopwords, webtext
from nltk import pos_tag
import csv

def main(argv = None):
  
  english_stops = set(stopwords.words('english'))
  csvinfile = open('tweet.csv','rb')
  
  #para = "Hello World. It's good to see you. Just being here makes me jealous. 'this is in quotes', said the frog. I love to see you. I ate pies. I ate pies."
  filter_stops = lambda w: len(w) < 3 or w in english_stops
  
  bcf = collocations.BigramCollocationFinder
  
  documents = []
  reader = csv.DictReader(csvinfile)
  for row in reader: 
    
    token_sentence = RegexpTokenizer("[@]?[\w]+('\w)*|[\S]").tokenize(row["text"].lower()) 
    documents.append(token_sentence)
    print token_sentence
    #print pos_tag(token_sentence)
    #for word in token_sentence:
      #if word not in english_stops:
        #print word
    
  bcf2 = bcf.from_documents(documents)
  bcf2.apply_word_filter(filter_stops)
  print bcf2.nbest(metrics.BigramAssocMeasures.likelihood_ratio,15)
  return

if __name__ == '__main__':
    main(sys.argv)