from googleapiclient.errors import HttpError

def files_to_google_doc(service1, service2, files_list, folder_id):
  """Converts files to google docs and moves them to the same folder and deletes the original file.
  Args:
      service1: a Google Drive service object
      service2: a Google Drive service object
      files_list: a list of files to be converted
      folder_id: the id of the folder
  """
  for file in files_list:
    docs_name = file['name'].split('.')[0]
    file_id = file['id']
    print(docs_name)
    try:
      service2.files().copy(fileId=file_id, convert=True, body={"name": docs_name, "parents": [folder_id]}).execute()
      service1.files().delete(fileId=file_id).execute()


    except HttpError as err:
          print(err)
