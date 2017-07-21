from bs4 import BeautifulSoup

def parseCase(html):
    soup = BeautifulSoup(html, 'html.parser')
    # TODO: Everything
    return {}

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
