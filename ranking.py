import logging, sys, getopt
logging.disable(sys.maxsize)

import time
from operator import itemgetter
import pandas as pd
import lucene
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity

#Retrieving relevant results using PyLucene
def retrieve(storedir, query, count):
        st = time.time()
        searchDir = NIOFSDirectory(Paths.get(storedir))
        searcher = IndexSearcher(DirectoryReader.open(searchDir))

        parser = QueryParser('Text', StandardAnalyzer())
        parsed_query = parser.parse(query)
        print("Query String:",query,"Query Terms:", parsed_query)

        topkdocs = []
        temp = count
        res_text = {}

        #Retrieve relevant information till the list containing unique results is not filled.
        while len(topkdocs) < count and time.time()-st < 30:
                topDocs = searcher.search(parsed_query, temp).scoreDocs
                for hit in topDocs:
                        doc = searcher.doc(hit.doc)
                        text = doc.get("Text")
                        id = doc.get("ID")

                        #Extra Functionality 1: Check for duplicate records
                        if text not in res_text.keys() and len(topkdocs) < count:
                                topkdocs.append({
                                        "score": hit.score,
                                        "text": text,
                                        "id": id
                                })
                        else:
                                temp+=1

                        #update the dictionary of unique tweets every round to keep an updated duplicate tweet checker.
                        res_text[text] = id

        #Return tweets in the decreasing order of their score. (i.e; Higher the score, better the match)
        print("Results fetched in ", time.time()-st, " seconds.")
        return sorted(topkdocs, key=itemgetter('score'), reverse=True)

def main(argv):
        #Extra Functionality 2: Provide users with the flexibility to provide custom query as well as required number of results.
        query = ''
        count = 10
        directory = ''

        #Command line argument handler
        opts, args = getopt.getopt(argv,"hc:q:d:",["count=","query="])
        for opt, arg in opts:
                if opt == '-h':
                        print ('ranking.py -q <query_string> -c <number-of-results> -d "sample_path_of_index_directory/"')
                        sys.exit()
                elif opt in ("-q", "--query"):
                        query = arg
                elif opt in ("-c", "--count"):
                        count = arg
                elif opt in ("-d", "--directory"):
                        directory = arg
        print("Top ", count, " Results:-")
        if query and directory:
                lucene.initVM(vmargs=['-Djava.awt.headless=true'])
                res = retrieve(directory, query, int(count))

                for i in range(len(res)):
                        print(str(i+1)+'. '+str(res[i]))

if __name__ == "__main__":
   main(sys.argv[1:])