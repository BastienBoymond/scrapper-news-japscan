from db import Supabase, Postgres
from scrapper import Scrapper
from updatestats import Stats

db = Supabase()
postgres = Postgres()

baseURL = "https://www.japscan.lol/"

scrapper = Scrapper(postgres, baseURL)
stats = Stats(db, postgres)

scrapper.scrap()
stats.update_stats()

postgres.close()

