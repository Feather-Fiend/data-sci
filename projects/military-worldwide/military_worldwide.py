{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"pygments_lexer":"ipython3","nbconvert_exporter":"python","version":"3.6.4","file_extension":".py","codemirror_mode":{"name":"ipython","version":3},"name":"python","mimetype":"text/x-python"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-31T22:00:59.628817Z\",\"iopub.execute_input\":\"2021-05-31T22:00:59.629082Z\",\"iopub.status.idle\":\"2021-05-31T22:00:59.644693Z\",\"shell.execute_reply.started\":\"2021-05-31T22:00:59.629059Z\",\"shell.execute_reply\":\"2021-05-31T22:00:59.643889Z\"}}\n# This Python 3 environment comes with many helpful analytics libraries installed\n# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python\n# For example, here's several helpful packages to load\n\nimport numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\n\n# Input data files are available in the read-only \"../input/\" directory\n# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory\n\nimport os\nfor dirname, _, filenames in os.walk('/kaggle/input'):\n    for filename in filenames:\n        print(os.path.join(dirname, filename))\n\n# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using \"Save & Run All\" \n# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-31T22:01:05.979672Z\",\"iopub.execute_input\":\"2021-05-31T22:01:05.979998Z\",\"iopub.status.idle\":\"2021-05-31T22:01:13.470508Z\",\"shell.execute_reply.started\":\"2021-05-31T22:01:05.979969Z\",\"shell.execute_reply\":\"2021-05-31T22:01:13.469407Z\"}}\n!pip install openpyxl #supports pd.read_excel and .xlsx format\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-31T23:02:38.143329Z\",\"iopub.execute_input\":\"2021-05-31T23:02:38.143596Z\",\"iopub.status.idle\":\"2021-05-31T23:02:38.204234Z\",\"shell.execute_reply.started\":\"2021-05-31T23:02:38.143573Z\",\"shell.execute_reply\":\"2021-05-31T23:02:38.203304Z\"}}\nmilitary_filepath = \"../input/military-presence-worldwide/Military Data .xlsx\"\nmilitary_data = pd.read_excel (military_filepath)\nmilitary_data['Country '] = military_data['Country '].str.strip() #remove trailing whitespace\ndel military_data['Unnamed: 7'] #some spurious column to be removed\ndisplay(military_data.head())\nprint(\"Number of countries:\", military_data.shape[0])\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-31T23:03:42.842630Z\",\"iopub.execute_input\":\"2021-05-31T23:03:42.842994Z\",\"iopub.status.idle\":\"2021-05-31T23:03:42.859814Z\",\"shell.execute_reply.started\":\"2021-05-31T23:03:42.842970Z\",\"shell.execute_reply\":\"2021-05-31T23:03:42.858721Z\"}}\nlargest_total = military_data.sort_values(by='Total', ascending=False).reset_index()\nlargest_active = military_data.sort_values(by='Active military', ascending=False).reset_index()\n\ndisplay(largest_total.columns) #notice that Country has a space!\ndisplay(largest_total.loc[:5, ['Country ', 'Total']])\ndisplay(largest_active.loc[:5, ['Country ','Active military']])\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-31T23:03:45.919180Z\",\"iopub.execute_input\":\"2021-05-31T23:03:45.919466Z\",\"iopub.status.idle\":\"2021-05-31T23:03:45.928749Z\",\"shell.execute_reply.started\":\"2021-05-31T23:03:45.919443Z\",\"shell.execute_reply\":\"2021-05-31T23:03:45.927312Z\"}}\n#data originated from https://www.nationsonline.org/oneworld/countries_of_the_world.htm\n#1) data was placed in country_list.txt\n#2) country_list.txt was parsed by country_region_parser.py \n#3) output was stored (\"pickled\") in country-region_list.txt\nimport pickle\n\nwith open ('../input/countryregion-list/country-region_list.txt', 'rb') as f:\n    country_region_pairs = pickle.load(f)\nprint(country_region_pairs[:5])\ncountry_region_dict = dict(country_region_pairs)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-05-31T23:03:48.176202Z\",\"iopub.execute_input\":\"2021-05-31T23:03:48.176594Z\",\"iopub.status.idle\":\"2021-05-31T23:03:48.221534Z\",\"shell.execute_reply.started\":\"2021-05-31T23:03:48.176571Z\",\"shell.execute_reply\":\"2021-05-31T23:03:48.220350Z\"}}\n\nregions = []\nmissing = []\nmissed_country = ['The Bahamas', 'Kingdom of Belgium', 'Brunei', \"People's Republic of China\",\n                  'Democratic Republic of the Congo', 'Republic of Fiji', 'Iran',\n                  'Republic of Kosovo', 'Laos', 'Moldova', 'Myanmar', 'North Korea',\n                  'Kingdom of Norway', 'State of Palestine', 'Macedonia',\n                  'Republic of the Congo', 'Russia', 'Republic of Singapore', 'Slovakia',\n                  'Republic of South Africa', 'South Korea', 'Kingdom of Spain', 'Syria',\n                  'Taiwan', 'Tanzania', 'East Timor',\n                  'United Kingdom of Great Britain and Northern Ireland',\n                  'United States of America'] \n#determined 'after the fact' (by running below once and finding names of the same countries don't match)\n\nmissed_region = ['Caribbean', 'Western Europe', 'Southeast Asia', 'Eastern Asia',\n                'Central Africa', 'Melanesia, Oceania', 'South-Central Asia',\n                'Southern Europe', 'South-East Asia', 'Eastern Europe', 'Southeast Asia', 'Eastern Asia',\n                'Northern Europe', 'Middle East, Western Asia', 'Southern Europe',\n                'Central Africa', 'Eastern Europe - Northern Asia', 'Southeast Asia', 'Eastern Europe',\n                'Southern Africa', 'Eastern Asia', 'Southern Europe', 'Middle East, Western Asia',\n                'Eastern Asia', 'Eastern Africa', 'South-East Asia', \n                'Northern Europe',\n                 'North America'] \n#these were determined manually by either noticing the difference in spelling of the same countries\n#(and hence copying the region from the output of country-region_parser.py OR\n#inferring the region from neighboring countries mentioned in output of country-region_parser.py)\n\nmissed_country_region_pairs = zip(missed_country, missed_region)\nmissed_country_region_dict = dict(missed_country_region_pairs)\n\nfor index, row in military_data.iterrows(): \n    #print(\"Total income in \"+ row[\"Date\"]+ \" is:\"+str(row[\"Income_1\"]+row[\"Income_2\"]))\n    if row['Country '] in country_region_dict:\n        regions.append(country_region_dict[row['Country ']])\n    elif row['Country '] in missed_country_region_dict:\n        regions.append(missed_country_region_dict[row['Country ']])\n    else:\n        missing.append(row['Country '])\n        \nprint(\"Number of matches:\", len(regions))\nprint(\"Number of misses:\", len(missing)) #0, as expected after correcting for it by creating missed_country_region_dict\nprint(missing) #empty, as expected\n\nmilitary_data['Region'] = regions\ndisplay(military_data)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2021-06-01T00:23:04.559028Z\",\"iopub.execute_input\":\"2021-06-01T00:23:04.559437Z\",\"iopub.status.idle\":\"2021-06-01T00:23:05.564087Z\",\"shell.execute_reply.started\":\"2021-06-01T00:23:04.559405Z\",\"shell.execute_reply\":\"2021-06-01T00:23:05.563188Z\"}}\nimport seaborn as sns\nimport matplotlib.pyplot as plt\n\nmilitary_region_data = military_data.groupby('Region')\ndisplay(military_region_data.Region.count().iloc[:5])\nsns.kdeplot(data=military_data['Active military'], shade=True)\n\n#military_presence = military_region_data['Active military'].sum()\nmilitary_presence = military_region_data['Active military'].agg([sum]).reset_index() #allows Region to become its own column\n                                                                                     #(not the index (which isn't a column by default) anymore)\nmilitary_presence.columns = [\n  'Region',\n  'Total active'\n]\n#display(military_presence)\nmilitary_presence.shape\nplt.figure(figsize=(20,6)) #how many active military personnel in a region?\nplt.title(\"Combined size of military forces in a region\")\nmp = sns.barplot(x=military_presence['Region'], y=military_presence['Total active'])\nfor item in mp.get_xticklabels():\n    item.set_rotation(90)\nplt.ylabel(\"Total size\")","metadata":{"_uuid":"2d270fd8-27f2-4fe9-ae55-eff1bbedc767","_cell_guid":"c23f761f-d7b0-4b5c-8a40-86ca9811deca","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}