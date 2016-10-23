import urllib
from collections import OrderedDict
from operator import itemgetter
import string


class PubMedDataWordCount(object):

    def __init__(self):
        punctuation = list(string.punctuation)
        self.stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
        self.stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
        self.stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
        self.stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
        self.stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
        self.stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
        self.stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
        self.stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
        self.stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
        self.stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
        self.stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
        self.stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
        self.stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
        self.stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
        self.stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
        self.stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
        self.stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
        self.stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
        self.stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
        self.stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
        self.stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
        self.stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
        self.stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
        self.stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
        self.stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
        self.stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
        self.stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
        self.stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
        self.stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
        self.stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
        self.stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
        self.stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
        self.stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
        self.stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
        self.stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
        self.stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
        self.stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
        self.stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
        self.stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
        self.stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
        self.stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
        self.stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
        self.stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
        self.stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
        self.stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
        self.stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
        self.stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
        self.stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
        self.stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
        self.stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
        self.stopwords += ['yours', 'yourself', 'yourselves']
        self.stopwords += ['0', '1', '2', '3', '4', '5', '6', '7','8','9','10']
        self.stopwords += ['a',    'b',    'c',    'd',    'e',    'f',    'g',    'h',    'i',    'j',    'k',    'l',    'm',    'n',    'o',    'p',    'q',    'r',    's',    't',    'u',    'v',    'w',    'x',    'y',    'z']
        self.stopwords += punctuation

    def wordCount(self, inputText):
        wordcount={}
        whiteSpaceRegex = "\\s";
        for word in inputText.replace(';',' ').replace(',',' ').replace('.',' ').replace(':',' ').replace('(',' ').replace(')',' ').replace("'",' ').split():      
            word = word.lower()
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
        wordcount_stop = {word:wordcount[word] for word in wordcount if word not in self.stopwords }
        wordcount_sorted = OrderedDict(sorted(wordcount_stop.items(),  key=itemgetter(1), reverse=True))
        return wordcount_sorted