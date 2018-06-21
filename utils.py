import socket


def humanReadable(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "{:>5.2f}{}".format(num, x)
        num /= 1024.0
    x = "TB"
    return "{:>5.2f}{}".format(num, x)


def exist(host):
    """
    :param host: an ip address as a string
    :return: the name of the host or False if it does
            not exist
    """
    try:
        return socket.gethostbyaddr(host)[0]
    except:
        return False