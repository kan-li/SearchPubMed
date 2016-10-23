# SearchPubMed

We access the PubMed via its public API Entrez Database. 
The searching procedure involve two steps. The user should first define a term/terms to search (e.g. Alzheimer’s disease), and the number of papers the followed analysis based (e.g. 200). The searching URL via the API for the example is 

*http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=200&sort=relevance&term=Alzheimers+disease*

The query will return a JSON string which contains 200 (may less) PubMed IDs corresponding to the top matches of our query. The second step is to get some more details about these articles using the efetch utility, which takes one or more PubMed IDs as input.  The fetch operation can be built as follows,

*http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=ID1,ID2,...*

This step will return XML data format for each citation. The returned data will be parsed using certain XML library and extracted information such as title, authors, journal, year, abstract and keywords set. All the information will output to a text file with decent format.

We can summarize and visualize the information to answer following questions: <br>
1. Is the topic hot? <br>
2. Who is the most productive author in the area? <br>
3. What are they talking about when they talk about this topic? <br>
4. Which paper should I read first? <br>
5. Which journal should I target? 


