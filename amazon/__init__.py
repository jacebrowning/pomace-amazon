from pomace import visit, get_secret
import log


def reload_balance(amount: str, _repeat: str):
    repeat = int(_repeat)

    page = visit("https://www.amazon.com/asv/reload/order", browser="Firefox")

    email = get_secret("email")
    password = get_secret("password")
    card = get_secret("card")
    assert email and password and card

    log.info(f"Logging in as {email}")
    page = page.click_sign_in().fill_email(email).click_continue()
    page = page.fill_password(password).click_sign_in()

    for index in range(repeat):
        log.info(f"Selecting amount ${amount}")
        page = page.fill_amount(amount)

        assert f"Reload ${amount}" in page
        log.info("Reloading balance")
        page = page.click_reload(delay=2)

        if "Verify your card" in page:
            log.info("Handling card verification")
            page = page.fill_card(card).click_verify_card()
            assert f"Reload ${amount}" in page
            page = page.click_reload(delay=2)

        log.info(f"Balance reloaded {index + 1} time(s)")
        page = page.click_reload_again()
