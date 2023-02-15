class Stats:
    def __init__(self, db):
        self.db = db

    def update_stats(self):
        content = self.db.get('japscan-chapter')
        usersStats = self.db.get('stats')
        for user in usersStats:
            for manga in content:
                if manga['manga_name'] in user['mangalist']:
                    for genre in manga['genres']:
                        genre_exist = False
                        if user['genres_read'] == []:
                            user['genres_read'].append({'genre': genre, 'nb': 1})
                            continue
                        for obj in user['genres_read']:
                            if genre in obj['genre']:
                                genre_exist = True
                                obj['nb'] += 1
                        if not genre_exist:
                            user['genres_read'].append({'genre': genre, 'nb': 1})
                    self.db.update('stats', "id" ,user['id'], {'genres_read': user['genres_read']})

# [{genre: Action, nb:1}, {genre: Romance, nb:1}]
