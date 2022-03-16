import subprocess


def test():
    """
    Run all unittests. Similar to: `python -m unittest discover`
    """
    subprocess.run(
        ['python', '-u', '-m', 'unittest', 'discover']
    )
