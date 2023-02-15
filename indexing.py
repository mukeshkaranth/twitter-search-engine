import logging, sys
logging.disable(sys.maxsize)

import time
import glob
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import lucene
import os, getopt
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity

#Code snippet to fetch all the csv files in the data directory to be used for indexing.
path = os.getcwd()+'/data/'
csv_files = glob.glob(os.path.join(path, '*.csv'))
print("List of scanned files:")
print(csv_files)


#timing the indexing
times = []


#stop word removal
stop_words = set(stopwords.words('english'))
def removeStopWords(text):
        word_tokens = word_tokenize(text)
        # converts the words in word_tokens to lower case and then checks whether
        #they are present in stop_words or not
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        res = ' '.join(filtered_sentence)
        return res

#Indexing using PyLucene
def create_index(dir, tweets):

        if not os.path.exists(dir):
                os.mkdir(dir)

        #Initialization
        start_time = time.time()
        store = SimpleFSDirectory(Paths.get(dir))
        analyzer = StandardAnalyzer()
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)
        metaType = FieldType()
        metaType.setStored(True)
        metaType.setTokenized(False)
        contextType = FieldType()
        contextType.setStored(True)
        contextType.setTokenized(True)
        contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        #Indexing tweet id, text and created date.
        for tweet in tweets:
                created_at = tweet[0]
                tweet_id = tweet[1]
                tweet_text = tweet[2]
                doc = Document()
                doc.add(Field('Created_At', str(created_at), metaType))
                doc.add(Field('ID', str(tweet_id), metaType))
                doc.add(Field('Text', str(removeStopWords(str(tweet_text))), contextType))
                writer.addDocument(doc)
        writer.close()
        return time.time()-start_time
        #times.append({'size':len(tweets), 'time':(time.time() - start_time)})


def main(argv):
        #Extra Functionality 2: Provide users with the flexibility to provide custom query as well as required number of results.
        directory = ''

        #Command line argument handler
        opts, args = getopt.getopt(argv,"hd:",["directory="])
        for opt, arg in opts:
                if opt == '-h':
                        print ('indexing.py -d "format_of_sample_directory/"')
                        sys.exit()
                elif opt in ("-d", "--directory"):
                        directory = str(arg)
        if directory:

                lucene.initVM(vmargs=['-Djava.awt.headless=true'])

                tweets = []
                for csv in csv_files:
                        data = pd.read_csv(csv)
                        size = os.path.getsize(csv)
                        res = [list(row) for row in data.values]
                        tweets.extend(res)
                        print("Number of tweets scanned in ",csv, " : ", len(res))
                timeTaken = create_index(directory, tweets)
                times.append({'size':len(tweets), 'time':timeTaken})
                print("Total number of records scanned: ", len(tweets))

                print("Time taken: ")
                print(times)

if __name__ == "__main__":
   main(sys.argv[1:])