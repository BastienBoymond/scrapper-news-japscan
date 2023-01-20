class Scrapper:
    def __init__(self, db, baseURL, bypassCloudflare):
        self.db = db
        self.baseURL = baseURL
        self.bypassCloudflare = bypassCloudflare

    def return_soup(self, url):
        import requests
        from bs4 import BeautifulSoup
        try:
            r = requests.post(self.bypassCloudflare, json={"url": url, "cmd":"request.get"}, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                json = r.json()
                soup = BeautifulSoup(json['solution']['response'], 'html.parser')
                return soup
            else :
                return None
        except:
            return None

    def scrap(self):
        content = self.db.get('mangas-names')
        for manga in content:
            print(manga)
            url = self.baseURL + 'manga/' + manga['name'] + "/"
            soup = self.return_soup(url)
            # print(soup)
            list = []
            if soup:
                chapters = soup.find('div', id="chapters_list");
                if not chapters:
                    continue
                chapters_list = chapters.find_all('a', class_="text-dark")
                nbchapter = len(chapters_list)
                for chapter in chapters_list:
                    chapter_url = chapter['href']
                    chapter_name = chapter.text.strip()
                    print(chapter_url.split('/')[-2], chapter_name)
                    list.append({'name': chapter_name, 'chapter': chapter_url.split('/')[-2]})
                list.reverse()
                exist = self.db.check_exist_string('japscan-chapter', 'manga_name', manga['name'])
                if exist:
                    self.db.update_str('japscan-chapter', 'manga_name', manga['name'], {'chapitre_list': list, 'nb_chapitre': nbchapter})
                else:
                    self.db.insert('japscan-chapter', {'manga_name': manga['name'], 'chapitre_list': list, 'nb_chapitre': nbchapter})

        print(content)
        pass;

