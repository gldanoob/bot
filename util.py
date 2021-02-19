# Parsing commands in the format:
# $commands param1 param2 'param of multiple words'
def parse(msg):
    params = []
    tmp = ''
    in_quotes = False
    for c in msg:
        if c == '`':
            in_quotes = not in_quotes
        elif c == ' ' and not in_quotes:
            if len(tmp):
                params.append(tmp)
                tmp = ''
        else:
            tmp += c
    if len(tmp):
        params.append(tmp)
    return params

def get_channel(msg, id):
    return msg.guild.get_channel(int(id))