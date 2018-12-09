# Mitchell Rudoll and Oliver Whittlef

# Inspiration drawn from NLTK Eliza, https://github.com/lizadaly/brobot/blob/master/broize.py,
# and https://github.com/parulnith/Building-a-Simple-Chatbot-in-Python-using-NLTK/blob/master/chatbot.py

# IMPORTS

from __future__ import print_function, unicode_literals
import nltk
from nltk.corpus import wordnet
import numpy as np
import random
import string
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import io
import os.path as path
import warnings
warnings.filterwarnings("ignore")
from textblob import TextBlob
from .config import *
from .interaction import findDrugInteractions
from .rxnorm import rxNormId
from nltk.corpus import stopwords

# DATA LOADING

p = path.abspath(path.join(__file__, "../../.."))

os.environ['NLTK_DATA'] = p + '/nltk_data/'

# make sure required files are downloaded, but don't print to console
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'corpora.txt')
f=open(file_path, 'r', errors= 'ignore')
raw=f.read()
raw=raw.lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

stop_words = set(stopwords.words('english'))

# Dictionary of drug names used

# dictionary of form RxNormId : {UserName : OfficialName}
user_drug_names = {}

# API CALLS

# CLASSES

class NoNoWordsException(Exception):
    """Response triggered blacklist"""
    pass
1
# FUNCTIONS

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def add_to_client_drug_names(rxNormId, dictPair):
    user_drug_names[rxNormId] = dictPair
    return True

def get_from_client_drug_names(rxNormId):
    return user_drug_names[rxNormId]

def starts_with_vowel(word):
    """Check for pronoun compability -- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False

def find_pronoun(sent):
    """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
    pronoun is found in the input"""
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # Disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word.lower() == 'your':
            pronoun = 'my'
        elif part_of_speech == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            pronoun = 'You'
    return pronoun

def find_verb(sent):
    """Pick a candidate verb for the sentence."""
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):  # This is a verb
            verb = word
            pos = part_of_speech
            break
    return verb, pos


def find_noun(sent):
    """Given a sentence, find the best candidate noun."""
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':  # This is a noun
                noun = w
                break

    return noun

def find_adjective(sent):
    """Given a sentence, find the best candidate adjective."""
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':  # This is an adjective
            adj = w
            break
    return adj

def preprocess_text(sentence):
    """Handle some weird edge cases in parsing, like 'i' needing to be capitalized
    to be correctly identified as a pronoun"""
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)

def construct_response(pronoun, noun, verb):
    """No special cases matched, so we're going to try to construct a full sentence that uses as much
    of the user's input as possible"""
    resp = []

    if pronoun:
        resp.append(pronoun)
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!
            resp.append(verb_word)
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    return " ".join(resp)

def check_for_comment_about_bot(pronoun, noun, adjective, verb):
    # checks if the user's response is about the bot
    resp = None
    if pronoun == 'I' and verb == 'are':
        resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective' : adjective })
    elif pronoun == 'I' and (noun or adjective):
        if noun:
            if random.choice((True, False)):
                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        else:
            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
    return resp

def check_for_greeting(input):
    resp = None
    # input_parsed = input.lower().split(" ")
    if("whats up" in input.lower() or "what's up" in input.lower()):
        resp = "The sky <span class='emoji'>🙄</span>"
    for word in GREETING_INPUTS:
        if " " + word + " " in input.lower():
            resp = random.choice(GREETING_RESPONSES).capitalize()
    return resp

def check_for_goodbye(input):
    resp = None
    for word in GOODBYE_INPUTS:
        if word in input.lower():
            resp = random.choice(GOODBYE_RESPONSES).capitalize()
    return resp

