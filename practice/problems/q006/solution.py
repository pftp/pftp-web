def first_word(sentence):
    return sentence.split(' ')[0]
print first_word('{{ random_sentence:s1 }}')
