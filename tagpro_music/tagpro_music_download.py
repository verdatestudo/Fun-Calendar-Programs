
'''
TagPro music downloader
First Created: 2016-May-23
Last Updated: 2016-May-23
Python 2.7
Chris
'''

import urllib2
import re

def get_music_links(my_url):
    '''
    Gets the names of each song and returns them in a list.
    '''
    my_list = urllib2.urlopen(my_url).read()
    links = re.findall('\"url\":\"(\w*)\"', my_list) # format is "url":"myfilename"
    return links

def dl_music_links(my_list):
    '''
    Download music files from a provided list of song names.
    '''
    for item in my_list:
        dl_url = 'http://tagpro.koalabeast.com/sounds/music/%s.mp3' %(item)
        mp3file = urllib2.urlopen(dl_url)
        with open(item + '.mp3', 'wb') as output:
            output.write(mp3file.read())

def run():
    '''
    Run
    '''
    my_url = 'http://tagpro.koalabeast.com/music?callback=init'
    links = get_music_links(my_url)
    dl_music_links(links)
