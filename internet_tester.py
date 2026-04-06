import os

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


def test_task9(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("JavaScript Alerts")

    page.click("button[onclick='jsAlert()']")

    result = page.locator("#result")
    assert result.text_content() == "You successfully clicked an alert"
    print(f"✅ Alert принят. Сообщение: {result.text_content()}")


def test_task10(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("File Upload")

    with open("test_upload.txt", "w") as f:
        f.write("Hello Playwright")

    page.set_input_files("#file-upload", "test_upload.txt")
    page.click("#file-submit")

    uploaded_file = page.locator("#uploaded-files")
    assert "test_upload.txt" in uploaded_file.text_content()

    print(f"✅ Файл загружен: test_upload.txt")

    os.remove("test_upload.txt")


def test_task11(page):
    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)
    tester.navigate_to_example("Dynamic Loading")

    page.click("//*[@id='content']/div/a[1]")

    page.click("//*[@id='start']/button")

    page.wait_for_selector("//*[@id='finish']/h4", state="visible")
    text = page.locator("//*[@id='finish']/h4").text_content()

    assert text == "Hello World!"
    print(f"✅ Элемент появился: {text}")


def test_task12(page):
    results = {}

    page.goto("https://the-internet.herokuapp.com/")
    tester = InternetTester(page)

    try:
        tester.navigate_to_example("Form Authentication")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button:has-text('Login')")
        page.click("//*[@id='content']/div/a")
        page.screenshot(path="screenshots/form_auth.png")
        results["Form Authentication"] = "✅"
    except:
        results["Form Authentication"] = "❌"

    try:
        page.goto("https://the-internet.herokuapp.com/")
        tester.navigate_to_example("Checkboxes")
        checkboxes = page.locator("input[type='checkbox']")
        checkboxes.nth(0).check()
        checkboxes.nth(1).uncheck()
        page.screenshot(path="screenshots/checkboxes.png")
        results["Checkboxes"] = "✅"
    except:
        results["Checkboxes"] = "❌"

    try:
        page.goto("https://the-internet.herokuapp.com/")
        tester.navigate_to_example("Dropdown")
        dropdown = page.locator("#dropdown")
        dropdown.select_option("Option 2")
        page.screenshot(path="screenshots/dropdown.png")
        results["Dropdown"] = "✅"
    except:
        results["Dropdown"] = "❌"

    try:
        page.goto("https://the-internet.herokuapp.com/")
        tester.navigate_to_example("Inputs")
        input_field = page.locator("input[type='number']")
        input_field.fill("999")
        page.screenshot(path="screenshots/inputs.png")
        results["Inputs"] = "✅"
    except:
        results["Inputs"] = "❌"

    try:
        page.goto("https://the-internet.herokuapp.com/")
        tester.navigate_to_example("Hovers")
        figure = page.locator("figure").first
        figure.hover()
        page.screenshot(path="screenshots/hovers.png")
        results["Inputs"] = "✅"
    except:
        results["Hovers"] = "❌"

    print("\n📊 ОТЧЁТ:")
    for key, value in results.items():
        print(f"{value} {key}")

    if all(v == "✅" for v in results.values()):
        print("\n✅ Все тесты пройдены!")
    else:
        print("\n❌ Некоторые тесты не пройдены!")


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
        test_task9(page)
        test_task10(page)
        test_task11(page)
        test_task12(page)

        browser.close()


if __name__ == "__main__":
    main()