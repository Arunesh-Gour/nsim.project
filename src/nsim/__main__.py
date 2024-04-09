import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(
   Path(__file__).parent.parent.resolve(),
))

if __name__ == '__main__':
   from nsim.ui import cli
   
   cli.execute()
   
   print('''
   NSIM, a concept prototype, is a package of simple, yet powerful tools and
   libraries allowing developers to develop and debug custom network algorithms
   with ease and efficiency.
   But being a concept prototype, its functionality and practicality is vastly
   limited.
   
   It is designed to be used as a library and hence, is not intended to be run
   via command line (cli).
   
   Please use '-h' or '--help' flag for help / documentation.
   ''')
   
   exit(0)
