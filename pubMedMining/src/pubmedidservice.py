import urllib
import json

class PubMedIdService(object):


    def __init__(self):
        self.PubMedIDServiceURLPrefix1 = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax="
        self.PubMedIDServiceURLPrefix2 = "&sort=relevance&term="
        self.pubMedIDServiceURL = ""
    
    def getPubMedID(self, numberOfPubMed, term):
        try:
            pubMedIDServiceURL = self.PubMedIDServiceURLPrefix1 + numberOfPubMed + self.PubMedIDServiceURLPrefix2 + term
            with urllib.request.urlopen(pubMedIDServiceURL)as f:
                response = f.read()
                jsondata = json.loads(response.decode('utf-8'))
            if jsondata["esearchresult"] is not None:
                PubMedIDs = (term, jsondata["esearchresult"]["idlist"])
            else:
                PubMedIDs = (term, None)
            return PubMedIDs
        except urllib.error.URLError:
             return "Network Failure"


    # def setLocationServiceURL(self, url):
    #     self.locationServiceURL = url

