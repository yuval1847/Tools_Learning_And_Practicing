import os
import time
from story import *
from docx import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class medium_docs_upload_session:
    """
    A class which handles uploading documents to Medium.com 
    """

    def __init__(self, story_title="", google_profile=None):
        self.new_story = story(title=story_title)
        self.google_profile = google_profile


    def read_docs_file(self, docx_path:str):
        """
        Read the content of a .docs file.
        """
        # A temporary folder for images
        tmp_dir = f"tmp_docx_images_{int(time.time())}"
        os.makedirs(tmp_dir, exist_ok=True)
        print(os.path.exists(docx_path))  # True if Python can see it
        doc = Document(docx_path)

        for i, para in enumerate(doc.paragraphs):
            self.new_story.add_text(para.text)

        for i, rel in enumerate(doc.part.rels):
            rel = doc.part.rels[rel]
            if "image" in rel.target_ref:
                img_path = f"{tmp_dir}/image_{i}.png"
                with open(img_path, "wb") as f:
                    f.write(rel.target_part.blob)
                self.new_story.add_image(img_path)


    def upload_story_content(self):
        """
        Upload the story content to Medium.com
        """
        user_data_dir, profile_dir = self.google_profile
        # assume user_data_dir is a Path, profile_dir is the profile folder name (e.g., "Default", "Profile 1")
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_dir}")   # e.g. C:\Users\...\User Data
        options.add_argument(f'--profile-directory={profile_dir}')  # e.g. Default or Profile 1
        # optional: start maximized
        options.add_argument("--start-maximized")

        # IMPORTANT: ensure Chrome is fully closed before launching with the same profile
        driver = webdriver.Chrome(options=options)
        time.sleep(5)  # wait for browser to start
        try:
            # Navigate to new story page
            driver.get("https://medium.com/new-story")

            # Wait for user to log in manually
            print("Please log in manually if not already, then press Enter...")
            input()

            # Fill in title
            title_field = driver.find_element(By.CSS_SELECTOR, 'textarea[placeholder="Title"]')
            title_field.clear()
            title_field.send_keys(self.new_story.title)

            # Fill in story content
            content_html = self.new_story.get_content_as_html()

            # The Medium editor is a div[role="textbox"], but Selenium cannot set innerHTML directly
            # So we can use JavaScript execution
            driver.execute_script(
                "document.querySelector('div[role=\"textbox\"]').innerHTML = arguments[0];",
                content_html
            )

            print("Story is ready. Review and publish manually if you wish.")
            # Optional: wait so user can see the result
            time.sleep(5)

        finally:
            driver.quit()