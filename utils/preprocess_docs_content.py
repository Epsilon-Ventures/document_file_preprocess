# This is only testing

with open('../ques/ques.txt', 'r') as file:
  text = file.read()
  bool = text.split("Attempt all the questions.")[1]
  print(bool)