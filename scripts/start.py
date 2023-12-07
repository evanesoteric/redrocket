import subprocess
from random import shuffle


# import proxies as list
with open('bots.txt', 'r') as f:
    bots = [line for line in f.read().splitlines() if line.strip()]


def start():
    for bot in bots:
        p = subprocess.run(["docker", "cp", "playlists.txt", str(bot) + ":/root/playlists.txt"])


start()
