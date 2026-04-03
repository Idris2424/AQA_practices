from playwright.sync_api import sync_playwright
import os
import re


def inspect_page(url, browser_type = "chromium", headless = True,
                 screenshot: bool = False) -> dict:
    with sync_playwright() as p:
        if browser_type == "chromium":
            browser = p.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")

        page = browser.new_page()
        page.goto(url)
        title = page.title()
        viewport = page.viewport_size
        url_final = page.url

        screenshot_path = None
        if screenshot:
            os.makedirs("output/screenshots", exist_ok=True)
            safe_name = re.sub(r'[^\w\-_]', '_', url)
            screenshot_path = f"output/screenshots/{browser_type}_{safe_name}.png"
            page.screenshot(path=screenshot_path)

        browser.close()

    result = {
        "url": url,
        "browser": browser_type,
        "title": title,
        "viewport": viewport,
        "url_final": url_final,
        "success": True
    }

    if screenshot_path:
        result["screenshot"] = screenshot_path

    return result


if __name__ == "__main__":
    result = inspect_page("https://example.com", browser_type="chromium", headless=False, screenshot=True)
    print(f"[{result['browser']}] {result['title']}")
    print(f"Viewport: {result['viewport']}")
    print(f"Финальный URL: {result['url_final']}")
    if "screenshot" in result:
        print(f"📸 Скриншот: {result['screenshot']}")
