import chardet


def get_stop_words(stop_words_file):
    stop_words = ""
    with open(stop_words_file, 'rb') as f:
        input_str = f.read()
        encoding = chardet.detect(input_str)['encoding']
        stop_words = input_str.decode(encoding)
    stop_words_list = stop_words.splitlines()
    return stop_words_list
