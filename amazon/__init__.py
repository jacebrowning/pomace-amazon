import sys

import bullet
import log
import pomace


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

    if "notification sent" in page:
        log.warn("Manually refresh the page after approving notification")
        while "notification sent" in page:
            page = pomace.auto()

    if "One Time Password" in page:
        log.info("One Time Password (OTP) required")
        otp = bullet.Input(prompt="otp: ").launch()
        page = page.fill_otp(otp).click_sign_in()

    if "Add mobile number" in page:
        page = page.click_not_now()

    for index in range(int(repeat)):
        log.info(f"Selecting amount ${amount}")
        page = page.fill_amount(amount).type_tab(wait=0).click_buy_now()
        assert f"${amount}" in page

        page = page.click_use_this_payment_method(wait=1)
        if "By placing your order" not in page:
            log.info("Choosing payment method")
            page = page.click_card(wait=1)

            if page.browser.find_by_text("Verify your card").first.visible:
                log.info("Handling card verification")
                page = page.fill_card(settings.card).click_verify_card(wait=1)

            page = page.click_use_this_payment_method(wait=1)
            assert "By placing your order" in page

        log.info("Placing order")
        page = page.click_place_your_order(wait=2)

        log.info(f"Balance reloaded {index + 1} time(s)")
        page = pomace.visit("https://www.amazon.com/asv/reload/order")
