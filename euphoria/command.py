class Command:
    """
    The Command class allows you to parse and read bot commands. This includes
    the main command, the arguments and the flags.
    """

    def __init__(self, text):
        self.text = text

        self.command = ""
        self.flags = {}
        self.args = []

    def parse(self):
        """
        parse() -> None

        Perform the parsing.
        """

        parts = self.text.split()

        if len(parts) == 0:
            return

        if parts[0][0] == '!':
            self.command = parts[0][1:]

        for p in range(1, len(parts)):
            if parts[p][0] == '-':
                if '=' in parts[p]:
                    flag = parts[p][1:].split('=')
                    self.flags[flag[0]] = flag[1]
                else:
                    self.flags[parts[p][1:]] = None
            else:
                self.args.append(parts[p])
