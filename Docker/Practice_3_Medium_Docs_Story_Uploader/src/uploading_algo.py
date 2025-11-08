import json
import requests
import zipfile
import os
import time

from docx import Document
from lxml import etree
from constants import *
from story import *



class medium_docs_upload_session:
    """
    A class which handles uploading documents to Medium.com 
    """

    def __init__(self, user_integration_token:str, story_title=""):
        self.user_integration_token = user_integration_token
        self.user_id = None
        self.new_story = story(title=story_title)


    def connect(self):
        """
        A function which connect to Medium API using the provided integration token and retrieves the user ID.
        """
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
    

    def read_docs_file(self, docx_path:str):
        """
        Read the content of a .docs file and returns its content as a string in HTML format.
        """
        # A temporary folder for images
        tmp_dir = f"tmp_docx_images_{int(time.time())}"
        os.makedirs(tmp_dir, exist_ok=True)

        # Extract the document.xml file (the real content)
        with zipfile.ZipFile(docx_path) as docx_zip:
            xml_content = docx_zip.read("word/document.xml")

            # Map image IDs to actual file names
            rels_xml = docx_zip.read("word/_rels/document.xml.rels")
            rels_tree = etree.fromstring(rels_xml)
            rels = {}
            for rel in rels_tree:
                rid = rel.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
                target = rel.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}target")
                if target.startswith("media/"):
                    rels[rid] = target

           # Parse document XML
            tree = etree.fromstring(xml_content)
            ns = {
                "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
                "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            }

            image_counter = 1

            # Iterate over document body elements
            for element in tree.findall(".//w:body/*", ns):
                # If paragraph
                if element.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p":
                    text = "".join(node.text for node in element.findall(".//w:t", ns) if node.text)
                    if text.strip():
                        self.new_story.add_text(text)

                # If image (drawing)
                for blip in element.findall(".//a:blip", ns):
                    rid = blip.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                    if rid in rels:
                        img_path = "word/" + rels[rid]
                        img_data = docx_zip.read(img_path)

                        # Give each image a separate filename
                        img_name = f"image_{image_counter}" + os.path.splitext(rels[rid])[1]
                        img_output_path = os.path.join(tmp_dir, img_name)

                        # Save image file
                        with open(img_output_path, "wb") as f:
                            f.write(img_data)

                        # Upload image to Medium
                        image_url = self.upload_image(img_output_path)
                        self.new_story.add_image(image_url)
                        
                        image_counter += 1


    def upload_image(self, image_url:str):
        """
        Upload an image to Medium.com and return the image URL.
        """
        with open(image_url, "rb") as f:
            image_upload = requests.post(
                "https://"+MEDIUM_API_SUBDOMAIN+"/v1/images",
                headers={"Authorization": f"Bearer {self.user_integration_token}"},
                files={"image": f}
            ).json()
        return image_upload["data"]["url"]


    def upload_story_content(self, publish_status:str="draft", story_tags_lst:list=[]):
        """
        Upload the story content to Medium.com
        """
        if self.user_id is None or self.user_integration_token is None:
            raise Exception("Not connected to Medium API. Please call connect() first.")
        
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain',
                   'Host': MEDIUM_API_SUBDOMAIN,
                   'Accept-Charset': 'utf-8',
                   "Authorization": self.user_integration_token}

        post_data = {
            "title": self.new_story.title,
            "contentFormat": "html",
            "content": self.new_story.get_content_as_html(),
            "tags": story_tags_lst,
            "publishStatus": publish_status
        }

        medium_story_upload_request = requests.post("https://"+MEDIUM_API_SUBDOMAIN+"/v1/users/"+self.user_id+"/posts", 
                                                    headers=headers, 
                                                    data=json.dumps(post_data))
        
        if medium_story_upload_request.status_code != 201:
            raise Exception("Failed to upload story to Medium")
        else:
            print("Story uploaded successfully! Story URL: " + medium_story_upload_request.json()['data']['url'])