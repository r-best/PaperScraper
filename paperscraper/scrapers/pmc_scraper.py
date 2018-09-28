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
        abstract = soup.find("div", {"id": "Abs1"}).findChildren("p")[0].contents
        abstract = [str(x) for x in abstract]
        return "".join(abstract)

    def get_body(self, soup):
        obj = {}
        self._get_body(soup.find("div", {"id": "ui-ncbiinpagenav-1"}), obj)
        return obj
    ##
    # Recursive helper function for get_body()
    ##
    def _get_body(self, section, obj):
        # Find subsections and paragraphs of the given section
        subsections = section.findChildren("div", {"class": "tsec sec"}, recursive=False)
        paragraphs = section.findAll("p", recursive=False)

        # For each subsection, create a blank entry for it and recurse into it
        for i in range(0, len(subsections)):
            obj["section"+str(i+1)] = {}
            self._get_body(subsections[i], obj["section"+str(i+1)])

            # If the entry didn't change after the recursion, it's pointless, delete it
            if obj["section"+str(i+1)] == {}:
                del obj["section"+str(i+1)]

        # For each paragraph, create an entry with its contents
        for i in range(0, len(paragraphs)):
            paragraph = [str(x) for x in paragraphs[i].contents]
            obj["p"+str(i+1)] = "".join(paragraph)

    def get_doi(self, soup):
        return soup.find("span", {"class": "doi"}).find("a").getText()

    def get_keywords(self, soup):
        return soup.find("span", {"class": "kwd-text"}).getText().split(", ")

    def get_pdf_url(self, soup):
        return self.website[0] + soup.find("div", {"class": "format-menu"}).find("li", text=re.compile(r'PDF\s\(\d\.\d\w\)')).find("a")['href']

    def get_title(self, soup):
        return soup.find("h1", {"class": "content-title"}).getText()
