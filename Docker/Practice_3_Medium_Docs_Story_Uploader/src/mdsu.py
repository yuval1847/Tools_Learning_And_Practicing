"""
A python tool that automate the proess of uploadinng docs files as storing to the site "medium.com"
"""

from uploading_algo import medium_docs_upload_session
from chrome_profile_handling import choose_profile


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
║  ✧ Project: MDSU - Medium Docs Story Uploader                  ║
║  ✧ Year: 2025                                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
* Note: This automation works only with google chrome browser!\n""")

def main():
    print_welcome_message()

    story_title = input("Enter the story title: ")
    docx_path = input("Enter the path to the .docx file: ")
    selected_google_profile = choose_profile()

    uploader = medium_docs_upload_session(story_title=story_title, google_profile=selected_google_profile)
    uploader.read_docs_file(docx_path)
    uploader.upload_story_content()


if __name__ == "__main__":
    main()