def humanReadable(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "{:>5.2f}{}".format(num, x)
        num /= 1024.0
    x = "TB"
    return "{:>5.2f}{}".format(num, x)
