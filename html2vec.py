#import urllib
from bs4 import BeautifulSoup


import pandas as pd

# need TLD info for seeing if src/href are external domains
import tldextract


# notes
# 3 Oct - add document-level features to vector

################
# pre-processing steps:


df = pd.read_csv (r'output_alexa_base_url_nz.csv') # html_alexa_A_base_url


global_flag = 0 # boolean: 0 if benign, 1 if phishing
global_dataset = "unspecified" # "alexa", this is optional but strongly recommended
global_batch = "unspecified" # "B2" # to dismabiguate multiple batches/scrapes B/F for Base/Full URL



# all 'url' values are assumed to be full urls
# shorten to base url for new column
# copy 'url' to 'full_url'
# later on can write sub script to detect base vs full
# need to generate 'base_url' to compare links/images


# features and functions



#extest = tldextract.extract(comp_url)
#print(extest.suffix == '')


def url_comparator(main_url, comp_url):



  temp_url = tldextract.extract(comp_url)
  print(temp_url.domain +'.'+ temp_url.suffix)

  if(temp_url.suffix == ''):
    print('local/relative url, skip')
    return 0
  elif((main_url).lower() == (temp_url.domain +'.'+ temp_url.suffix).lower()):
    print('its ok')
    return 0
  else:
    print('external link')
    return 1

# sample use for comparator:
##host_url = tldextract.extract(df.loc[2,'url'])
#print(host_url.domain +'.'+ host_url.suffix)

#comp_url = '/ermgs/img.png'
#main_url = host_url.domain +'.'+ host_url.suffix

#url_comparator(main_url, comp_url)







########
xml_doc_length_list = []
xml_style_length_list = []
xml_script_length_list = []
xml_body_length_list = []

# number of special chars (nonalpha, nonnumeric)
# word 'copyright' is present or not

# ratios
# script to body
xml_scriptbody_ratio = []
# script to special chars

xml_num_titles_list = []

xml_num_links_list = []
xml_num_links_empty_list = []
xml_num_links_ext_list = []

xml_num_img_list = []
xml_num_img_ext_list = []

xml_body_entropy_list = []
base_doc_entropy_list = []


############
header_list = ['url', # in original dataset
'flag', # in original dataset, hardcoded in preproc
'dataset', # hardcoded in preproc
'batch', # hardcoded in preproc
'full_url',
'base_url',
'status', # inherited from scrape
'xml', # inherited from scrape
'datetime', # inherited from scrape
# derived in this script
'xml_doc_length',
'xml_script_length',
'xml_style_length',
'xml_body_length',
'xml_scriptbody_ratio',
'xml_num_titles'
# link-based features

# other features / topic analysis (reserved)
]


#############



# Get Stats function
# First order:
# string length of text, scripts, styles, whole doc
# Second order:
# image src, a href count
# of these tags, which refer to an external domain




#print (df.loc[0,'xml'])

# original csv:
# url,status,xml,datetime


# new csv:
# url*, status, datetime
# numerical features


# test page:
print("Loading test page:")
print((df.loc[0,'url']))
print(type(df.loc[0,'xml']))

# get column names
print(df.columns)



# create lists for new features that get extracted


print("Main loop:")

## main script here
for index, row in df.iterrows():

  print("\n\nProcessing: ") #remove
  print(row['url']) #remove
  
  html = row['xml']

  soup = BeautifulSoup(html, 'html.parser')

  style_raw = soup(["style"])

  script_raw = soup(["script"])

  for script in soup(["script", "style"]):
    script.extract()    # rip it out
  # end of loop


  # user-facing content
  text = soup.get_text()

  lines = (line.strip() for line in text.splitlines())
  # break multi-headlines into a line each
  
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
  # drop blank lines
  
  text = '\n'.join(chunk for chunk in chunks if chunk)


  ### subprocess A: get lengths of body, style, script


  print("\n\nLengths:")

  # style_uni = style_uni.join(u'\n',map(style_uni,style_length))

  #print(type(text))

  print("\nLength of main text:")
  body_length = len(text)

  print(body_length)

  

  style_length = 0
  for line in style_raw:
    #get str value from each line,replace charset with utf-8 or other charset you need
    style_length += len(str(line))
    #print( line)

  print("\nLength of style tags:")
  print(style_length)    



  script_length = 0
  for line in script_raw:
    #get str value from each line,replace charset with utf-8 or other charset you need
    script_length += len(str(line))
    #print( line)

  print("\nLength of script tags:")
  print(script_length)    


  ## APPEND TO LIST
  xml_doc_length_list.append(script_length+style_length+body_length)
  xml_script_length_list.append(script_length)
  xml_style_length_list.append(style_length)
  xml_body_length_list.append(body_length)

  xml_scriptbody_ratio.append(script_length/body_length)

# ratios:


## APPEND TO LIST





  ### 

  ### subprocess B: calculate ratios

  ### sub C: count features -- img src, a href, title

  titles = soup.findAll('title')

  for title in titles: # can remove
    print(title.string) # can remove

  print(len(titles)) # can remove

  xml_num_titles_list.append(len(titles))



  ### sub D: compare tags -- url is local, null, same site, or external site













# once loop has ended, turn lists into new columns






#print(soup(["script", "style"]))



# kill all script and style elements


# get text


#print(type(text))

# break into lines and remove leading and trailing space on each



print('\n\n\n\n')
#print(text)

# feature basket to extract:

# plain text (user-facing context)
# length of plain text
# scripts 
# css
# img tags
# a href tags
# count of external vs internal (base domain matches url feature)
# if css is hosted externally
# title (not for feature vector)
# favicon
# copyright info





# get content of img src and href tags
# compare to base domain

# https://stackoverflow.com/questions/43982002/extract-src-attribute-from-img-tag-using-beautifulsoup



###############
# subsection: a href and img src tag analysis

# dummy HTML "page" for testing
htmlText = """<title>title1</title><a href="http://google.com"><img src="https://src1.com/imgs/img.png">test</a> <title>title2</title><img src="https://src3.com/" /> """


soup = BeautifulSoup(htmlText, 'html.parser')

images = soup.findAll('img')

links = soup.findAll('a')


# <title>HTML Elements Reference</title>




print("\n\nimg tag src: ")
for image in images:

  # compare and count
    print(image['src'])
print(len(images))


# add in: if a href is an empty string

print("\na href tag src: ")



for link in links:


  print(link['href'])


print(len(links))



##### end subsection 


## close out program

# save as new csv with xml dropped (save space)

df['flag'] = global_flag
df['dataset'] = global_dataset
df['batch'] = global_batch


df['xml_doc_length'] = xml_doc_length_list
df['xml_script_length'] = xml_script_length_list
df['xml_style_length'] = xml_style_length_list
df['xml_body_length'] = xml_body_length_list

df['xml_scriptbody_ratio'] = xml_scriptbody_ratio


df['xml_num_titles'] = xml_num_titles_list

#global_flag = 0 # 0 if alexa, 1 if pt
#global_dataset = "alexa"
#global_batch =



# merge lists with features



# save HTML version

output = 'output.csv'
df.to_csv(output, encoding='utf-8', index=False)

# save no HTML version (smaller)
df_trim = df.drop('xml', 1)
output = 'output_trim.csv'
df_trim.to_csv(output, encoding='utf-8', index=False)
