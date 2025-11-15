"""
A python tool that automate the proess of uploadinng docs files as storing to the site "medium.com"
"""

from uploading_algo import medium_docs_upload_session
import subprocess
from colorama import Fore, Style, Back


def print_welcome_message():
    print(f"""{Fore.BLUE}
███╗   ███╗██████╗ ███████╗██╗   ██╗    ╔════════╗
████╗ ████║██╔══██╗██╔════╝██║   ██║    ║  ▄▄▄▄  ║
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
{Fore.RED}
✦ Note: This automation works only with edge browser!
You can't use it while there is any edge proccess running.
Please close all edge windows and proccesses before using this tool.\n
✦ Note: After a story is uploaded, it is recommended to inspect it and fix mistakes as needed.{Style.RESET_ALL}{Fore.BLUE}\n""")


def terminate_edge_processes():
    """
    A function which terminate all edge proccesses using powershell command.
    """
    terminate_edge_processes_command = "Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force"
    subprocess.run(["powershell", "-Command", terminate_edge_processes_command])

def running_edge_browser():
    """
    A function which runs a new edge browser instance using powershell command.
    """
    starting_edge_instance = r'& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\USER\AppData\Local\Microsoft\Edge\User Data" --profile-directory="Profile 1"'
    subprocess.run(["powershell", "-Command", starting_edge_instance])


def main():
    print_welcome_message()

    story_title = input("Enter the story title: ")
    docx_path = input("Enter the path to the .docx file: ")

    terminate_edge_processes()
    running_edge_browser()

    uploader = medium_docs_upload_session(story_title)
    uploader.read_docs_file(docx_path)
    uploader.upload_story_content()
    
    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()