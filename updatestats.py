class Stats:
    def __init__(self, db, postgres):
        self.db = db
        self.postgres = postgres

    def update_stats(self):
        import json
        content = self.postgres.get('japscan_chapter')
        usersStats = self.postgres.get('stats')
        for user in usersStats:
            genres_read = []
            for manga in content:
                if manga[0] in user[5]:
                    if manga[3] == None:
                        continue
                    for genre in manga[3]:
                        genre_exist = False
                        if genres_read == []:
                            genres_read.append({'genre': genre, 'nb': 1})
                            continue
                        for obj in genres_read:
                            if genre in obj['genre']:
                                genre_exist = True
                                obj['nb'] += 1
                        if not genre_exist:
                            genres_read.append({'genre': genre, 'nb': 1})
            if genres_read == []:
                continue
            self.postgres.update('stats', 'genres_read', (json.dumps(genres_read),), ("%s"), user[0])
        return;
# [{genre: Action, nb:1}, {genre: Romance, nb:1}]
