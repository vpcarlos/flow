import subprocess


class Shell:

    @staticmethod
    def run(command: str):
        sb = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sb.stdout.read()
        return f"{subprocess_return.decode('utf8').strip()}"