def check_for_mention_of_drugs(input):
    resp = ""
    stopwords_drugs = stop_words;
    stopwords_drugs.update(DRUGS_STOP_WORDS)
    potential_drugs = []
    for sent in input.sentences:
        for word, typ in sent.pos_tags:
            if typ in ("RB", "CC", "NN", "JJ") and word not in stopwords_drugs:
                potential_drugs.append(word)
    if(len(potential_drugs) < 2):
        return resp
    rxnorms = map(rxNormId, potential_drugs)
    rxnorms = list(filter(None, rxnorms))
    if(len(rxnorms) < 2):
        return resp
    drugInteractionsDict = findDrugInteractions(rxnorms)
    if(len(drugInteractionsDict) < 1):
        return resp
    resp = random.choice(INTERACTION_PREFIXES) + " "
    for i in drugInteractionsDict.values():
        # print(i)
        resp += "<br>" + i
    return resp
#     resp = ""
#     drugs = []
#     if input.find("are") >= 0:
#         drugs = [str(d).strip() for d in input[input.index("are"):].split()]
#     elif input.find("taking") >= 0:
#         drugs = [str(d).strip() for d in input[input.index("taking"):].split()]
#     elif input.find("check") >= 0:
#         drugs = [str(d).strip() for d in input[input.index("check"):].split()]
#     elif input.find("thank") >= 0:
#         drugs = [str(d).strip() for d in input[:input.index("thank")].split()]
#     if(len(drugs) > 0):
#         drugInteractionsDict = findDrugInteractions(map(rxNormId, drugs))
#         for i in drugInteractionsDict.values():
#             resp += i + " "
#         if not resp:
#             resp = "I couldn't find anything. Would you like me to ask Siri?"
#     return resp
#
# def check_for_comment_about_drugs(pronoun, noun, adjective):
#     """Check if the user's input was about drugs, in which case try to fashion a response
#     that feels right based on their input. Returns the new best sentence, or None."""
#     resp = None
#     if noun and noun.lower() in ["drugs", "medicine", "medication"]:
#         names = ('tylenol', 'ibuprofen', 'viagra')
#         resp = str(findDrugInteractions(map(rxNormId, names)))
#     return resp

def find_candidate_parts_of_speech(parsed):
    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    return pronoun, noun, adjective, verb

def filter_response(resp):
    """Don't allow any words to match our filter list"""
    tokenized = resp.split(' ')
    for word in tokenized:
        for s in FILTER_WORDS:
            if word.lower().startswith(s):
                raise NoNoWordsException()

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greeting(sentence):
    # TODO: change split to .words
    for word in sentence.words:
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def respond(sentence):
    """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    # Loop through all the sentences, if more than one. This will help extract the most relevant
    # response text even across multiple sentences (for example if there was no obvious direct noun
    # in one sentence
    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    # If we said something about the bot and used some kind of direct noun, construct the
    # sentence around that, discarding the other candidates

    # resp = check_for_comment_about_bot(pronoun, noun, adjective)
    resp = None
    if not resp:
        resp = check_for_mention_of_drugs(parsed)
    # if not resp:
    #     resp = check_for_comment_about_drugs(pronoun, noun, adjective)
    if not resp:
        resp = check_for_greeting(parsed)
    if not resp:
        resp = check_for_goodbye(parsed)
    if not resp:
        resp = check_for_comment_about_bot(pronoun, noun, adjective, verb)

    # if we get through our rules, just respond using a corpora
    if not resp:
        resp = converse_normal(sentence)

    # will just say it doesn't know what's going on as an absolute last check to make sure there's a response
    if not resp:
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif not resp:
            resp = construct_response(pronoun, noun, verb)
        else:
            resp = random.choice(NONE_RESPONSES)
    # make sure we don't say anything obviously offensive
    filter_response(resp)

    return resp

def respond_normal(sentence):
    resp = ''
    sent_tokens.append(sentence)
    TfidVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        resp = resp + "I apologize, but I don't understand what you're saying."
    else:
        resp = resp + sent_tokens[idx]
        return resp

#DRIVER

def converse(sentence):
    resp = respond(sentence)
    return resp

def converse_normal(sentence):
    resp = respond_normal(sentence)
    return resp

if __name__ == '__main__':
    print("Bot: Hello, my name is Dr. Web MD. Please feel free to ask me any questions you may have regarding the medicines you're taking.")
    while(True):
        resp = input('> ')
        print(converse(resp))
