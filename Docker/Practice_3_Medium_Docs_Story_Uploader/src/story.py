class story:
    """
    A class which represents a story to be uploaded to Medium.com
    """

    def __init__(self, title="", content=[]):
        self.title = title
        self.content = content
        

    def add_text(self, paragraph_text:str):
        """
        Add a string to the story content.
        """
        self.content.append(["text", paragraph_text])

    def enhance_content_text(self):
        """
        A function which enhance the story content text. 
        """

        # Add \n after each ':'
        for i in range(len(self.content)):
            if self.content[i][0] == "text":
                paragraph = self.content[i][1]
                enhanced_paragraph = paragraph.replace(":", ":\n")
                self.content[i][1] = enhanced_paragraph

    def add_image(self, image_path:str):
        """
        Add an image to the story content.
        """
        self.content.append(["image", image_path])