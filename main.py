from db import Supabase
from scrapper import Scrapper
from updatestats import Stats

db = Supabase()

baseURL = "https://www.japscan.lol/"

scrapper = Scrapper(db, baseURL)
stats = Stats(db)

scrapper.scrap()
stats.update_stats()
