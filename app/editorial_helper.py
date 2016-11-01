from bs4 import BeautifulSoup


def get_editorial_content(html_doc):
    bs = BeautifulSoup(html_doc)
    content = ''.join((p.text for p in bs.findAll('p', {'class': 'body'}))).replace('\n', '')
    return content
