import asyncio
from playwright.async_api import async_playwright

def get_zocdoc_search_url(query, location, page=1):
    return f"https://www.zocdoc.com/search?dr_specialty={query}&address={location}&page={page}"

async def scrape_zocdoc_lash_salons_nyc(limit=30):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page_num = 1
        while len(results) < limit:
            url = get_zocdoc_search_url('lash+salon', 'New+York%2C+NY', page_num)
            await page.goto(url)
            await page.wait_for_selector('div[data-test="search-result-card"]', timeout=10000)
            cards = await page.query_selector_all('div[data-test="search-result-card"]')
            for card in cards:
                name = await card.query_selector_eval('h2', 'el => el.innerText')
                phone = await card.query_selector_eval('a[href^=tel]', 'el => el.innerText', strict=False) if await card.query_selector('a[href^=tel]') else ''
                category = 'Lash Salon'
                address = await card.query_selector_eval('address', 'el => el.innerText', strict=False) if await card.query_selector('address') else ''
                website = '' # Zocdoc rarely lists websites
                results.append({
                    'name': name.strip(),
                    'phone': phone.strip(),
                    'category': category,
                    'address': address.strip(),
                    'website': website
                })
                if len(results) >= limit:
                    break
            page_num += 1
        await browser.close()
    return results

def scrape_lash_salons(limit=30):
    return asyncio.run(scrape_zocdoc_lash_salons_nyc(limit=limit))
