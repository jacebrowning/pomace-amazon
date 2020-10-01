import bullet
import log
import pomace
import sys


def cli():
    try:
        reload_balance(*sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        breakpoint()


def reload_balance(amount: str, repeat: str):
    page = pomace.visit("https://www.amazon.com/asv/reload/order")
    settings = pomace.prompt("email", "password", "card")

    log.info(f"Logging in as {settings.email}")
    page = page.click_sign_in().fill_email(settings.email).click_continue()
    page = page.fill_password(settings.password).click_sign_in()

    if "One Time Password" in page:
        log.info("One Time Password (OTP) required")
        otp = bullet.Input(prompt="otp: ").launch()
        page = page.fill_otp(otp).click_sign_in()

    if "Add mobile number" in page:
        page = page.click_not_now()

    for index in range(int(repeat)):
        log.info(f"Selecting amount ${amount}")
        page = page.fill_amount(amount)

        assert f"Reload ${amount}" in page
        log.info("Reloading balance")
        page = page.click_reload(delay=2)

        if "Verify your card" in page:
            log.info("Handling card verification")
            page = page.fill_card(settings.card).click_verify_card()
            assert f"Reload ${amount}" in page
            page = page.click_reload(delay=2)

        log.info(f"Balance reloaded {index + 1} time(s)")
        page = page.click_reload_again()
