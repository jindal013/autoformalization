from google.cloud.storage import Client, transfer_manager
import os

BUCKET_NAME = "10bt_gpt4"
DATA_CACHE_DIR = "/Users/chinmay/Programming/deep_learning/data/edu_fineweb10B"
FILE_NAMES = os.listdir(DATA_CACHE_DIR)
WORKERS = 8

def main():

  def upload_many_blobs_with_transfer_manager(
      bucket_name, filenames, source_directory="", workers=8
  ):

      storage_client = Client()
      bucket = storage_client.bucket(bucket_name)

      results = transfer_manager.upload_many_from_filenames(
          bucket, filenames, source_directory=source_directory, max_workers=workers, worker_type=transfer_manager.THREAD
      )

      for name, result in zip(filenames, results):

          if isinstance(result, Exception):
              print("Failed to upload {} due to exception: {}".format(name, result))
          else:
              print("Uploaded {} to {}.".format(name, bucket.name))

  upload_many_blobs_with_transfer_manager(BUCKET_NAME, FILE_NAMES, DATA_CACHE_DIR, WORKERS)

if __name__ == '__main__':
    main()