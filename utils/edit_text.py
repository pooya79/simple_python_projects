MAXIMUM_CHAR_PER_LINE = 15

def edit_text(text):
    number_of_new_lines = (len(text) - 1) // MAXIMUM_CHAR_PER_LINE
    for i in range(number_of_new_lines):
        text = text[:MAXIMUM_CHAR_PER_LINE+(MAXIMUM_CHAR_PER_LINE + 2)*i] + '\n'\
               +text[MAXIMUM_CHAR_PER_LINE+(MAXIMUM_CHAR_PER_LINE + 2)*i : ]

    return text