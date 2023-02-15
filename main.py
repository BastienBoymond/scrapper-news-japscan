from db import Supabase
from scrapper import Scrapper

db = Supabase()

baseURL = "https://www.japscan.lol/"

scrapper = Scrapper(db, baseURL)

scrapper.scrap()
