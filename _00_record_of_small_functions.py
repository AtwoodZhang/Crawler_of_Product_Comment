import sys


def judge_url_whole(url_address):
    if url_address[0] == '/' or url_address[0] != 'h':
        url_address = "https://www.macys.com" + url_address
    return url_address


def judge_url_whole2(url):
    if url[0] == '/' or url[0] != 'h':
        url_new = 'https://www.macys.com' + url
    elif isinstance(url, list):
        url_new = url[0]
    else:
        url_new = url
    return url_new


class Logger(object):
    def __init__(self, file_name='Default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(file_name, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
