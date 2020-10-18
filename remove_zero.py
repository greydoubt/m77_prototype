# basic script to remove rows with 0 as status

import pandas as pd

include_value = 200 # for removing anything but status 200
exclude_value = 0 # to remove just 0


df = pd.read_csv (r'output_alexa_base_url.csv')

indexNames = df[ df['status'] == exclude_value ].index
# Delete these row indexes from dataFrame
df.drop(indexNames , inplace=True)

output = 'output_alexa_base_url_nz.csv'
df.to_csv(output, encoding='utf-8', index=False)
