class Scrapper:
    def __init__(self, postgres, baseURL, bypassCloudflare):
        self.postgres = postgres
        self.baseURL = baseURL
        self.bypassCloudflare = bypassCloudflare
        self.cloudflareActive = False

    def run_cloudflare_bypass(self, url):
        import requests
        from bs4 import BeautifulSoup
        try: 
            r = requests.post(self.bypassCloudflare, json={"url": url, "cmd":"request.get"}, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                json = r.json()
                soup = BeautifulSoup(json['solution']['response'], 'html.parser')
                return soup
            else:
                return None
        except:
            return None

    def return_soup(self, url):
        import requests
        from bs4 import BeautifulSoup
        if not self.cloudflareActive:
            try:
                r = requests.get(url);
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    return soup
                else :
                    self.cloudflareActive = True
                    return  self.run_cloudflare_bypass(url)
            except:
                self.cloudflareActive = True
                return  self.run_cloudflare_bypass(url)
                
        else:
            return self.run_cloudflare_bypass(url)

    def find_things(self, soup, tag, text, need_split = False):
        things = soup.find_all(tag)
        for thing in things:
            if text in thing.text:
                if need_split:
                    return thing.text.replace(text, '').strip().replace('\t', '').split(',')
                else:
                    return thing.text.replace(text, '').strip()
    
    def scrap(self):
        content = self.postgres.get('mangas_names')
        for manga in content:
            url = self.baseURL + 'manga/' + manga[1] + "/"
            soup = self.return_soup(url)
            listChap = []
            if not soup:
                continue
            chapters = soup.find('div', id="chapters_list");
            print(chapters)
            if not chapters:
                continue
            genres = self.find_things(soup, 'p', 'Genre(s):', True)
            types = self.find_things(soup, 'p', 'Type(s):', False)
            author = self.find_things(soup, 'p', 'Auteur(s):', False)
            artist = self.find_things(soup, 'p', 'Artiste(s):', False)
            names = self.find_things(soup, 'p', 'Nom(s) Alternatif(s):', True)
            realease = self.find_things(soup, 'p', 'Date Sortie:', False)
            synopsis = soup.find('p', class_="list-group-item")
            if synopsis:
                synopsis = synopsis.text.strip()
            else:
                synopsis = ''
            chapters_list = chapters.find_all('a', class_="text-dark")
            nbchapter = len(chapters_list)
            for chapter in chapters_list:
                chapter_url = chapter['href']
                chapter_name = chapter.text.strip()
                listChap.append({'name': chapter_name, 'chapter': chapter_url.split('/')[-2]})
            listChap.reverse()
            import json
            exist = self.postgres.check_if_exist_string('japscan_chapter', 'manga_name', manga[1])
            if exist:
                self.postgres.update_str('japscan_chapter', 'manga_name', manga[1], "(chapitre_list, nb_chapitre, genres, type, author, artist, release_date, alternative_name, synopsis)", (json.dumps(listChap), nbchapter, json.dumps(genres), types, author, artist, realease, json.dumps(names), synopsis), "(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            else:
                self.postgres.insert('japscan_chapter', "(manga_name, chapitre_list, nb_chapitre, genres, type, author, artist, release_date, alternative_name, synopsis)", (manga[1], json.dumps(listChap), nbchapter, json.dumps(genres), types, author, artist, realease, json.dumps(names), synopsis), "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        return;
