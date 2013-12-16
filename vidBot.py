#! /usr/bin/python -O
# Video link information
# A reddit bot to add descriptions to video links
# Usage: ./vidBot.py
# Copyright niroyb 2013

'''This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Please also refer to the stipulations defined in the README file.'''

import subprocess
import string
import random
import praw
import time
import threading
import re
import HTMLParser
import ConfigParser
import vidInfo

# Set up config so we can get basic data
config = ConfigParser.ConfigParser()
config.read("config_real.cfg")

# Reddit related
USERNAME = config.get("Reddit", "username")
PASSWORD = config.get("Reddit", "password")

COMMENT_FOOTER = u"\n\n_____\n^(Hey I'm a bot, I give info on video links.)"
COMMENT_TEMPLATE = u"{0}" + COMMENT_FOOTER
COMMENT_BUG_TEXT = u"Sorry, there was an error obtaining the info" +\
                   COMMENT_FOOTER
# Objects
# Reddit related
R = praw.Reddit(user_agent = config.get("Reddit", "user_agent"))
R.login(USERNAME, PASSWORD)
html_parser = HTMLParser.HTMLParser()

# Random string generator
def get_id(size=6, chars=string.ascii_uppercase + string.digits):
    '''Returns pseudo-random unique ID string'''
    return ''.join(random.choice(chars) for x in xrange(size))

def download_vid_info(video_url, file_prefix = None):
    '''Dowloads the video info from url, returns info file name.
    Will raise an exception on error'''
    if file_prefix == None:
        file_prefix = get_id()
    assert ' ' not in file_prefix
    assert ' ' not in video_url
    
    cmd = "youtube-dl --write-info-json --skip-download -o {} {}"
    args = cmd.format(file_prefix, video_url).split()
    subprocess.check_call(args, stdout=open("NUL", "w"), \
                          stderr=subprocess.STDOUT)
    return file_prefix + '.info.json'

def reply_to_comment(comment, video_url):
    '''Replies to comment with info from video_url'''
    try:
        info_file_name = download_vid_info(video_url)
        desc = vidInfo.json_to_comment(info_file_name)
    except Exception as e:
        # print e
        comment.reply(COMMENT_BUG_TEXT)
    else:
        comment.reply(COMMENT_TEMPLATE.format(desc))
    print "Replied ", comment.permalink

def get_comment_URLs(comment):
    '''Returns a list of the urls in a reddit comment'''
    return re.findall('a href="(.*?)"', comment.body_html, re.MULTILINE)
                      
def parse_comment(comment):
    '''Look at the comment content and initiate reply thread'''
    urls = get_comment_URLs(comment) + [comment.submission.url]
    if len(urls):
        url = urls[0]
        threading.Thread(
                target=reply_to_comment, 
                args=(comment, html_parser.unescape(url))
                ).start()

def has_replied(comment):
    '''Returns true if logged in user (bot) answered comment'''
    return any(r.author and r.author.name == USERNAME \
               for r in comment.replies)

def can_reply(comment):
    '''Returns true if the comment should be replied to'''
    # Ignore deleted comments
    if comment.author == None:
        return False
    # Prevent infinite self reply loops
    if USERNAME == comment.author.name:
        return False
    # Prevent replying multiple times to same comment 
    if has_replied(comment):
        return False
    # Only reply to directed comments
    if USERNAME in comment.body:
        return True
    # Default
    return False

def debug_comment(comment):
    '''Prints comment info and goes into interactive debug mode'''
    print comment.id
    print comment.permalink
    print comment.body
    print comment.replies
    urls = get_comment_URLs(comment)
    print urls
    import pdb
    pdb.set_trace()
    
def process_comments(comments):
    '''Loop on comments and catch exceptions'''
    for comment in comments:
        try:
            if can_reply(comment):
                parse_comment(comment)
        except Exception, e:
            print e
            # debug_comment(comment)

def main_loop():
    '''Main loop for comment searching and processing'''
    #while True:
    try:
        # Check comments
        comments = R.get_comments("test", limit=None)
        #comments = R.get_comments("all", limit=None)
        process_comments(comments)
        # Finally wait 30 seconds
        time.sleep(30)
    except Exception, e:
        print e

if __name__ == '__main__':
    print 'start'
    main_loop()
    print 'done'
