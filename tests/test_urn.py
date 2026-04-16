import re
import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def test_main_title(page):
    page.goto("https://www.urn.su/ui/basic_test/#intro")
    heading = page.locator("h1, h2").first
    text = heading.inner_text()
    print(f"\n[Задача 1] Заголовок: {text}")
    assert text.strip() != "", "Заголовок не должен быть пустым"


def test_list_elements(page):
    page.goto("https://www.urn.su/ui/basic_test/#intro")

    all_lis = page.locator("ul li, ol li")
    texts = all_lis.all_inner_texts()
    expected = ""
    assert expected in texts


def test_formatted_text(page):
    page.goto("https://www.urn.su/ui/basic_test/#intro")
    elem = page.locator("p").first
    inner = elem.inner_text()
    text_content = elem.text_content()
    print(f"\n[Задача 3]")
    print(f"inner_text(): {repr(inner)}")
    print(f"text_content(): {repr(text_content)}")
    stripped = inner.strip()
    print(f"После strip(): {repr(stripped)}")

def test_visible_vs_full_text(page):
    page.goto("https://www.urn.su/ui/basic_test/#intro")
    elem = page.locator("div").first
    inner = elem.inner_text()
    text_content = elem.text_content()
    print(f"\n[Задача 4]")
    print(f"Длина inner_text(): {len(inner)}")
    print(f"Длина text_content(): {len(text_content)}")
    print("Вывод: Для видимого текста лучше inner_text()")

def test_regex_extract_number(page):
    page.goto("https://www.urn.su/ui/basic_test/#intro")
    cell_with_number = page.locator("td").filter(has_text=re.compile(r"\d{4}")).first
    expect(cell_with_number).to_have_text(re.compile(r"\d+"))
    text = cell_with_number.inner_text()
    numbers = re.findall(r"\d+", text)
    print(f"\n[Бонус] Текст: {text}, Число: {numbers}")
    assert numbers, "Число не найдено"
    value = int(numbers[0])
    assert value > 0


if __name__ == "__main__":
    pytest.main()
