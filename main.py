from db import Supabase
from scrapper import Scrapper

db = Supabase()

baseURL = "https://www.japscan.me/"
# bypassCloudflare = "http://localhost:8191/v1"

scrapper = Scrapper(db, baseURL)

scrapper.scrap()
