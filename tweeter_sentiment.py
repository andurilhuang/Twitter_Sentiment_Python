from data.uw_ischool_sample import SAMPLE_TWEETS
from data.sentiments_nrc import SENTIMENTS
from data.sentiments_nrc import EMOTIONS
from functools import reduce
import re
import requests

def split_text_string(text_string):
    """this is to split the text string into list of words and make it lower case"""    
    text_string = str.lower(text_string)
    splited = re.split('\W+', text_string)
    word_list=[]
    for word in splited:
        if len(word)>1:
            word_list.append(word)
    return word_list        

def emotion_filter(emotion,words):
    emotion_list=[]
    """word filtering based on emotion"""    
    for word in words:
        if word in list(SENTIMENTS.keys()):
            if SENTIMENTS.get(word).get(emotion) == 1:
                emotion_list.append(word)
            
    return emotion_list    

def emotion_dict(text_string):
    """ which words from a list have each emotion"""   
    return {emotion: list(emotion_filter(emotion,text_string)) for emotion in EMOTIONS}
    
def sort_word_freq(words):
    """count word frequencies and sort"""
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] = word_freq[word] + 1
        else:
            word_freq[word] = 1  
    sorted_word_freq = sorted(word_freq.keys(), key = lambda word: word_freq[word], reverse = True)    
    return sorted_word_freq
    
#sort_word_freq(['a','b','c','c','c','a'])
#-----------------analyze tweets---------------#
def tweet_words_count(tweets):
    """this is to count all the words of the tweets"""
    """this is used to calculate pct later"""
    tweet_word = []
    for tweet in tweets:
        tweet_to_word = split_text_string(tweet['text'])
        for word in tweet_to_word:
            tweet_word.append(word)
    return len(tweet_word)   
    
    
def analyze_tweets(tweets):
    """for each tweet, pull out its emotion and hashtags as dics in a list"""
    pull_list_1 = []
    for tweet in tweets:
        tweet_to_word = split_text_string(tweet['text'])
        result = emotion_dict(tweet_to_word)
        
        result['hashtags'] = []
        if tweet['entities']['hashtags'] != []:
            for i in range(len(tweet['entities']['hashtags'])):
                result['hashtags'].append(tweet['entities']['hashtags'][i]['text'].lower())
        pull_list_1.append(result)
        
    """start analyze_tweets"""
    pull_list_2 = []    
    for emotion in EMOTIONS:
        result = {'EMOTION' : emotion, 'words':[], '% of WORDS':[], 'EXAMPLE WORDS':[], 'NOHASHTAG':[], 'HASHTAG':[]}
        for dict in pull_list_1:
            if dict[emotion] != []:
                result['words']= result['words']+dict[emotion]
                result['% of WORDS'] = str(round((len(result['words'])/tweet_words_count(tweets))*100,2)) +'%'
                result['EXAMPLE WORDS']=sort_word_freq(result['EXAMPLE WORDS']+dict[emotion])[:3]
                if dict['hashtags']!=[]:
                    hash = []
                    result['NOHASHTAG']=sort_word_freq(result['NOHASHTAG']+dict['hashtags'])[:3]
                    for h in result['NOHASHTAG']:
                        hash.append('#'+h)
                        result['HASHTAG'] = hash
        result.pop("words")
        result.pop("NOHASHTAG")
        pull_list_2.append(result)  
        analysis =  pull_list_2
    
    return analysis

def display(analysis):
    """display the resulst from analyze_tweets"""
    print ('{:<14s} {:<11s} {:<35s} {:<70s}'. format('EMOTION','% of WORDS', 'EXAMPLE WORDS', 'HASHTAG'))
    for i in analysis:
       print ('{:<14s} {:<11s} {:<35s} {:<70s}'. format(i['EMOTION'],i['% of WORDS'], ', '.join(i['EXAMPLE WORDS']),', '.join (i['HASHTAG'])))
        
def get_data(name):
    '''tweeter api call'''
    auth = {'screen_name': str(name)}
    response = requests.get('https://faculty.washington.edu/joelross/proxy/twitter/timeline/', params=auth)
    tweets = response.json()
    return tweets        


if __name__ == '__main__':
    name = input('Screenname: ')
    if name == 'SAMPLE':
        tweets = SAMPLE_TWEETS
    else:
        tweets = get_data(name)
    
    display(analyze_tweets(tweets))

        
