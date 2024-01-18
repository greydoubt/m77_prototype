# HTML2Vec
Converts list of URLs to salient features for ML tasks

# THIS LIBRARY WILL DOWNLOAD THE ENTIRE INTERNET. IT CAN GET YOU BANNED, ARRESTED, DEPORTED, ETC

Files/Pipeline

Raw dataset -- pull CSV file from Alexa (kaggle dataset), Phishtank, etc

google_canonical_result.py -- Takes a list of URLs (host names) and finds a canonical full URL to associate with that host. Not supported or endorsed by Google nor is Google endorsed. Secondary purpose is to drop suspicious URLs from datasets. Necessary if dataset consists only of host names.

get_raw_html.py -- takes list of URLs and attempts to download the HTML file. Stores as CSV. Large file warning. Records all status codes and failures. 

remove_zero.py -- utility script to drop failed connections from dataset. Can be skipped if NAs are needed in dataset.

html2vec.py -- takes CSV with HTML, generates summary features. Saves two CSVs, one that still contains the original HTML, and one that is trimmed. 
Features: document length, script length, style length, body length, script-to-body, number of title tags. 

url_preproc.py --  given a dataset with url(s), generate a feature vector that summarizes core syntax of the URL. Inherits from html-level feature vector. Generates features based on host name (base url) and full url. 
Features: number of periods, presence of special symbols (@, -),  URL length, IP address (if site responded), number of anchors (#), number of URL parameters, number of queries, number of digits, Shannon Entropy score.

jupyter notebook with examples 

Aggregate feature set as of 14 Oct 2020: 
url, status, datetime, flag, dataset, batch, xml_doc_length, xml_script_length, xml_style_length, xml_body_length, xml_scriptbody_ratio, xml_num_titles, base_url, base_num_periods, full_num_periods, base_spec_symbols, full_spec_symbols, base_length, full_length, ip, full_anchors,base_anchors, full_params, base_params, full_queries, base_queries, full_digits, base_digits, full_entropy, base_entropy
