# sean.mcwillie@nist.gov
# purpose: given a dataset with url(s), generate a feature vector that summarizes core syntax of the URL
# can inherit from other vectors (ie one based on document-level features)

import math # for calculating entropy
import socket
import pandas as pd
import tldextract

output = 'output.csv'

filename = 'pt5000.csv'


inputdf = pd.read_csv(filename)  



# pre-production version




# functions

# Feature 1 - Count periods in URL
def countPeriods(url):
  result = url.count('.')
  return result

# Feature 2 - URL contains @ or -
def flagSpecialSymbols(url):
  return ("@" in url) or ("-" in url)


# Feature 3 - Length of URL >= 74
def obtainLength(url):
  return len(url)


# entropy
def shannonEntropy(url):
  string = url.strip()
  
  prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]

  entropy = sum([(p * math.log(p) / math.log(2.0)) for p in prob])

  #l = float(len(s))
  #return -sum(map(lambda a: (a/l)*math.log2(a/l), Counter(s).values()))


  return entropy



def numDigits(url):
  digits = [i for i in url if i.isdigit()]
  return len(digits)

def numParameters(url):
  params = url.split('&')
  return len(params) - 1

def numQueries(url):
  params = url.split('?')
  return len(params) - 1

def numAnchors(url):
  fragments = url.split('#')
  return len(fragments) - 1

def hasHttp(url):
  return 'http:' in url

def hasHttps(url):
  return 'https:' in url

# get host ip
def get_ip(url):

  url2=url
  if url[0:5] == 'https':
    url2 = url[8:]
  elif url[0:4] == 'http':
    url2 = url[7:]

  try:
    temp = socket.gethostbyname(url2)
  except:
    temp = 0

  return temp





# lists
# feature 1
base_num_periods_list = []
full_num_periods_list = []

# feature 2
base_spec_symbols_list = []
full_spec_symbols_list = []

# feature 3
base_length_list = []
full_length_list = []

ip_list = []

full_anchors_list = []
base_anchors_list = []

full_params_list = []
base_params_list = []

full_queries_list = []
base_queries_list = []

full_digits_list = []
base_digits_list = []

full_entropy_list = []
base_entropy_list = []

## # main loop

for index, row in inputdf.iterrows():
  print('processing ' + row['url'])

  # feature 1
  full_num_periods_list.append(countPeriods(row['url']))
  base_num_periods_list.append(countPeriods(row['base_url']))

  # feature 2
  full_spec_symbols_list.append(flagSpecialSymbols(row['url']))
  base_spec_symbols_list.append(flagSpecialSymbols(row['base_url']))

  # feature 3
  full_length_list.append(obtainLength(row['url']))
  base_length_list.append(obtainLength(row['base_url']))

  ip_list.append(get_ip(row['base_url']))

  full_anchors_list.append(numAnchors(row['url']))
  base_anchors_list.append(numAnchors(row['base_url']))

  full_params_list.append(numParameters(row['url']))
  base_params_list.append(numParameters(row['url']))

  full_queries_list.append(numQueries(row['url']))
  base_queries_list.append(numQueries(row['url']))

  full_digits_list.append(numDigits(row['url']))
  base_digits_list.append(numDigits(row['base_url']))

  full_entropy_list.append(shannonEntropy(row['url']))
  base_entropy_list.append(shannonEntropy(row['base_url']))



# tie lists to features

inputdf['base_num_periods'] = base_num_periods_list
inputdf['full_num_periods'] = full_num_periods_list

inputdf['base_spec_symbols'] = base_spec_symbols_list
inputdf['full_spec_symbols'] = full_spec_symbols_list

inputdf['base_length'] = base_length_list
inputdf['full_length'] = full_length_list

inputdf['ip_list'] = ip_list

inputdf['full_anchors'] = full_anchors_list
inputdf['base_anchors'] = base_anchors_list

inputdf['full_params'] = full_params_list
inputdf['base_params'] = base_params_list

inputdf['full_queries'] = full_queries_list
inputdf['base_queries'] = base_queries_list

inputdf['full_digits'] = full_digits_list
inputdf['base_digits'] = base_digits_list

inputdf['full_entropy'] = full_entropy_list
inputdf['base_entropy'] = base_entropy_list


inputdf.to_csv(output, encoding='utf-8', index=False)