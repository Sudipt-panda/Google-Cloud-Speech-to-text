import sys,os
import pandas as pd
from google.cloud import storage


root = "C:/Users/Sudipt Panda/Downloads/amicorpus"
path = os.path.join(root, "targetdirectory")

Filenames = pd.DataFrame(columns = ['Path','Name'])


for path, subdirs, files in os.walk(root):
    for name in files:
        Filenames = Filenames.append({'Path': os.path.join(path, name),'Name':os.path.basename(name)},ignore_index=True)

Filenames['Path'] = Filenames['Path'].str.replace('\\','/')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Sudipt Panda/Downloads/crafty-calling-274812-40d0f3d2adb9.json"
storage_client = storage.Client()

buckets = list(storage_client.list_buckets())
bucket = storage_client.get_bucket("theseis_audio")

for index, row in Filenames.iterrows():
    blob = bucket.blob(row['Name'])
    blob.upload_from_filename(row['Path'])


# print(buckets)