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
        self.content.append({"type": "text", "value": paragraph_text})


    def add_image(self, image_path:str):
        """
        Add an image to the story content.
        """
        self.content.append({"type": "image", "value": image_path})


    def get_content_as_text(self):
        """
        Get the story content as a single text string.
        """
        text_content = f'{self.title}\n\n'
        for item in self.content:
            if item["type"] == "text":
                text_content += f'{item["value"]}\n\n'
            elif item["type"] == "image":
                text_content += f'[Image: {item["value"]}]\n\n'
        return text_content


    def get_content_as_html(self):
        """
        Get the story content as a single HTML string.
        """
        html_content = f'<h1>{self.title}</h1>\n'
        for item in self.content:
            if item["type"] == "text":
                html_content += f'<p>{item["value"]}</p>\n'
            elif item["type"] == "image":
                html_content += f'<img src="{item["value"]}"\n'
        return html_content