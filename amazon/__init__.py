from pomace import visit, autopage, shared


def reload_balance(email: str, password: str, amount: str, _repeat: str):
    repeat = int(_repeat)

    page = visit("https://www.amazon.com/asv/reload/order", browser="Firefox")

    page = page.click_sign_in().fill_email(email).click_continue()
    page = page.fill_password(password).click_sign_in()

    for x in range(repeat):
        page = page.fill_amount(amount)

        input()
        page = page.click_reload()

        if "Verify your card" in shared.browser.html:
            input()

        page.click_reload_again()

