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
║  ✧ Project: MDSU - Medium Docs Story Uploader                  ║
║  ✧ Year: 2025                                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
* Note: This automation works only with edge browser!\n
You can't use it while there is any edge proccess running.
Please close all edge windows and proccesses before using this tool.""")

def main():
    print_welcome_message()

    story_title = input("Enter the story title: ")
    docx_path = input("Enter the path to the .docx file: ")

    uploader = medium_docs_upload_session(story_title)
    uploader.read_docs_file(docx_path)
    uploader.upload_story_content()


if __name__ == "__main__":
    main()