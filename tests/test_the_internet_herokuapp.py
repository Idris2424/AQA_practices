import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope="function")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


def test_main_page_title(browser_page):
    browser_page.goto("https://the-internet.herokuapp.com/")
    h3_element = browser_page.locator("h2")
    expect(h3_element).to_contain_text("Available Examples")


def test_login_error_message(browser_page):
    browser_page.goto("https://the-internet.herokuapp.com/login")
    browser_page.fill("#username", "dfgdfbsfd")
    browser_page.fill("#password", "Supfbsdfbassword!")
    browser_page.click("button[type='submit']")
    flash_element = browser_page.locator(".flash")
    expect(flash_element).to_contain_text("Your username is invalid!")


def test_successful_login(browser_page):
    browser_page.goto("https://the-internet.herokuapp.com/login")
    browser_page.fill("#username", "tomsmith")
    browser_page.fill("#password", "SuperSecretPassword!")
    browser_page.click("button[type='submit']")

    browser_page.wait_for_url("https://the-internet.herokuapp.com/secure")
    subheader_element = browser_page.locator(".subheader")
    welcome_text = subheader_element.inner_text()

    expect(subheader_element).to_contain_text("Welcome to the Secure Area")
    print(f"\nТекст приветствия: {welcome_text}")


def test_checkboxes_list(browser_page):
    browser_page.goto("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = browser_page.locator("input[type='checkbox']")
    count = checkboxes.count()
    for i in range(count):
        checkbox = checkboxes.nth(i)

        is_checked = checkbox.is_checked()
        state = "checked" if is_checked else "unchecked"
        print(state)


def test_dynamic_loading(browser_page):
    browser_page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")

    start_button = browser_page.locator("button:has-text('Start')")
    start_button.click()

    finish_element = browser_page.locator("#finish")
    finish_element.wait_for(state="visible", timeout=10000)

    actual_text = finish_element.inner_text()
    assert actual_text == "Hello World!"


def test_iframe_text(browser_page):
    browser_page.goto("https://the-internet.herokuapp.com/iframe")

    frame = browser_page.frame_locator("#mce_0_ifr")

    text_element = frame.locator("body")

    expect(text_element).to_contain_text("Your content goes here")

    actual_text = text_element.inner_text()
    print(f"\nТекст внутри iframe: '{actual_text}'")

    assert "Your content goes here" in actual_text, "Текст не найден в iframe"
