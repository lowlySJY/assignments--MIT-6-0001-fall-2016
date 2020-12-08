# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:jinyi
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Parameters
        ----------
        guid : string
            globally unique identifier (GUID)
        title : string
            the news story's headline
        description : string
            a paragraph or so summarizing the story
        link : string
            a link to a website with the entire story
        pubdate : datetime
            date the news was published
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def is_phrase_in(self, phrase, text):
        '''
        takes in one string argument text. 
    
        returns True if the whole phrasephrase is present in text, False otherwise.
        '''
        # the trigger is not case sensitive
        phrase = phrase.lower()
        text = text.lower()
        p_split = phrase.split(' ')
        t_split = []
        t_split_nospace = []
        word = ''
        # text include consecutive punctuation
        # judge every element in text string
        for l in text:    
            # if the letter and previous ele is letter, record as word
            if l.isalpha():
                word += l
            # else the word is splited by punctuation
            else:
                t_split.append(word)
                word = ''
        if word != '':
            t_split.append(word)
        for t in t_split:
            if t != '':
                t_split_nospace.append(t)
        flag = False
        # compare if the phrase is in text
        for i in range(len(t_split_nospace) - len(p_split) + 1):
            # text is converted into word list which may have many space
            # judge if the word is space at first
            if t_split_nospace[i] == '':
                continue
            n = 0
            for j in range(len(p_split)):
                if p_split[j] == t_split_nospace[i + j]:
                    n += 1
            if n == len(p_split):
                flag = True
                break
        return flag
        
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase
        
    def get_phrase(self):
        return self.phrase
    
    def evaluate(self, story):
        title = story.get_title()
        return self.is_phrase_in(self.get_phrase(), title)
            
# Problem 4
# TODO: DescriptionTrigger
# TIME TRIGGERS
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase
        
    def get_phrase(self):
        return self.phrase
    
    def evaluate(self, story):
        des = story.get_description()
        return self.is_phrase_in(self.get_phrase(), des)
    
# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def string_to_datetime(self, datetime_str):
        datetime_str = datetime_str.split(' ')
        time = datetime_str[-1]
        time = time.split(':')
        date = datetime_str[:3]
        month_dict = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,
                      'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,
                      'Nov':11,'Dec':12}
        return datetime(int(date[2]), month_dict[date[1]],
                        int(date[0]), int(time[0]),
                        int(time[1]), int(time[2]))
    
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, datetime_str):        
        self.datatime = self.string_to_datetime(datetime_str)
        
    def get_datetime(self):
        return self.datatime
    
    def evaluate(self, story):
        story_dt = story.get_pubdate()
        if story_dt.tzinfo != None:                
            trigger_time = self.get_datetime()
            trigger_time = trigger_time.replace(tzinfo=pytz.timezone("EST"))
        else:
            trigger_time = self.get_datetime()
        return (story_dt < trigger_time) 

class AfterTrigger(TimeTrigger):
    def __init__(self, datetime_str):        
        self.datatime = TimeTrigger.string_to_datetime(self, datetime_str)
        
    def get_datetime(self):
        return self.datatime
    
    def evaluate(self, story):
        story_dt = story.get_pubdate()
        if story_dt.tzinfo != None:                
            trigger_time = self.get_datetime()
            trigger_time = trigger_time.replace(tzinfo=pytz.timezone("EST"))
        else:
            trigger_time = self.get_datetime()
        return (story_dt > trigger_time)    
        
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.Trigger = trigger
        
    def get_trigger(self):
        return self.Trigger
    
    def evaluate(self, story):
        trigger = self.get_trigger()
        return not trigger.evaluate(story)
        
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    
    def get_t1(self):
        return self.t1
    
    def get_t2(self):
        return self.t2
    
    def evaluate(self, story):
        t1 = self.get_t1()
        t2 = self.get_t2()
        r1 = t1.evaluate(story)
        r2 = t2.evaluate(story)
        return r1 and r2
    
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    
    def get_t1(self):
        return self.t1
    
    def get_t2(self):
        return self.t2
    
    def evaluate(self, story):
        t1 = self.get_t1()
        t2 = self.get_t2()
        r1 = t1.evaluate(story)
        r2 = t2.evaluate(story)
        return r1 or r2

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    s = []
    for story in stories:
        for t in triggerlist:
            if t.evaluate(story):
                s.append(story)
    return s



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    t = []
    for line in lines:
        info = line.split(',')
        if info[0] != 'ADD' and info[1] == 'TITLE':
            t.append(TitleTrigger(info[2]))
        elif info[0] != 'ADD' and info[1] == 'DESCRIPTION':
            t.append(DescriptionTrigger(info[2]))
        elif info[0] != 'ADD' and info[1] == 'AFTER':
            t.append(AfterTrigger(info[2]))
        elif info[0] != 'ADD' and info[1] == 'BEFORE':
            t.append(BeforeTrigger(info[2]))
        elif info[0] != 'ADD' and info[1] == 'NOT':
            t.append(NotTrigger(info[2]))
        elif info[0] != 'ADD' and info[1] == 'AND':
            t.append(AndTrigger(info[2], info[3]))
        elif info[0] != 'ADD' and info[1] == 'OR':
            t.append(OrTrigger(info[2], info[3]))
        else:
            for i in range(1, len(info)):
                t.append(info[i])
    return t
    # print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Clinton")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            # stories = process("http://news.google.com/news?output=rss")
            # stories = process("https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans")
            
            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

