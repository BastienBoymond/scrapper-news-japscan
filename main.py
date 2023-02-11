from db import Supabase
from scrapper import Scrapper

db = Supabase()

baseURL = "https://www.japscan.me/"

scrapper = Scrapper(db, baseURL)

scrapper.scrap()
