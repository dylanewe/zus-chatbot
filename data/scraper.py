import requests
from bs4 import BeautifulSoup
import sqlite3

class ZusScraper():
    def __init__(self):
        self.outlets = []
        self.locations = []
        self.url = "https://zuscoffee.com/category/store/kuala-lumpur-selangor/"
        self.session = requests.Session()

    def run_scraper(self):
        while self.url:
            soup = self.get_html()
            if not self.get_data(soup):
                break
            self.get_next_page(soup)
        self.update_db()
        self.session.close()

    def get_html(self):
        try:
            res = self.session.get(self.url,timeout=10)
            res.raise_for_status()
            return BeautifulSoup(res.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")
            self.url = None
            return None

    def get_next_page(self, soup):
        if soup is None:
            self.url = None
            return
        page = soup.find("a",{"class":"page-numbers next"})
        self.url = str(page["href"]) if page else None

    def get_data(self, soup):
        if soup is None:
            return False
        
        page = soup.find("div", {"class":"elementor-posts-container"})
        if not page:
            return False
        
        outlet_elements = page.find_all("span", {"class":"entry-title"})
        location_elements = page.find_all("div", {"data-widget_type":"theme-post-content.default"})

        for element in outlet_elements:
            self.outlets.append(element.get_text(strip=True).lower())
        for element in location_elements:
            self.locations.append(element.find("p").get_text(strip=True).lower())

        return True

    def update_db(self):
        conn = sqlite3.connect('zus_outlets.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outlets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                outlet TEXT,
                location TEXT
            )
        """)

        for outlet, location in zip(self.outlets, self.locations):
            cursor.execute("""
                INSERT INTO outlets (outlet, location) VALUES (?, ?)
            """, (outlet, location))
        conn.commit()
        conn.close()


scraper = ZusScraper()
scraper.run_scraper()
    