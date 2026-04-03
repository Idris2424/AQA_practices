from playwright.sync_api import sync_playwright


class InternetTester:
    def __init__(self, page):
        self.page = page

    def navigate_to_example(self, example_name: str):
        self.page.get_by_text(example_name).click()
        return self.page.url


def test_task1(page):
    page.goto("https://the-internet.herokuapp.com/")
    assert "The Internet" in page.title()
    h1_text = page.locator("h2").first.text_content()
    print(f"✅ Сайт доступен. Заголовок: {h1_text}")


def test_task2(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    url = tester.navigate_to_example("Form Authentication")
    assert "/login" in url
    print(f"✅ Перешли в: Form Authentication | URL: {url}")


def test_task3(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Form Authentication")
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button:has-text('Login')")
    assert "/secure" in page.url
    print(f"✅ Успешный вход! URL: {page.url}")


def test_task4(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Form Authentication")
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button:has-text('Login')")
    page.click("//*[@id='content']/div/a")
    assert "/login" in page.url
    print(f"✅ Успешный выход! URL: {page.url}")


def test_task5(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Checkboxes")
    checkboxes = page.locator("input[type='checkbox']")
    assert not checkboxes.nth(0).is_checked()
    assert checkboxes.nth(1).is_checked()
    checkboxes.nth(0).check()
    checkboxes.nth(1).uncheck()
    assert checkboxes.nth(0).is_checked()
    assert not checkboxes.nth(1).is_checked()
    print(f"✅ Checkbox 1: checked={checkboxes.nth(0).is_checked()}")
    print(f"✅ Checkbox 2: checked={checkboxes.nth(1).is_checked()}")


def test_task6(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Dropdown")
    dropdown = page.locator("#dropdown")
    dropdown.select_option("Option 1")
    assert dropdown.input_value() == "1"
    dropdown.select_option("Option 2")
    assert dropdown.input_value() == "2"
    print("✅ Выбрано: Option 2")


def test_task7(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Inputs")
    input_field = page.locator("input[type='number']")
    input_field.fill("123")
    assert input_field.input_value() == "123"
    input_field.clear()
    input_field.fill("456")
    print(f"✅ Введено: {input_field.input_value()}")


def test_task8(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Hovers")
    figure = page.locator("figure").first
    figure.hover()
    text = figure.locator("figcaption").text_content()
    assert "user1" in text.lower()
    print(f"✅ Навели на изображение. Текст: {text.strip()}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        test_task1(page)
        test_task2(page)
        test_task3(page)
        test_task4(page)
        test_task5(page)
        test_task6(page)
        test_task7(page)
        test_task8(page)

        browser.close()


if __name__ == "__main__":
    main()