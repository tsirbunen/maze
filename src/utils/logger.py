class Logger:

    @staticmethod
    def logPink(message):
        print(f"\033[95m{message}\033[00m")

    @staticmethod
    def logYellow(message):
        print(f"\033[93m{message}\033[00m")

    @staticmethod
    def logGreen(message):
        print(f"\033[92m{message}\033[00m")

    @staticmethod
    def logBlue(message):
        print(f"\033[94m{message}\033[00m")

