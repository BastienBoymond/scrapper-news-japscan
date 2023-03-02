class Scrapper:
    def __init__(self, db, baseURL):
        self.db = db
        self.baseURL = baseURL

    def return_soup(self, url):
        import requests
        from bs4 import BeautifulSoup
        try:
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup
            else :
                return None
        except:
            return None

    def find_things(self, soup, tag, text, need_split = False):
        things = soup.find_all(tag)
        for thing in things:
            if text in thing.text:
                if need_split:
                    return thing.text.replace(text, '').strip().split(',')
                else:
                    return thing.text.replace(text, '').strip()
    
    def scrap(self):
        content = self.db.get('mangas-names')
        for manga in content:
            url = self.baseURL + 'manga/' + manga['name'] + "/"
            soup = self.return_soup(url)
            list = []
            if not soup:
                continue
            chapters = soup.find('div', id="chapters_list");
            if not chapters:
                continue
            genres = self.find_things(soup, 'p', 'Genre(s):', True)
            types = self.find_things(soup, 'p', 'Type(s):', False)
            author = self.find_things(soup, 'p', 'Auteur(s):', False)
            artist = self.find_things(soup, 'p', 'Artiste(s):', False)
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
                list.append({'name': chapter_name, 'chapter': chapter_url.split('/')[-2]})
            list.reverse()
            exist = self.db.check_exist_string('japscan-chapter', 'manga_name', manga['name'])
            if exist:
                self.db.update_str('japscan-chapter', 'manga_name', manga['name'], {'chapitre_list': list, 'nb_chapitre': nbchapter, 'genres': genres, 'type': types, 'author': author, 'artist': artist, 'release-date': realease, 'synopsis': synopsis})
            else:
                self.db.insert('japscan-chapter', {'manga_name': manga['name'], 'chapitre_list': list, 'nb_chapitre': nbchapter, 'genres': genres, 'type': types, 'author': author, 'artist': artist, 'release-date': realease, 'synopsis': synopsis})
        return;
