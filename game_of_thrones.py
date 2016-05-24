import pysrt
from httplib2 import Http
import requests
from soupselect import select
from BeautifulSoup import BeautifulSoup as Soup
from bs4 import BeautifulSoup
import urllib
from afinn import Afinn
import agate
import json
import operator
from senti_classifier import senti_classifier
from textblob import TextBlob
import matplotlib.pyplot as plt
import requests
#import scipy
#import numpy
#from gensim import utils
#from gensim import corpora, models, similarities

afinn = Afinn(language='en')

def test_sentiment_api():
    subs = pysrt.open("subtitles/" + 'S01E01' + ".srt")
    total_text = ""
    for sub in subs:
        total_text += sub.text.replace('\n', ' ').replace('<i>', '').replace('</i>', '').replace("\'", '').replace("?", ' ')
    form = dict(text="love love love")
    r = requests.post("http://text-processing.com/api/sentiment/", data=form)

    unicode_sentiment = r.text.encode("utf-8")
    print json.loads(r.text.encode("utf-8"))['probability']['neg']



def perform_sentiment_analysis():
    sentiment1 = {}
    sentiment2 = {}
    sentiment3 = {}
    text = {}

    for season_number in range(1, 6):
        for episode_number in range(1, 11):
            if(episode_number < 10):
                file_name = 'S0' + str(season_number) + 'E0' + str(episode_number)
            else:
                file_name = 'S0' + str(season_number) + 'E' + str(episode_number)
            #print file_name
            subs = pysrt.open("subtitles/" + file_name + ".srt")
            total_text = ""
            for sub in subs:
                total_text += sub.text.replace('\n', ' ').replace('<i>', '').replace('</i>', '').replace("\'", '').replace("?", ' ')
            text[file_name] = total_text
            sentiment1[file_name] = afinn.score(total_text)
            blob = TextBlob(total_text)
            form = dict(text=total_text)
            r = requests.post("http://text-processing.com/api/sentiment/", data=form)
            sentiment2[file_name] = json.loads(r.text.encode("utf-8"))['probability']['neg']
            #sentiment2[file_name] = blob.sentiment.polarity
            #sentiment3[file_name] = senti_classifier.polarity_scores([total_text])


def get_seasons_text():
    episode_array = []
    for season_number in range(1, 6):
        for episode_number in range(1, 11):
            if(episode_number < 10):
                file_name = 'S0' + str(season_number) + 'E0' + str(episode_number)
            else:
                file_name = 'S0' + str(season_number) + 'E' + str(episode_number)
            #print file_name
            subs = pysrt.open("subtitles/" + file_name + ".srt")
            total_text = ""
            for sub in subs:
                total_text += sub.text.replace('\n', ' ').replace('<i>', '').replace('</i>', '').replace("\'", '').replace("?", ' ').replace(",", '')
            #print total_text
            episode_array.append({file_name: total_text.lower()})
            
    return episode_array


def show_sentiment_analysis():
    #for episode in sentiment.items():
        #print episode[0], episode[1]
    sentiment_sorted_episode_name = sorted(sentiment1.items(), key=operator.itemgetter(0))
    sentiment_sorted_sentiment = sorted(sentiment1.items(), key=operator.itemgetter(1))
    for episode in sentiment_sorted_sentiment:
        print episode[0], episode[1]
    #plt.plot(range(1,len(sentiment_sorted_episode_name) + 1), [val[1] for val in sentiment_sorted_episode_name], '--')
    print '---------------------------------'

    sentiment_sorted_episode_name2 = sorted(sentiment2.items(), key=operator.itemgetter(0))
    sentiment_sorted_sentiment2 = sorted(sentiment2.items(), key=operator.itemgetter(1))
    for episode in sentiment_sorted_sentiment2:
        print episode[0], episode[1]
    plt.plot(range(1,len(sentiment_sorted_episode_name2) + 1), [val[1] for val in sentiment_sorted_episode_name2], '--')
    plt.show()



#show_sentiment_analysis()

def requests_request_to_json(requests_request):
    # Extract the html of the request
    requestText = str(requests_request.text.encode("utf-8"))
    notUnicode = requestText.decode('unicode-escape')
    notUnicodeStr = str(notUnicode.encode("utf-8"))
    dJson = json.loads(notUnicodeStr)
    return dJson

def download_subtitle_file_from_episode(url, file_name):
    # first extract the download url
    r2 = requests.get(url)
    requestText = str(r2.text.encode("utf-8"))
    notUnicode = requestText.decode('unicode-escape')
    notUnicodeStr = str(notUnicode.encode("utf-8"))
    #print notUnicodeStr
    soup = BeautifulSoup(notUnicodeStr, 'html.parser')
    download_url = 'https://subscene.com' + select(soup, '#downloadButton')[0]['href']
    print download_url
    urllib.urlretrieve (download_url, file_name + ".zip")


def download_subtitles():
    #seasons = ['https://subscene.com/subtitles/game-of-thrones-first-season', 'https://subscene.com/subtitles/game-of-thrones-second-season', 'https://subscene.com/subtitles/game-of-thrones-third-season', 'https://subscene.com/subtitles/game-of-thrones-fourth-season', 'https://subscene.com/subtitles/game-of-thrones-fifth-season-2015']
    seasons = ['https://subscene.com/subtitles/game-of-thrones-fourth-season']
    season_counter = 4
    for season in seasons:
        r2 = requests.get(season)
        requestText = str(r2.text.encode("utf-8"))
        notUnicode = requestText.decode('unicode-escape')
        notUnicodeStr = str(notUnicode.encode("utf-8"))
        #print notUnicodeStr
        soup = BeautifulSoup(notUnicodeStr, 'html.parser')
        rows = select(soup, '.a1')

        for episode_number in range(1,2):
            if(episode_number < 10):
                file_name = 'S0' + str(season_counter) + 'E0' + str(episode_number)
            else:
                file_name = 'S0' + str(season_counter) + 'E' + str(episode_number)

            print file_name

            for row in rows:
                #print row
                soup = BeautifulSoup(str(row.encode("utf-8")), 'html.parser')
                spans = select(soup, 'a span')
                language = spans[0].text.strip()
                title = spans[1].text.strip()
                if(language == 'English'):
                    if(file_name in title):

                        print title
                        #print 
                        aTag = select(soup, 'a')
                        url = 'https://subscene.com' + aTag[0]['href']
                        print url
                        download_subtitle_file_from_episode(url, file_name)
                        break


        season_counter += 1

    # Go through every result 
    #row_attrs = extract_attributes_from_row_html(rows)
    



def count_phrases(phrase, ax, show_episodes = False, plot = False):
    phrase = phrase.lower()
    episodes = get_seasons_text()
    total_count = 0
    episode_count = []
    for episode in episodes:
        episode_text = episode.values()[0]
        episode_name =  episode.keys()[0]
        #print episode_text.count(phrase)
        occurence = episode_text.count(phrase)
        total_count += occurence
        if(show_episodes):
            if(occurence != 0):
                print episode_name
        episode_count.append(occurence)
    
    if(plot):
        ax.plot(range(1,len(episodes) + 1), [val for val in episode_count], '-', label=phrase)
        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        legend = ax.legend(loc='upper center', shadow=True)
        frame = legend.get_frame()
        frame.set_facecolor('0.90')

        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('large')

        for label in legend.get_lines():
            label.set_linewidth(1.5)  # the legend line width

    return {'total_count': total_count}


