# save_cookies.py
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.linkedin.com/login")
    print("🔑 Please log in manually... then press Enter here.")
    input()

    context.storage_state(path="linkedin_cookies.json")
    browser.close()
