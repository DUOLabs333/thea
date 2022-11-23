import readline,json,os,signal
from spellchecker import SpellChecker

thesaur={}

if 1:
    with open(os.path.join(os.path.dirname(__file__),'thesaur.txt'),'r') as words:
        for line in words:
            word=line.split(',')[0].lower()
            synlists=line.split(',')[1:]
            if word not in thesaur:
                thesaur[word]=synlists
            else:
                thesaur[word].extend(synlists)
else:
    thesaur=json.load(open(os.path.join(os.path.dirname(__file__),'thesaur.json'),'r'))

results=[]
prev_word=""
curr_word=""
def get_synonyms(word):
    return thesaur[word] if word in thesaur else []

def checkspelling(word):
    spell = SpellChecker()
    misspelled = spell.unknown([word])
    for w in misspelled:
        return [_ for _ in list(spell.candidates(w) or []) if _.lower() in thesaur]

def _exit(a,b):
    print()
    exit()

def format_results(_list,offset=0):
    return ", ".join([f"{offset+i+1}. {e}" for i,e in enumerate(_list)])
    
signal.signal(signal.SIGINT,_exit)        
while True:
    word=input("Enter word to search: ")
    word=word.strip().lower()
    if word=="0":
        word=curr_word
    elif word=="-1":
        word=prev_word
    if word.isnumeric():
        if not results:
            print(f"Previous word {prev_word} did not have any results")
        elif int(word)<-1 or int(word)>len(results):
            print("Can't do that")
            continue
        word=results[int(word)-1]
    prev_word=curr_word
    curr_word=word
    print("Word: "+word)
    
    results=checkspelling(word)
    if results:
        print(f"{word} not found. Did you mean:")
    else:
        results=get_synonyms(word)
        if not results:
            print("No synonyms found")
            results=[]
    printed_results=[]
    d=10
    parts=len(results)//d
    remainder=len(results)%parts
    offset=0
    for i in range(remainder):
        printed_results.append(format_results(results[offset:offset+d+1],offset))
        offset+=d+1

    for i in range(parts-remainder):
        printed_results.append(format_results(results[offset:offset+d],offset))
        offset+=d
    
    print('\n\n'.join(printed_results))
