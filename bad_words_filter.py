def clean_text(text):
    bad_words = ["badword1", "badword2"]
    for word in bad_words:
        text = text.replace(word, "***")
    return text
