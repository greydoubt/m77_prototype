# sean.mcwillie@nist.gov
# purpose: given a list of host names, query google to find a "canonical" fully formed URL
# in this version, the canonical URL is a log-in page


# known issues: 
# google wont return search results for google.com
# too many/too fast queries, can lead to block -- do not use on all 1 million Alexa sites without proper intervals
# suggestion from google engineer: "use Bing"

try: 
  from bs4 import BeautifulSoup
  from googlesearch import search  
  import pandas
except ImportError:  
  print("module not found") 
  

def gSearch(base_url, topic = "login"):

  polite_pause = 60
  query = " ".join(["site:"+base_url, base_url, topic]) 

  results_list = []

  for result in search(query, tld="com", num=1, stop=1, pause=polite_pause, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"): 
    results_list.append(result) 
    return results_list[0]


# basedomain = "microsoft.com"
#sample_url = gSearch(basedomain)
#print(sample_url)


# load csv into list, generate list of scraped search results, then save as a new csv

filename = 'justalexa.csv'
inputdf = pandas.read_csv(filename)


header_list = ['url', # in original dataset
'flag', # in original dataset
'full_url' # target result
]

full_urls_list = []

url_count = 0

for index, row in inputdf.iterrows():

  url_extract = row['url']
  print("try " + str(url_count) + ": " + url_extract)
  url_count += 1

  top_result = gSearch(url_extract)

  # diagnostic:
  print(top_result)


  full_urls_list.append(top_result)

inputdf['full_url'] = full_urls_list

output = 'output.csv'
inputdf.to_csv(output, encoding='utf-8', index=False)
