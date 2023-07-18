from googleapiclient.discovery import build

class DriveAPI:
    def __init__(self, credentials):
        self.service = build('drive', 'v3', credentials=credentials)

    def create_folder(self, folder_name):
        # Implement the logic to create a folder in Google Drive
        # Use the self.service object to interact with the API
        # Return the ID of the created folder

        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = self.service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

        return folder_id

    # Implement other methods related to Drive interactions, if required
