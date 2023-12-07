#!/usr/bin/python3

import os
from bots import bots


div = "------------------------------"

for bot in bots:
    print(bot)
    c = os.system('docker exec -it ' + str(bot) + ' /bin/bash -c "python3 count.py"')
    print(div)
