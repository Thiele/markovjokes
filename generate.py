import json
import markovify

### LOADING
jokes = []
with open('stupidstuff.json') as json_data:
    tmp_jokes = json.load(json_data)
    for d in tmp_jokes:
        try:
            jokes.append(d["body"])
        except:
            pass
with open('wocka.json') as json_data:
    wocka = json.load(json_data)
    for d in wocka:
        try:
            jokes.append(d["body"])
        except:
            pass

with open('reddit_jokes.json') as json_data:
    reddit = json.load(json_data)
    for d in reddit:
        try:
            jokes.append(d["title"]+" "+d["body"])
        except:
            pass

def replace_special_characters(jokes):
    tmp_jokes = []
    for j in jokes:
        tmp_jokes.append(j.replace('\r',' ').replace('\n', ' ').replace("'",""))
    return tmp_jokes

def lower(jokes):
    tmp_jokes = []
    for j in jokes:
        tmp_jokes.append(j.lower())
    return tmp_jokes

def remove_long_jokes(jokes, l):
    tmp_jokes = []
    for j in jokes:
        if len(j) <= l:
            tmp_jokes.append(j)
    return tmp_jokes

def replace(jokes, needle, r):
    tmp_jokes = []
    for j in jokes:
        tmp_jokes.append(j.replace(needle,r))
    return tmp_jokes

def remove_empty(jokes):
    tmp_jokes = []
    for j in jokes:
        if len(j) > 0:
            tmp_jokes.append(j)
    return tmp_jokes

### PREPROCESSING
tmp_jokes = []
for j in jokes:
    joke = j
    while "..." in joke:
        joke = joke.replace("...","..")
    tmp_jokes.append(joke)
jokes = tmp_jokes

jokes = replace(jokes, "."," DOT ")
jokes = replace(jokes, "?"," QUESTIONMARK ")
jokes = replace_special_characters(jokes)
jokes = lower(jokes)
jokes = remove_long_jokes(jokes, 80)
jokes = remove_empty(jokes)

#Now we have the jokes. Generate some original ones
text_model = markovify.NewlineText(jokes, state_size=4)
generated_jokes = []
while len(generated_jokes) <= 500:
    joke = text_model.make_sentence()
    if not joke == None and joke not in generated_jokes:
        clean_joke = joke.replace(" dot",".").replace(" questionmark", "?")
        generated_jokes.append(clean_joke)

with open("generated_jokes.json", "w") as f:
    f.write(json.dumps(generated_jokes))
