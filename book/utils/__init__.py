def simple_bb(text):
    tags = ['SIZE', 'FONT', 'B', 'COLOR', 'U', 'I', 'URL', 'IMG']
    for tag in tags:
        text = text.replace("[/%s]" % tag, "")
        open_tag = "[%s" % tag
        index = text.find(open_tag)
        if index != -1:
            while index != -1:
                last_index = text.find("]", index)
                text = text[:index] + text[(last_index + 1):]
                index = text.find(open_tag)

    return text
