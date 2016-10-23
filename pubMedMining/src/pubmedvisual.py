import pandas as pd
import numpy as np
import rpy2.robjects as robj
import rpy2.robjects.pandas2ri # for dataframe conversion
from rpy2.robjects.packages import importr
from rpy2.robjects.lib import grid
from rpy2.robjects.lib import ggplot2
from collections import OrderedDict
from operator import itemgetter

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re


class PubMedVisual(object):
    def __init__(self, terms):
        self.fo_terms = "_".join(terms)
        print(self.fo_terms)

    def plotYear(self, allYears):
        year_series = pd.Series(allYears)
        counts = year_series.value_counts()
        years = dict(counts)
        #print(list(years.keys()))
        #print(list(years.values()))
        data = pd.DataFrame( {'Years':list(years.keys()), 'Number':list(years.values())} )
        gr = importr('grDevices')
        gr.png(file='../file/yearplot_'+ self.fo_terms +'.png', width=800, height=800)
        robj.pandas2ri.activate()
        data_R = robj.conversion.py2ri(data)
        year_plot = ggplot2.ggplot(data_R) + ggplot2.aes_string(x = 'Years', y= 'Number', group=1) + ggplot2.geom_line()
        year_plot.plot()
        input()
        gr.dev_off()
        
    def plotJournal(self, allJournals):
        threshold = 3
        journal_series = pd.Series(allJournals)
        counts = journal_series.value_counts()
        output = dict(counts)
        output = {k:output[k] for k in output if output[k]>=threshold}
        data = pd.DataFrame( {'Journals':list(output.keys()), 'Frequency':list(output.values())} )
        gr = importr('grDevices')
        gr.png(file='../file/journalplot_'+ self.fo_terms +'.png', width=800, height=800)
        robj.pandas2ri.activate()
        data_R = robj.conversion.py2ri(data)
        journal_plot = ggplot2.ggplot(data_R) + ggplot2.aes_string(x = 'Journals', y= 'Frequency') + ggplot2.geom_bar(stat = "identity", width=0.8) + ggplot2.coord_flip()
        journal_plot.plot()
        input()
        
        gr.dev_off()
        
    def plotAuthor(self, allAuthors):
        threshold = 3
        author_series = pd.Series(allAuthors)
        counts = author_series.value_counts()
        output = dict(counts)
        output = {k:output[k] for k in output if output[k]>=threshold}
        data = pd.DataFrame( {'Authors':list(output.keys()), 'Frequency':list(output.values())} )
        gr = importr('grDevices')
        gr.png(file='../file/authorplot_'+self.fo_terms+'.png', width=800, height=600)
        robj.pandas2ri.activate()
        data_R = robj.conversion.py2ri(data)
        author_plot = ggplot2.ggplot(data_R) + ggplot2.aes_string(x = 'Authors', y= 'Frequency') + ggplot2.geom_bar(stat = "identity", width=0.8) + ggplot2.coord_flip()  
        author_plot.plot()
        input()
        gr.dev_off()
        
    def plotWords(self, wordcounts):
        threshold = 25
        wordcounts2 = {k:wordcounts[k] for k in wordcounts if wordcounts[k]>=threshold}
        data = pd.DataFrame( {'Word':list(wordcounts2.keys()), 'Frequency':list(wordcounts2.values())} )
        data = data.sort_values(by = 'Frequency', ascending=False)
        #print(data)
        gr = importr('grDevices')
        gr.png(file='../file/wordsplot_'+self.fo_terms+'.png', width=1000, height=1200)
        robj.pandas2ri.activate()
        data_R = robj.conversion.py2ri(data)
        words_plot = ggplot2.ggplot(data_R) + ggplot2.aes_string(x = 'Word', y= 'Frequency') + ggplot2.geom_bar(stat = "identity", width=0.8) + ggplot2.coord_flip()
        words_plot.plot()
        input()
        gr.dev_off()
        
        wordcloud = WordCloud(background_color='white',
                      width=1800,
                      height=1400).generate_from_frequencies(wordcounts.items())
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('../file/wordcloud_'+self.fo_terms+'.png', dpi=600)
        plt.show()
        input()
   

  
