from playwright.sync_api import sync_playwright, expect


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demoqa.com/buttons")

        # ========== ЗАДАНИЕ 1: Получение текста кнопки «Double Click Me» ==========
        dbl_click_btn = page.get_by_role("button", name="Double Click Me", exact=True)
        text_btn = dbl_click_btn.inner_text()

        print(f"Текст кнопки: '{text_btn}'")

        assert text_btn == "Double Click Me"

        # ========== ЗАДАНИЕ 2: Клик по «Click Me» и проверка сообщения ==========
        click_me_btn = page.get_by_role("button", name="Click Me", exact=True)
        click_me_btn.click()

        message_element = page.locator("#dynamicClickMessage")
        expect(message_element).to_have_text("You have done a dynamic click")

        message_text = message_element.inner_text()
        print(f"Текст сообщения: '{message_text}'")

        assert message_text == "You have done a dynamic click"

        # ========== ЗАДАНИЕ 3: Работа с полями ввода на странице Text Box ==========
        page.goto("https://demoqa.com/text-box")

        username_field = page.locator("#userName")
        email_field = page.locator("#userEmail")

        username_field.fill("Idris")
        email_field.fill("test@test.com")

        username_value = username_field.input_value()
        email_value = email_field.input_value()

        print(f"Имя: {username_value}, Email: {email_value}")

        assert username_value == "Idris"
        assert email_value == "test@test.com"

        # ========== ЗАДАНИЕ 4: Работа со списком на странице Select Menu ==========
        page.goto("https://demoqa.com/select-menu")

        select_element = page.locator("#selectMenuContainer")
        options = select_element.locator("option")
        options_texts = options.all_inner_texts()

        print("Список всех опций:")
        for i, text in enumerate(options_texts, 1):
            print(f"  {i}. '{text}'")

        expected_option = "Volvo"
        assert expected_option in options_texts, (f"Ожидалась опция "
                                                  f"'{expected_option}', но она не найдена в списке")

        # ========== ЗАДАНИЕ 5: Сравнение .inner_text() и .text_content() ==========
        page.goto("https://demoqa.com/text-box")

        current_address_label = page.locator("label:has-text('Current Address')").first

        text_inner = current_address_label.inner_text()

        text_content = current_address_label.text_content()

        print(f"Текст через .inner_text(): {repr(text_inner)}")
        print(f"Текст через .text_content(): {repr(text_content)}")

        # Сравниваем результаты
        if text_inner == text_content:
            print("✓ Результаты совпадают")
        else:
            print("✗ Результаты различаются")
            print(f"Разница: .inner_text() возвращает '{text_inner}', а .text_content() возвращает '{text_content}'")

        assert "Current Address" in text_inner, f"Ожидалось 'Current Address' в .inner_text(), получено '{text_inner}'"
        assert "Current Address" in text_content, f"Ожидалось 'Current Address' в .text_content(), получено '{text_content}'"

        browser.close()


if __name__ == '__main__':
    main()
