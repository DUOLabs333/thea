#! /usr/bin/python3

from flask import Flask, render_template, request
from collections import Iterable
from spellchecker import SpellChecker
import json
import random
import requests

class ReverseProxied(object):
    ''' Fix to allow subfolder locations on the reverse proxy '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
''' Uncomment this if you are using a reverse proxy with a subfolder '''
#app.wsgi_app = ReverseProxied(app.wsgi_app)

def multireplace(dict, text):
  regex = re.compile("|".join(map(re.escape, dict.keys())))
  return regex.sub(lambda mo: dict[mo.group(0)], text)


def flatten(lists):
    for item in lists:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def findkeys(node, keyval):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, keyval):
               yield x
    elif isinstance(node, dict):
        if keyval in node:
            yield node[keyval]
        for j in node.values():
            for x in findkeys(j, keyval):
                yield x


def get_synonyms(word):
    synlists=None
    with open('mthesaur.txt') as words:
        for line in words:
            if line.split(',')[0].lower()==word.lower():
                synlists=line.split(',')[1:]

    if synlists:
        return synlists
    else:
        synlists = "No synonyms found"
        return synlists


def checkspelling(word):
    spell = SpellChecker()
    misspelled = spell.unknown([word])

    for w in misspelled:
        return list(spell.candidates(w))

@app.route('/')
def index():

    wordlist = open('words.txt')
    mode='index'
    line = next(wordlist)
    # Pick a random word from the word list file
    for num, line in enumerate(wordlist):
        if random.randrange(num + 2):
            continue
        word = line.rstrip("\n")
    wordlist.close()

    words = get_synonyms(word)

    return render_template(
        'index.html', word=word, synonyms=words)


@app.route('/words')
def get_words():
    word=request.args.get('q')
    mode='search'
    words = get_synonyms(word)

    return render_template(
        'index.html', word=word, synonyms=words,mode=mode)


''' Sends no-cache headers to browser, for easier web development '''
#@app.after_request
#def set_response_headers(response):
#    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#    response.headers['Pragma'] = 'no-cache'
#    response.headers['Expires'] = '0'
#    return response

''' Allows printing of debug msgs from jinga2 templates '''
#@app.context_processor
#def utility_functions():
#    def print_in_console(message):
#        print(str(message))

#    return dict(mdebug=print_in_console)



if __name__ == '__main__':
    app.config.update(TEMPLATES_AUTO_RELOAD=False)
    #app.config.update(TEMPLATES_AUTO_RELOAD=True)
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    #app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
    app.run(host='0.0.0.0', port=6001, threaded=True, debug=False)
