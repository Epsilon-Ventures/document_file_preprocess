import re

def preprocess_text():
  with open('./ques/ques.txt', 'r') as file:
    text = file.read()
    only_questions = text.split("Attempt all the questions.")[-1]
    seperate_questions = re.sub(r'(\.|\?)\t', r'\n',only_questions)
    remove_extraline = re.sub(r'^\s*\n', '', seperate_questions, flags=re.MULTILINE)
    remove_tabs = re.sub(r'\t', ' ', remove_extraline)
    split_questions = remove_tabs.split("\n")
    return [[questions] for questions in split_questions]
