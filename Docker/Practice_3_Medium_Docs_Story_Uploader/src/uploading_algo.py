import os
import time
import shutil
from story import *
from docx import Document
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class medium_docs_upload_session:
    """
    A class which handles uploading documents to Medium.com 
    """

    def __init__(self, story_title=""):
        self.new_story = story(title=story_title)


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

    
    def upload_title(self, driver, wait):
        # Wait until the title field appears
        print("Waiting for title element...")
        title_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h3[data-testid="editorTitleParagraph"]'))
        )
        # Inject the title safely (triggers React events)
        driver.execute_script("""
            const el = arguments[0];
            const text = arguments[1];
            el.textContent = text;
            el.dispatchEvent(new InputEvent('input', { bubbles: true }));
        """, title_element, self.new_story.title)
        print("✅ Title inserted")

    def upload_text(self, driver, wait, text: str, timeout_after_each_paragraph=0.15):
        """
        Insert text into Medium editor reliably by:
        - selecting the last content paragraph (p[data-testid="editorParagraphText"])
        - moving caret to its end via JS Range/Selection
        - sending keys (so React sees native keyboard events)
        Splits text by newline and inserts paragraphs in order.
        """
        print("Waiting for at least one content paragraph...")
        # Wait for at least one content paragraph to exist
        content_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-testid="editorParagraphText"]'))
        )

        # Find *all* content paragraphs and pick the last one (works if editor already has paragraphs)
        paras = driver.find_elements(By.CSS_SELECTOR, 'p[data-testid="editorParagraphText"]')
        if not paras:
            raise RuntimeError("No content paragraphs found after wait()")

        last_para = paras[-1]

        # Move caret/selection to end of the last paragraph using JS (works better than click)
        # This JS sets caret at the end of the element (creates a text node if needed).
        set_caret_js = """
        const el = arguments[0];
        // Ensure there's a text node so range.setStart works
        if (!el.firstChild) {
            el.appendChild(document.createTextNode(''));
        }
        const range = document.createRange();
        // If the element has child nodes, put caret after last child
        range.selectNodeContents(el);
        range.collapse(false); // move caret to end
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        // Focus the element to receive keyboard events
        el.focus();
        return true;
        """

        driver.execute_script(set_caret_js, last_para)
        time.sleep(0.05)  # tiny pause to allow focus to settle

        # Now type paragraphs one by one (preserves ordering)
        paragraphs = text.split("\n")

        actions = ActionChains(driver)
        for i, paragraph in enumerate(paragraphs):
            # send the paragraph text as native keys
            # Some huge paragraphs may need to be broken; here we send as one send_keys call
            last_para.send_keys(paragraph)

            # After each paragraph except the last, press ENTER to create a new paragraph,
            # then move caret to the end of that newly-created paragraph
            if i != len(paragraphs) - 1:
                last_para.send_keys(Keys.ENTER)
                time.sleep(timeout_after_each_paragraph)

                # re-locate the last paragraph (Medium creates a new <p>)
                paras = driver.find_elements(By.CSS_SELECTOR, 'p[data-testid="editorParagraphText"]')
                last_para = paras[-1]

                # set caret to end of this new paragraph so next send_keys goes to correct place
                driver.execute_script(set_caret_js, last_para)
                time.sleep(0.02)

        # small wait to ensure editor processed the keystrokes
        time.sleep(0.2)
        print("✅ Text inserted (keystrokes).")

    def upload_image(self, driver, wait, image_local_path:str):
        add_image_button = driver.find_element(By.CSS_SELECTOR, 'button[data-action="inline-menu-image"]')
        add_image_button.click()
        image_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][accept^="image/"]')
        image_input.send_keys(image_local_path)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'figure img'))
        )
        print("✅ Image inserted")


    def upload_story_content(self):
        """
        Upload the story content to Medium.com using an existing Edge session (remote debugging).
        """
        options = Options()
        options.debugger_address = "localhost:9222"
        service = Service(r"C:/Users/USER/Downloads/msedgedriver.exe")

        driver = webdriver.Edge(options=options, service=service)

        try:
            # Go to Medium "new story" page
            driver.get("https://medium.com/new-story")

            # Wait for user to confirm they are logged in
            print("Please log in manually if not already, then press Enter...")
            input()

            wait = WebDriverWait(driver, 20)

            # Insert the title
            self.upload_title(driver, wait)

            # Insert each paragraph
            for paragraph in self.new_story.content:
                if paragraph["type"] == "text":
                    self.upload_text(driver, wait, paragraph["value"])
                elif paragraph["type"] == "image":
                    self.upload_image(driver, wait, paragraph["value"])
                

            print("✅ Content inserted")
            print("Story is ready. Review and publish manually if you wish.")
            time.sleep(5)

        finally:
            # Keep the browser open for manual publishing
            print("Browser left open for manual publishing.")