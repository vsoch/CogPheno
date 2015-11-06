from textblob import Word

def get_synsets(concept_name):
    word = Word(concept_name)
    return word.get_synsets()

