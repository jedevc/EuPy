from . import executable

import unicodedata

def filter_nick(name):
    """
    filter_nick(name) -> String

    Process the name and get rid of all whitespace, invisible characters and
    make it all lower case.

    This function is intended to mimic euphoria's name pinging system, however
    it is slightly less pedantic, allowing for punctuation within names. It is
    what @NotBot uses for it's nick system.
    """

    ret = "".join(c for c in name if unicodedata.category(c)[0] not in ["C", "Z"])

    ret = "".join(ret.split())
    ret = ret.lower()

    return ret

def extract_time(seconds):
    """
    extract_time(seconds) -> String

    Turn the time in seconds to a string containing the time formatted into
    day, hours, minutes and seconds.
    """

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if d == 0 and h == 0 and m == 0:
        return "%ds" % s
    if d == 0 and h == 0:
        return "%dm %ds" % (m, s)
    elif d == 0:
        return "%dh %dm %ds" % (h, m, s)
    else:
        return "%dd %dh %dm %ds" % (d, h, m, s)
