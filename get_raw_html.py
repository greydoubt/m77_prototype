# sean.mcwillie@nist.gov
# purpose: given a dataset of URLs, attempt to retrieve the content at that address
# does not do encoding or file type checks (ie, can download and add a .zip file)
# post-process to drop error codes as relevant


import pandas as pd
import datetime
import requests
import random
import time

# given a URL, attempt to retrieve the XML file 
def fetchXML(url):
  headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# in case the dataset lacks protocol, attach http in front
  if url[0:7] != "http://" and url[0:8] != "https://":
      url = "http://"+url
  
  try:
    r = requests.get(url, headers=headers, timeout=10)
  except:
    print("failure: " + url)
    return 0, None

  if r.status_code != 200:
    status = r.status_code
    xml = r.content
    print("Irregular status code")

  else:
    status = 200
    time.sleep(10)
    xml = r.content
  
  return status, xml


def parser(inputdf, urls_list, fails_list, tries):

  for url in urls_list:
    print("trying: ", url)

    temp_status, temp_xml = fetchXML(url)
  
    if temp_status == 200 or tries == 3:
      
      new_row = {'full_url':url, 'status':temp_status, 'xml':temp_xml,'datetime':datetime.datetime.now()}
      inputdf = inputdf.append(new_row, ignore_index=True)
  

    else: 
      fails_list.append(url)
    
  return inputdf


  
def main():

# append URL-XML pair to dataframe
# This makes a new dataframe (linear)
  df1 = pd.DataFrame(columns = ['full_url', 'status','xml','datetime']) 
  df2 = pd.DataFrame(columns = ['full_url', 'status','xml','datetime']) 
  df3 = pd.DataFrame(columns = ['full_url', 'status','xml','datetime']) 
  
  filename = 'justalexa.csv'


  inputdf = pd.read_csv(filename, usecols=['full_url'])  

  urls_list = inputdf['full_url'].values.tolist()



  fails_list = []
  fails_list2 = []

  df1 = parser(df1, urls_list, fails_list, 1)
  df1.to_csv('output_temp.csv', encoding='utf-8', index=False)
  # this saves the first wave
  
  df2 = parser(df2, fails_list, fails_list2, 2)

  df3 = parser(df3, fails_list2, fails_list2, 3)

  frames = [df1, df2, df3]
  resultdf = pd.concat(frames)
  #print(type(result))

  output = 'outputxml.csv'

  resultdf.to_csv(output, encoding='utf-8', index=False)

  print("failed:")
  print(fails_list)




if __name__ == "__main__":
    main()

