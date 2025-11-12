import os
import time
import shutil
from story import *

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import win32clipboard
import io
from PIL import Image


class medium_docs_upload_session:
    """
    A class which handles uploading documents to Medium.com 
    """

    def __init__(self, story_title=""):
        self.new_story = story(title=story_title)


    def read_docs_file(self, docx_path: str):
        """
        Read the content of a .docx file, preserving the order of text and images.
        Adds text and images to self.new_story in the same order they appear in the docx.
        """
        tmp_dir = f"tmp_docx_images_{int(time.time())}"
        os.makedirs(tmp_dir, exist_ok=True)

        doc = Document(docx_path)

        # helper to save an image part and return its path
        def save_image_part(image_part, index):
            # determine extension from content type, fallback to png
            content_type = getattr(image_part, "content_type", "")
            ext = content_type.split("/")[-1] if "/" in content_type else "png"
            img_path = os.path.join(tmp_dir, f"image_{index}.{ext}")
            with open(img_path, "wb") as f:
                f.write(image_part.blob)
            return img_path

        image_counter = 0

        # iterate over the document body children (preserves order)
        for child in doc.element.body:
            tag = child.tag
            if tag == qn('w:p'):  # paragraph
                p = Paragraph(child, doc)  # wrap into python-docx Paragraph
                # iterate runs so we can capture text and images in the correct order
                for run in p.runs:
                    # first, any textual content in the run
                    if run.text and run.text.strip() != "":
                        self.new_story.add_text(run.text)

                    # then check the run for images (blip elements)
                    # a:blip with r:embed attribute references the image rId
                    blips = run._element.xpath('.//a:blip')
                    for blip in blips:
                        rId = blip.get(qn('r:embed'))  # rId like 'rId5'
                        if not rId:
                            continue
                        # get the related part via the document part relationships
                        try:
                            rel = doc.part.rels[rId]
                            image_part = rel.target_part
                        except Exception:
                            # fallback - some docx versions store related_parts differently
                            image_part = doc.part.related_parts.get(rId, None)
                        if image_part is None:
                            continue
                        img_path = save_image_part(image_part, image_counter)
                        image_counter += 1
                        self.new_story.add_image(img_path)

                # if paragraph had no runs with text or images but you want to keep blank paragraph
                if not p.runs and p.text.strip() == "":
                    # optional: keep blank paragraph if you want
                    # self.new_story.add_text("")
                    pass

            elif tag == qn('w:tbl'):  # table
                tbl = Table(child, doc)
                # add table content as text blocks (row by row)
                for row in tbl.rows:
                    row_texts = []
                    for cell in row.cells:
                        cell_text = cell.text.strip()
                        if cell_text:
                            row_texts.append(cell_text)
                    if row_texts:
                        # join cells by a separator (customize as you like)
                        self.new_story.add_text(" | ".join(row_texts))

            else:
                # other block types (sectPr etc.) — ignore or handle if needed
                pass

    
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
                # last_para.send_keys(Keys.ENTER)
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

    def upload_image(self, driver, wait, image_local_path: str):
        """
        Upload an image to Medium by copying it to the clipboard and pasting it
        after the last visible paragraph (not splitting it).
        """

        # --- Step 1: Copy image to clipboard ---
        image = Image.open(image_local_path)
        output = io.BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # skip BMP header
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        # --- Step 2: Wait until paragraphs are ready ---
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'p[data-testid="editorParagraphText"]')
        ))

        # --- Step 3: Scroll to bottom ---
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.4)

        # --- Step 4: Find last paragraph ---
        paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p[data-testid="editorParagraphText"]')
        if not paragraphs:
            raise Exception("No paragraphs found in Medium editor.")
        last_para = paragraphs[-1]

        # --- Step 5: Place caret *after* the paragraph text using JS ---
        driver.execute_script("""
            const el = arguments[0];
            const range = document.createRange();
            const sel = window.getSelection();
            range.selectNodeContents(el);
            range.collapse(false);  // move to end
            sel.removeAllRanges();
            sel.addRange(range);
        """, last_para)
        time.sleep(0.2)

        # --- Step 6: Press Enter to create a *new empty paragraph* after the last one ---
        last_para.send_keys(Keys.ENTER)
        time.sleep(0.4)

        # --- Step 7: Focus new empty paragraph ---
        new_paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p[data-testid="editorParagraphText"]')
        target_para = new_paragraphs[-1]
        target_para.click()
        time.sleep(0.3)

        # --- Step 8: Paste image from clipboard ---
        target_para.send_keys(Keys.CONTROL, 'v')

        # --- Step 9: Wait until image appears ---
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'figure img')))
        time.sleep(0.5)

        print("✅ Image successfully inserted after the last paragraph (no text split).")




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

            print(self.new_story.content)

            # Insert each paragraph
            for i in self.new_story.content:
                if i[0] == "text":
                    self.upload_text(driver, wait, i[1])
                elif i[0] == "image":
                    self.upload_image(driver, wait, i[1])
                

            print("✅ Content inserted")
            print("Story is ready. Review and publish manually if you wish.")
            time.sleep(5)

        finally:
            # Keep the browser open for manual publishing
            print("Browser left open for manual publishing.")