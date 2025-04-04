import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

# 🔁 Replace with real LinkedIn profile URLs (public or network-visible)
profile_urls = [
    "https://www.linkedin.com/in/sampleprofile1/",
    "https://www.linkedin.com/in/sampleprofile2/"
]

async def extract_profile_data(page):
    try:
        # ⏳ Wait for main content to load (fallback if selector fails)
        await page.wait_for_selector('section.pv-profile-section', timeout=15000)
    except:
        print("⚠️  Main profile content not found, skipping.")
        await page.screenshot(path="profile_debug.png", full_page=True)
        return None

    data = {
        "education": [],
        "roles": [],
        "skills": [],
        "certifications": [],
        "groups": []
    }

    # 🧠 Work Experience
    roles = await page.query_selector_all('.experience-section li')
    for role in roles:
        try:
            title = await role.query_selector('h3')
            company = await role.query_selector('.pv-entity__secondary-title')
            years = await role.query_selector('.pv-entity__date-range span:nth-child(2)')
            if title and company:
                data["roles"].append({
                    "title": (await title.inner_text()).strip(),
                    "company": (await company.inner_text()).strip(),
                    "years": (await years.inner_text()).strip() if years else None
                })
        except:
            continue

    # 🎓 Education
    schools = await page.query_selector_all('.education-section li')
    for school in schools:
        try:
            name = await school.query_selector('h3')
            degree = await school.query_selector('.pv-entity__degree-name span:nth-child(2)')
            field = await school.query_selector('.pv-entity__fos span:nth-child(2)')
            year = await school.query_selector('.pv-entity__dates span:nth-child(2)')
            data["education"].append({
                "school": (await name.inner_text()).strip() if name else None,
                "degree": (await degree.inner_text()).strip() if degree else None,
                "field": (await field.inner_text()).strip() if field else None,
                "year": (await year.inner_text()).strip() if year else None
            })
        except:
            continue

    # 🛠 Skills
    skill_elements = await page.query_selector_all('.pv-skill-category-entity__name-text')
    for skill in skill_elements:
        try:
            text = (await skill.inner_text()).strip()
            if text:
                data["skills"].append(text)
        except:
            continue

    return data

async def main():
    async with async_playwright() as p:
        # 🧠 Connect to your already open Chrome (with login)
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]  # Grab the first available browser context
        page = await context.new_page()

        results = []

        for url in profile_urls:
            try:
                print(f"🔍 Scraping {url}")
                await page.goto(url, timeout=20000)
                data = await extract_profile_data(page)
                if data:
                    results.append(data)
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
                await page.screenshot(path="error_debug.png", full_page=True)

        # 💾 Save output
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'career_fingerprints_{timestamp}.json', 'w') as f:
            json.dump(results, f, indent=2)

        await browser.close()

asyncio.run(main())
