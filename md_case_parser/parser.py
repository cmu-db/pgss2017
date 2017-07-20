from bs4 import BeautifulSoup
from gethtml import getCaseHTML

def parseCase(html):
    soup = BeautifulSoup(html, 'html.parser')
    # TODO: Everything

parseCase(getCaseHTML())
