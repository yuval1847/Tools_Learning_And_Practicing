from Scanning_technics import scannig_techniques


def first_load():
    # A function which prints the welcome message.
    print("""
 ____   _                          _         _____                ⠀⠀⠀⠀⠀⠀⠀⡀⢀⢆⠏ ⡚⢁⠏⠀⠎⡡⠂⡠⠄⢀⠀⠀⠀
|  _ \ | |__    ___    ___  _ __  (_)__  __ | ____|_   _   ___    ⠀⠀⣀⡤⡰⠁⣎⣀⣸⣾⡾⠿⢿⣿⣷⣾⣤⡂⣔⡱⡑⡡⣄⠀⠀
| |_) || '_ \  / _ \  / _ \| '_ \ | |\ \/ / |  _| | | | | / _ \   ⠀⠀⠱⡀⢘⣢⡶⠛⠉⠀⣇⠀⠘⣿⣿ ⣀⡏⠻⡻⣭⣧⡁⡐⠁
|  __/ | | | || (_) ||  __/| | | || | >  <  | |___| |_| ||  __/   ⠴⣤⣶⣿⠛⠀⠀⠀⠀ ⠘⣆⠀⠙⠿⠿⠟⠃⢠⠇⠈⣹⡶⣷⡅
|_|    |_| |_| \___/  \___||_| |_||_|/_/\_\ |_____|\__, | \___|    ⠀⠀⠈⢑⢗⡤⣠⣀⣀⣀⣀⡓⣄⣀⣀⣠⣴⡣⢶⡋⡙⣢⠀⠀
                                                    |___/                ⠈⠘⠂⠃⠀⠏⠀⡏⠈⠏⠹⠈⠙⠀⠓⠂⠉⠁
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                      ✦✦  Credits  ✦✦                           ║
║                                                                ║
║  This program was written for educational purposes only.       ║
║  Please use it responsibly and with respect to others.         ║
║                                                                ║
║  ✧ Author: Yuval Quina                                         ║
║  ✧ Project: PhoenixEye                                         ║
║  ✧ Year: 2025                                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝""")


def main():
    # The main function of the program.
    first_load()
    scannig_techniques.print_results(scannig_techniques.scan())


if __name__ == "__main__":
    main()