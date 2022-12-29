def get_all_files(drive_service, folder_id):
  """Returns all the files in a folder
  
  Args:
      drive_service: a Google Drive service object
      folder_id: the id of the folder
  """
  # Page size is by default 100 and max is 1000
  # Page size refers to max number of files returned in a single request
  drive_result = drive_service.files().list(q=f"'{folder_id}' in parents",fields='nextPageToken, files(name, id, mimeType)', pageSize=1000).execute()
  items = drive_result.get('files', [])

  # Get all the files
  files = []
  for item in items:
    if item['mimeType'] in ['application/msword', "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
      files.append({"id":item['id'], "name":item['name']})
  
  return files
