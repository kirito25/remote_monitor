def humanReadable(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "{:>5d}{}".format(int(num), x)
        num /= 1024.0
    return "{:>5d}{}".format(int(num), x)
