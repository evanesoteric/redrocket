import subprocess
from random import shuffle


# import proxies as list
with open('bots.txt', 'r') as f:
    bots = [line for line in f.read().splitlines() if line.strip()]

# import proxies as list
with open('proxies.txt', 'r') as f:
    proxies = [line for line in f.read().splitlines() if line.strip()]

# import playlists as list
with open('playlists.txt', 'r') as f:
    playlists = [line for line in f.read().splitlines() if line.strip()]



def sync_bot():
    for bot in bots:
        p = subprocess.run(["docker", "cp", "redrocket.py", str(bot) + ":/root/redrocket.py"])


def sync_playlists():
    for bot in bots:
        p = subprocess.run(["docker", "cp", "playlists.txt", str(bot) + ":/root/playlists.txt"])


def sync_proxies():
    # randomize proxy order
    shuffle(proxies)

    # send
    for bot in bots:
        # create sublist of first 10 proxies
        selection = proxies[:10]

        # write sublist to proxy_selection.txt
        with open('proxy_selection.txt', 'w+') as f:
            for line in selection:
                f.write(line + '\n')

        # delete first 10 proxies from proxy list
        del proxies[:10]

        # sync
        p = subprocess.run(["docker", "cp", "proxy_selection.txt", str(bot) + ":/root/proxies.txt"])


# sync_playlists()
# sync_proxies()

sync_bot()
