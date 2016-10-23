import urllib
import xmltodict
import xml.etree.ElementTree as ET


class PubMedDataService(object):


    def __init__(self):
        self.PubMedDataServiceURLPrefix = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="
        self.pubMedDataServiceURL = ""

    def getPubMedData(self, pubMedId):
        self.pubMedId = pubMedId
        try:
            pubMedDataServiceURL = self.PubMedDataServiceURLPrefix + pubMedId
            with urllib.request.urlopen(pubMedDataServiceURL)as f:
                response = f.read()
                self.xmldata = xmltodict.parse(response.decode('utf-8'))
        except urllib.error.URLError:
            return "Network Failure"

    def getPubMedAuthor(self):
        try:
            authorList = self.xmldata['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['AuthorList']['Author']
            authorArray = []
            for author in authorList:
                authorArray.append(author['LastName'] + "," + author['ForeName'])
            return (self.pubMedId, "Author", authorArray)
        except:
            return (self.pubMedId, "Author", None)

    def getPubMedAbstract(self):
        try:
            abstractList = self.xmldata['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['Abstract']['AbstractText']
            abstractString = ""
            isString = True
            if '#text' in abstractList:
                abstractString = abstractString + " " + abstractList['#text']
                isString = False
            else:
                for abstract in abstractList:
                    if '#text' in abstract:
                        isString = False
                        abstractString = abstractString + " " + abstract['#text']
            if isString:
                abstractString = abstractList       
            return (self.pubMedId, "Abstract", abstractString)
        except:
            return (self.pubMedId, "Abstract", None)

    def getPubMedKeyword(self):
        try:
            keywordList = self.xmldata['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['KeywordList']['Keyword']
            keywordArray = []
            for keyword in keywordList:
                if '#text' in keyword:
                    keywordArray.append(keyword['#text'])
                else: 
                    keywordArray.append(keyword)
            return (self.pubMedId, "Keyword", keywordArray)
        except:
            return (self.pubMedId, "Keyword", None)

    def getPubMedPublishedYear(self):
        try:
            publishedYear = self.xmldata['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']["Journal"]['JournalIssue']['PubDate']['Year']
            return (self.pubMedId, "Published Year", publishedYear)
        except:
            return (self.pubMedId, "Published Year", None)

    def getPubMedJournalName(self):
        try:
            journalName = self.xmldata['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']["Journal"]['Title']
            return (self.pubMedId, "Journal Name", journalName)
        except:
            return (self.pubMedId, "Journal Name", None)

    def getPubMedArticleName(self):
        try:
            articleTitle = self.xmldata['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']["ArticleTitle"]
            return (self.pubMedId, "Article Name", articleTitle)
        except:
            return (self.pubMedId, "Article Name", None)

    def setWeatherServiceURL(self, url):
        self.weatherServiceURLPrefix = url
