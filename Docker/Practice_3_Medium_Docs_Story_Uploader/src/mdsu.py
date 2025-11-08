"""
A python tool that automate the proess of uploadinng docs files as storing to the site "medium.com"
"""

from uploading_algo import medium_docs_upload_session


def print_welcome_message():
    print("""
        ███╗   ███╗██████╗ ███████╗██╗   ██╗    ╔══════\\
        ████╗ ████║██╔══██╗██╔════╝██║   ██║    ║   ▄▄  \\
        ██╔████╔██║██║  ██║███████╗██║   ██║    ║ ▄▄▄ ▄▄ ║
        ██║╚██╔╝██║██║  ██║╚════██║██║   ██║    ║ ▄▄▄▄▄▄ ║ 
        ██║ ╚═╝ ██║██████╔╝███████║╚██████╔╝    ║ ▄▄▄▄ ▄ ║
        ╚═╝     ╚═╝╚═════╝ ╚══════╝ ╚═════╝     ╚════════╝
        ╔════════════════════════════════════════════════════════════════╗
        ║                                                                ║
        ║                      ✦✦  Credits  ✦✦                           ║
        ║                                                                ║
        ║  This program was written for educational purposes only.       ║
        ║  Please use it responsibly and with respect to others.         ║
        ║                                                                ║
        ║  ✧ Author: Yuval Quina                                         ║
        ║  ✧ Project: MDSU - Medium Docs Story Uploader                   ║
        ║  ✧ Year: 2025                                                  ║
        ║                                                                ║
        ╚════════════════════════════════════════════════════════════════╝""")

def main():
    story_title = input("Enter the story title: ")
    docx_path = input("Enter the path to the .docx file: ")
    user_integration_token = input("Enter your Medium integration token: ")
    publish_status = input("Enter publish status (draft/published/unlisted): ").lower()

    if publish_status not in ["draft", "published", "unlisted"]:
        print("Invalid publish status. Defaulting to 'draft'.")
        publish_status = "draft"

    story_tags = input("Enter story tags separated by commas (optional): ")
    story_tags_lst = [tag.strip() for tag in story_tags.split(",")] if story_tags else []

    uploader = medium_docs_upload_session(story_title=story_title, user_integration_token=user_integration_token)
    uploader.connect()
    uploader.read_docs_file(docx_path)
    uploader.upload_story_content(publish_status=publish_status, story_tags_lst=story_tags_lst)



if __name__ == "__main__":
    main()