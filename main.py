from db import Supabase, Postgres
from scrapper import Scrapper
from updatestats import Stats

db = Supabase()
postgres = Postgres()

baseURL = "https://www.japscan.lol/"
bypassCloudflare = "http://localhost:8191/v1"

scrapper = Scrapper(postgres, baseURL, bypassCloudflare)
stats = Stats(db, postgres)

scrapper.scrap()
stats.update_stats()

postgres.close()

