from google.cloud import storage
import os

BUCKET_NAME = "10bt_gpt4"
DATA_CACHE_DIR = "/Users/chinmay/Programming/deep_learning/data/edu_fineweb10B"
FILE_NAMES = os.listdir(DATA_CACHE_DIR)
WORKERS = 8
i = 1

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    print('working on', source_file_name)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


for s in (sorted(os.listdir(DATA_CACHE_DIR))):
    if i < 23:
        i = i+1
        continue;
    path = DATA_CACHE_DIR + "/" + s
    # print(path)
    upload_blob(BUCKET_NAME, path, s)
    i += 1