from pubmedidservice import PubMedIdService
from pubmeddataservice import PubMedDataService
from pubmeddatawordcount import PubMedDataWordCount
from pubmeddataassociationrule import PubMedDataAssociationRule
from pubmedvisual import PubMedVisual
from collections import OrderedDict
from operator import itemgetter




import os,sys
import time
#import pandas

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python main.py num_paper search_term\n")
        sys.exit(1)
    else:
        number = sys.argv[1]
        terms = sys.argv[2:]

    pubmedidservice = PubMedIdService()
    pubmeddataservice = PubMedDataService()
    pubmeddatawordcount = PubMedDataWordCount()
    max_p = 10
    
    # return pubMedID of N paper related to the searched term from db pubMed 
    pubMedIds=  pubmedidservice.getPubMedID(number, "+".join(terms))

    allAbstract = ""
    articleAbstractTermCountDict = {}
    allAuthors = []
    allYears = []
    allJournals = []

    #print(pubMedIds)
    
    fo_terms = "_".join(terms)
    # papers information
    fo_data = open("../file/pub_med_data_" + fo_terms + ".txt", "w")
    # papers keywords
    fo_keyword = open("../file/pub_med_data_keyword_"+ fo_terms + ".txt", "w")
    # word frequencies in abstracts
    fo_abstractTermCountDict = open("../file/pub_med_data_abstract_term_count_dict_"+ fo_terms + ".txt", "w")
    
    # fetch information for each paper from db pubMed
    for pubMedId in pubMedIds[1]:
        articleAbstract = ""

        pubmeddataservice.getPubMedData(pubMedId) 

        fo_data.write("PMID: " + pubMedId + "\n")

        articleTitle = pubmeddataservice.getPubMedArticleName()
        fo_data.write("Article Title: ")
        try:
            fo_data.write(articleTitle[2])
        except:
            pass
        fo_data.write("\n")

        authorList = pubmeddataservice.getPubMedAuthor()
        fo_data.write("Author:")
        try:
            for author in authorList[2]:
                try:
                    fo_data.write(" " + author)
                    allAuthors.append(author)
                except:
                    pass
        except:
            pass
        fo_data.write("\n")

        abstractList = pubmeddataservice.getPubMedAbstract()
  
        fo_data.write("Abstract:")
        #print(articleAbstract)
        #print(type(articleAbstract))

        try:
            articleAbstract= ""+abstractList[2]
            fo_data.write(articleAbstract)
            allAbstract = allAbstract + " " + articleAbstract
        except:
            pass
        

        fo_data.write("\n")

        keywordList = pubmeddataservice.getPubMedKeyword()
        fo_data.write("Keyword:")
        if keywordList[2] is not None:
            try:
                    for keyword in keywordList[2]:
                        try:
                            fo_data.write(keyword + ",")
                            fo_keyword.write(keyword + ",")
                        except:
                            pass
            except:
                pass
            fo_keyword.write("\n")
        fo_data.write("\n")
        


        journalName = pubmeddataservice.getPubMedJournalName()
        fo_data.write("Journal Name:")
        try:
            fo_data.write(journalName[2])
            allJournals.append(journalName[2])
        except:
            pass
        fo_data.write("\n")

        publishedYear = pubmeddataservice.getPubMedPublishedYear()
        fo_data.write("Published Year: ")
        try:
            fo_data.write(publishedYear[2])
            allYears.append(publishedYear[2])
        except:
            pass
        fo_data.write("\n")
        fo_data.write("--------------------\n")

        # count frequency of searched terms appeared in the abstract
        try:
            articleAbstractWordCount = pubmeddatawordcount.wordCount(articleAbstract)
        except:
            pass
        for term in terms:
            try:
                if articleTitle[2] not in articleAbstractTermCountDict:
                    articleAbstractTermCountDict[articleTitle[2]] = articleAbstractWordCount.get(term.lower()) if articleAbstractWordCount.get(term.lower()) else 0 
                else:
                    articleAbstractTermCountDict[articleTitle[2]] += articleAbstractWordCount.get(term.lower()) if articleAbstractWordCount.get(term.lower()) else 0 
            except:
                pass
    
    print("\n---Papers Information Stored---")
    print("\n---Papers Recommendation:---")
    # sort articles by frequency of searched terms in abstract, high to low
    articleAbstractTermCountDict_sorted = OrderedDict(sorted(articleAbstractTermCountDict.items(),  key=itemgetter(1), reverse=True))
    n_p = 0
    for k,v in articleAbstractTermCountDict_sorted.items():
        try:
            fo_abstractTermCountDict.write(k + " ")
            if n_p< max_p:
                print(str(n_p+1) + ": " + k)
                n_p +=1
            fo_abstractTermCountDict.write(str(v) + "\n")
        except:
            pass
  
    fo_data.close()
    fo_keyword.close()
    fo_abstractTermCountDict.close()



    # count word frequencies in all abstracts,  filter out stop words
    print("\n---Abstract Word Frequencies:---")
    AbstractWordCount = pubmeddatawordcount.wordCount(allAbstract)
    for term in terms:
        if(term.lower() in AbstractWordCount):
            del AbstractWordCount[term.lower()]
	
    fo_allAbstractWordCount = open("../file/pub_med_data_abstract_word_count_"+ fo_terms + ".txt", "w")
    n_p = 0
    for k,v in AbstractWordCount.items():
        fo_allAbstractWordCount.write(k + " ")
        fo_allAbstractWordCount.write(str(v) + "\n")
        if n_p< max_p:
            print(k + ": " + str(v))
            n_p +=1
    fo_allAbstractWordCount.close()
    

    # association analysis using Apriori algorithm,  mining association rules from frequent items set
    pubmeddataassociationrule = PubMedDataAssociationRule()
    inFile = pubmeddataassociationrule.dataFromFile("../file/pub_med_data_keyword_"+ fo_terms + ".txt")
    items, rules = pubmeddataassociationrule.runApriori(inFile)
    pubmeddataassociationrule.printResults(items, rules)
    
    
    # data visualization
    print("\n---Visulization (press Enter for next graph):---")
    input()
    pubmedvisual = PubMedVisual(terms)
    pubmedvisual.plotYear(allYears)
    pubmedvisual.plotJournal(allJournals)
    pubmedvisual.plotAuthor(allAuthors)
    pubmedvisual.plotWords(AbstractWordCount)
    #pubmedvisual.plotWC(AbstractWordCount)
    

if __name__ == "__main__": 
	main()
