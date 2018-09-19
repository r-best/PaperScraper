from paperscraper.scrapers.base.base_scraper import BaseScraper
import re
"""A scraper of a PMC articles"""

class PMC(BaseScraper):

    def __init__(self,driver):
        self.driver = driver
        self.website = ["ncbi.nlm.nih.gov"]

    def get_authors(self, soup):
        author_links = soup.find("div", {"class": "contrib-group fm-author"}).findAll("a")
        authors = {}

        for i in range(len(author_links)):
            authors['a'+str(i+1)] = {'last_name':author_links[i].contents[0].split(" ")[-1], 'first_name':author_links[i].contents[0].split(" ")[0]}

        return authors

    def get_abstract(self,soup):
        #TODO get working
        pass
        #abstract = soup.find("div", id=lambda x: x and x.startswith('__abstract'))
        # print(abstract)
        # print(soup.find("p", id="__p1"))
        # [tag.unwrap() for tag in abstract.findAll(["em", "i", "b", "sub", "sup"])]
        # return abstract.find("p").contents[0]
        return soup.find(id="Abs1").contents

    def get_body(self, soup):
        #TODO get working
        pass

    def get_doi(self, soup):
        return soup.find("span", {"class": "doi"}).find("a").getText()

    def get_keywords(self, soup):
        return soup.find("span", {"class": "kwd-text"}).getText().split(", ")

    def get_pdf_url(self, soup):
        return self.website[0] + soup.find("div", {"class": "format-menu"}).find("li", text=re.compile(r'PDF\s\(\d\.\d\w\)')).find("a")['href']

    def get_title(self, soup):
        return soup.find("h1", {"class": "content-title"}).getText()
