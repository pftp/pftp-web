def get_word_counts(list_of_words):
    word_counts = {}
    for word in list_of_words:
        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word] += 1
    return word_counts
