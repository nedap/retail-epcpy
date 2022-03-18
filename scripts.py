import subprocess


def test():
    """Run all unittests. Similar to: `python -u -m unittest discover`"""
    subprocess.run(["python", "-u", "-m", "unittest", "discover"])
