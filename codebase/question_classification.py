from  nltk.parse.corenlp  import CoreNLPParser
from nltk.tree import *
from nltk import word_tokenize
import nltk.grammar
import os
import pprint
from nltk.corpus import wordnet
parser=None
label=[]
def classify_sent(head_words):
    i=0
    sim=0
    label=""
    
    dict={
    'geography':['location.n.01','sea.n.01','mountain.n.01'],
    'movie':['film.n.01','actor.n.01','Academy_Award.n.01'],
    'music':['track.n.01','album.n.01','artist.n.01']
    }
    try:
        for word in head_words:
            word1=word+'.'+'n'+'.'+'01'
            #print(word1)
            Gaga=wordnet.synset(word1)
            for x in dict:
                sim1=[]
                for c in dict[x]:
                    
                    w2=wordnet.synset(c)
                    num=w2.wup_similarity(Gaga)
                    #print(num)
                    sim1.append(num)
                #print(max(sim1))
                if max(sim1)>sim:
                    #print(sim1.max())
                    sim=max(sim1)
                    label=x
                    #print(label)
            if sim<0.5:
                continue
            else:
                return label   
        return label        
    except:
        #print('hi')
        return 'movie'
def ExtractPhrases( myTree, phrase):
    myPhrases = []
    
    
    #print(myTree)
    if (myTree.label() == phrase):
        
        #myPhrases.append(myTree.copy(True))
        myPhrases.extend(myTree.leaves())
        
        
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = ExtractPhrases(child, phrase)
            if (len(list_of_phrases)> 0):
                #print(list_of_phrases)
                myPhrases.extend(list_of_phrases)
    return myPhrases
def extract_head(parse):
    list_of_noun_phrases=['NN','NNP']
    list_of_verb_phrases=['VBZ','VBD', 'VB', 'VBN']
    head_words=[]
    head_words2=[]
    born =['born']
    code_words_movie=['director', 'Park','World', 'movie', 'actor', 'oscar']
    code_words_lie=['lie']
    code_words2=['directed', 'directs', 'direct', 'star','win', 'won']
    code_words=['Thriller', 'TheFame', '4', 'Artpop', '1989', 'Bad', 'True Blue', 'Rebel Heart', 'Crazy in Love',
'Baby Boy','Be With You',
'1+1',
'I Care',
'I Miss You',
'Best Thing I Never Had',
'Just Dance',
'Love Game',
'Aura',
'Venus',
'Thriller',
'Beat It',
'Bad',
'The Way You Make Me Feel',
'Speed Demon',
'Welcome To New York',
'Blank Space',
'White Heat',
'Papa Do not Preach',
'Open Your Heart',
'Devil Pray',
'Ghosttown', 'Gaga', 'Beyonce\'', 'Madonna', 'Beyonce', 'Swift']
    code_words_singer= ['Gaga', 'Beyonce\'', 'Madonna', 'Beyonce', 'Swift', 'artist', 'singer']
    
    for phrase in list_of_noun_phrases:
        result=ExtractPhrases(parse,phrase)
                  
        head_words.extend(result)

    for phrase2 in list_of_verb_phrases:
        result2=ExtractPhrases(parse,phrase2)
                  
        head_words2.extend(result2)
        
     
      #  print(head_words)
    for word in head_words:
        if word in code_words: 
            return "music"
        if word in code_words_movie:
            return "movie"
    xx=0;  
    for word2 in head_words2:
        if word2 in code_words2: 
            return "movie"
        if word2 in code_words_lie:
            return "geography"
        if word2 in born:
            for word in head_words:
                if word in code_words_singer: 
                    xx=1;
                    return "music"
            if xx==0:
                return "movie"
        
    
    label=classify_sent(head_words)
    return label


def load_question(q):
    parse = next(parser.raw_parse(q))
    result=extract_head(parse)
    return result
def initialize():
    global parser
    
    parser = CoreNLPParser(url='http://localhost:9000')
    
# with open('input.txt', 'r') as f:
    # for line in f:
        # print("<QUESTION> " + line+os.linesep)
        # parse = next(parser.raw_parse(line))
        # res=extract_head(parse)
        # label.append(res)
        # print("<CATEGORY> " + res+os.linesep)      
        # print("<PARSETREE>" + "\n")
        # parse.pretty_print()
        # print("\n")
    