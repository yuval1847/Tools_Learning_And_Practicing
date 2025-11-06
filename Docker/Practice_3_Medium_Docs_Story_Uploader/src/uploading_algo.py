import json
import requests
from docx import Document
from constants import *

class medium_docs_upload_session:
    """
    A class which handles uploading documents to Medium.com 
    """

    def __init__(self):
        self.user_integration_token = None
        self.user_id = None


    def connect(self, user_integration_token:str):
        """
        Connect to Medium API using the provided integration token.
        """
        self.user_integration_token = user_integration_token
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain',
                   'Host': MEDIUM_API_SUBDOMAIN,
                   'Accept-Charset': 'utf-8',
                   "Authorization": self.user_integration_token}
        medium_user_id_request = requests.get("https://"+MEDIUM_API_SUBDOMAIN+"/v1/me", headers=headers)
        if medium_user_id_request.status_code != 200:
            raise Exception("Failed to connect to Medium API: " + medium_user_id_request.text)
        else:
            self.user_id = medium_user_id_request.json()['data']['id']
    

    def upload_docs_file(self, file_path:str):
        """
        Read the content of a .docs file while uploading its content to the site medium as a new story.
        """
        doc = Document(file_path)
        # Continue the uploading function...