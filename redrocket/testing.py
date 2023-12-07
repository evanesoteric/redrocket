#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    Red Rocket
    ~~~~~~~~~~
    YouTube playlist automation

    1. open browser to playlist overview
    2. get video count
    3. play each video for video count
    4. close browser
    5. swap proxy and user-agent
    6. repeat

    BUGS:
        add try-except for opening playlist
        -- close and repoen same everything 3 times

    TODO:
        add more exception blocks
        shuffle proxies after importing

'''


# imports
from config import *
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException
# from user_agents import user_agents



def which_playlist(playlist):
    try:
        logging.info('playlist = ' + str(playlist))
    except:
        logging.critical('Could not log which_playlist(). EXITING!')
        sys.exit()


def which_proxy(proxy_ip):
    try:
        logging.info('proxy = ' + str(proxy_ip))
    except:
        logging.critical('Could not log proxy_ip. EXITING!')
        sys.exit()



def close_popups(browser):
    again = 3
    while again > 0:
        again -= 1

        try:
            browser.find_element_by_id("dismiss-button").click()
            time.sleep(2)
        except:
            pass

        try:
            browser.find_elements_by_css_selector("[aria-label='Got it']").click()
            time.sleep(2)
        except:
            pass

        try:
            browser.find_elements_by_css_selector("[aria-label='No thanks']").click()
            time.sleep(2)
        except:
            pass


# delay of 51 to 133 seconds
def delay(browser):
    time.sleep(random.randrange(52, 83))

    # after delay > detect and close popups
    close_popups(browser)


# browser config
def browser_config(proxy_ip):
    try:
        # initialize Firefox profile
        fp = webdriver.FirefoxProfile('1h71xg5a.redrocket')

        ## USER AGENT (problematic - changes elements/tag names)
        # select a random user_agent
        # ua = random.choice(user_agents)
        # set user_agent
        # fp.set_preference("general.useragent.override", str(ua))

        # mute audio on browser
        fp.set_preference("media.volume_scale", "0.0")

        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http", str(proxy_ip))
        fp.set_preference("network.proxy.http_port", int(65432))
        fp.set_preference("network.proxy.ssl", str(proxy_ip))
        fp.set_preference("network.proxy.ssl_port", int(65432))
    except:
        logging.critical('Could not set browser config. EXITING!')
        sys.exit()

    return fp


# start Firefox with a user-agent and ad-block extension (spoof profile)
def start_browser(fp):
    try:
        browser_options = Options()
        browser_options.headless = True
        browser = webdriver.Firefox(firefox_profile=fp, options=browser_options)
        return browser
    except:
        logging.critical('Could not open browser. EXITING!')
        sys.exit()


# open playlist overview page
def playlist_overview(browser, playlist):
    try:
        browser.get(playlist)
    except:
        logging.critical('could not open playlist. EXITING!')
        sys.exit()


# get video count from playlist overview page
def get_vid_count(browser):
    try:
        vid_count = browser.find_element_by_id('stats')
        vid_count = vid_count.text
        vid_count = re.match('\d+', vid_count).group()
        logging.info('vid_count = ' + str(vid_count))
        return vid_count
    except:
        logging.critical('could not get vid_count. EXITING!')


def current_vid(browser):
    try:
        current_vid = browser.current_url
        current_vid = re.search('v=.*&list', current_vid).group()
        current_vid = current_vid.replace('v=', '')
        current_vid = current_vid.replace('&list', '')
        logging.info('current video: ' + current_vid)
    except:
        logging.error('could not get current video title. PASSING!')
        pass


# start playlist (from playlist overview page - after getting video count)
def start_playlist(browser):
    try:
        browser.find_element_by_id('playlist-thumbnails').click()
    except:
        logging.critical('playlist start button failed. Exiting!')
        sys.exit()


# skip to next video (after delay)
def next_vid(browser):
    try:
        ActionChains(browser).key_down(Keys.SHIFT).send_keys('n').perform()
        # browser.find_element_by_class_name('ytp-next-button').click()
    except:
        logging.critical('shift n actionchain failed. PASSING.')
        pass


# play/pause video (unused)
def play_pause(browser):
    try:
        browser.send_keys('k')
        # browser.find_element_by_id('movie_player').click()
    except:
        logging.critical('shift n actionchain failed. PASSING.')
        pass


# delete session data and close browser
def close_browser(browser):
    # delete cookies
    try:
        browser.delete_all_cookies()  # don't think this is needed but, idk so keep
    except:
        logging.error('could not delete browser cookies. PASSING!')
        pass

    # close browser entirely
    try:
        browser.close()
    except:
        logging.error('could not close browser. PASSING!')
        pass



'''
    RedRocket Bot
'''
def bot(playlist, proxy_ip):
    which_playlist(playlist)
    which_proxy(proxy_ip)
    fp = browser_config(proxy_ip)
    browser = start_browser(fp)

    # wait for browser to start
    time.sleep(12)

    # open youtube overview page
    playlist_overview(browser, playlist)

    # wait for page to load
    time.sleep(12)

    # after sleeping search for boxes to close
    close_popups(browser)
    time.sleep(3)

    # get total number of videos in playlist
    vid_count = get_vid_count(browser)

    # start playing music
    start_playlist(browser)

    # first video playing, let it play then start loop
    delay(browser) # delay and close popups

    # list to each track
    for i in range(int(vid_count)):
        current_vid(browser)
        delay(browser) # delay and close popups

        next_vid(browser)

    # close session after watching all videos
    close_browser(browser)
    # then fully quit to inject config
    browser.quit()

    time.sleep(3)

    ## SEE IF I CAN INCORPORATE THIS INTO DOCKER
    # delete tmp files and cache
    # os.system('rm -rf /tmp/*')
    # os.system('rm -rf $HOME/.cache/mozilla')
    # time.sleep(3)

    # DONE
    logging.info('complete')


'''
    BOT LOOP
    ~~~~~~~~
    Listen to each playlist with each proxy.
    Loop a total of 5 times
'''
cycles = 5
while cycles > 0:
    cycles -= 1
    try:
        for playlist_uri in playlists:
            playlist = 'https://www.youtube.com/playlist?list=' + playlist_uri
            for proxy_ip in proxies:
                # skip proxy if dead (or ping over 300ms)
                is_proxy_alive = subprocess.call(['ping', '-c', '1', '-W', '3', proxy_ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if is_proxy_alive != 0:
                    continue

                # run bot
                bot(playlist, proxy_ip)
    except:
        logging.critical('CRASHED! EXITING!')
        sys.exit()

    logging.info('cycle ' + str(cycles) + ' complete.')


# LOG WHEN FINISHED
logging.info('FINISHED - ALL PROXIES USED ON ALL PLAYLISTS!')
