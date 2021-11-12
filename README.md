# Thea
Self-hosted web-based thesaurus written in Python 3. Fork of [Synonym-web](https://github.com/andyforceno/synonym-web). I didn't want to rely on an external API, so here we are. I also removed a lot of things to make the interface more minimal.

With Thea you can: query for words in your browser and get synonyms. It also offers spelling suggestions for mispelled words

Depends on pyspellchecker (https://github.com/barrust/pyspellchecker), Flask, Requests, and CherryPy (see requirements.txt)

## Installation:
    git clone https://github.com/andyforceno/synonym-web.git
    cd synonym-web/
    (Setting up a virtual environment is a good idea, but not covered here)
    pip install -r requirements.txt
    cd app/ 
	python3 wsgi.py
    Browse to http://localhost:6001 (can be changed with environment variable `PORT`

## Attribution:
Synonyms are from Gutenburg: 
https://www.gutenberg.org/files/3202/files/mthesaur.txt
