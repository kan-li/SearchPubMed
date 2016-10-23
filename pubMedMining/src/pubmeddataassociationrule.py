import sys

from itertools import chain, combinations
from collections import defaultdict, OrderedDict
from optparse import OptionParser


class PubMedDataAssociationRule(object):
    
    def __init__(self):
        self.minSupport = 0.2
        self.minConfidence = 0.3
        
    def subsets(self,arr):
        """ Returns non empty subsets of arr"""
        return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


    def returnItemsWithMinSupport(self,itemSet, transactionList, minSupport, freqSet):
        """calculates the support for items in the itemSet and returns a subset
        of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in list(localSet.items()):
                support = float(count)/len(transactionList)

                if support >= self.minSupport:
                        _itemSet.add(item)

        return _itemSet
    
    
    def joinSet(self,itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
    
    
    def getItemSetTransactionList(self, data_iterator):
        transactionList = list()
        itemSet = set()
        for record in data_iterator:
            transaction = frozenset(record)
            transactionList.append(transaction)
            for item in transaction:
                itemSet.add(frozenset([item]))              # Generate 1-itemSets
        return itemSet, transactionList
    
    
    def runApriori(self,data_iter):
        """
        run the apriori algorithm. data_iter is a record iterator
        Return both:
         - items (tuple, support)
         - rules ((pretuple, posttuple), confidence)
        """
        itemSet, transactionList = self.getItemSetTransactionList(data_iter)
    
        freqSet = defaultdict(int)
        largeSet = dict()
        # Global dictionary which stores (key=n-itemSets,value=support)
        # which satisfy minSupport
    
        assocRules = dict()
        # Dictionary which stores Association Rules
    
        oneCSet = self.returnItemsWithMinSupport(itemSet,
                                            transactionList,
                                            self.minSupport,
                                            freqSet)
    
        currentLSet = oneCSet
        k = 2
        while(currentLSet != set([])):
            largeSet[k-1] = currentLSet
            currentLSet = self.joinSet(currentLSet, k)
            currentCSet = self.returnItemsWithMinSupport(currentLSet,
                                                    transactionList,
                                                    self.minSupport,
                                                    freqSet)
            currentLSet = currentCSet
            k = k + 1
        
        def getSupport(item):
                """local function which Returns the support of an item"""
                return float(freqSet[item])/len(transactionList)
    
        toRetItems = []
        for key, value in list(largeSet.items()):
            toRetItems.extend([(tuple(item), getSupport(item))
                               for item in value])
    
        toRetRules = []
        for key, value in list(largeSet.items())[1:]:
            for item in value:
                _subsets = list(map(frozenset, [x for x in self.subsets(item)]))
                for element in _subsets:
                    remain = item.difference(element)
                    if len(remain) > 0:
                        confidence = getSupport(item)/getSupport(element)
                        if confidence >= self.minConfidence:
                            toRetRules.append(((tuple(element), tuple(remain)),
                                               confidence))
        return toRetItems, toRetRules
    
    
    def printResults(self,items, rules):
        print("\n ---Keywords sets sorted by support---:")
        """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
        for item, support in sorted(items, key=lambda item_support: item_support[1], reverse=True):
            print("item: %s , %.3f" % (str(item), support))
        print("\n---Confidence rules sorted by confidence---:")
        for rule, confidence in sorted(rules, key=lambda rule_confidence: rule_confidence[1], reverse=True):
            pre, post = rule
            print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
            
            
    def dataFromFile(self,fname):
        """Function which reads from the file and yields a generator"""
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')                         # Remove trailing comma
                record = frozenset(line.split(','))
                yield record
