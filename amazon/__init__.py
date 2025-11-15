import sys
import time

import bullet
import log
import pomace


def cli():
    log.reset()
    log.init()
    log.silence("datafiles", allow_warning=True)
    if "--dev" in sys.argv:
        sys.argv.pop()
    else:
        pomace.freeze()

    try:
        amount, repeat = sys.argv[1:]
    except ValueError:
        print("Usage: amazon-reload-balance <amount> <repeat>")
        sys.exit(1)

    try:
        reload_balance(amount, repeat)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        page = pomace.auto()
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
        log.info("Selecting one-time reload")
        page = page.click_one_time_reload()
        time.sleep(2)

        log.info(f"Entering amount ${amount}")
        page = page.fill_amount(amount, wait=2).type_tab(wait=1)
        assert f"${amount}" in page

        log.info("Clicking buy now")
        page = page.click_buy_now()

        time.sleep(1)
        popover = page.browser.find_by_id("a-popover-content-1")
        if popover and popover.visible:
            log.info("Closing popover")
            page.browser.find_by_css(".a-button-close").click()
            time.sleep(2)

        suffix = settings.card[-4:]
        if suffix not in page:
            log.info("Changing payment method")
            page = page.click_change(wait=2)
        log.info(f"Selecting card ending in {suffix}")
        page.browser.find_by_text(f"ending in {suffix}").click()
        time.sleep(2)

        verify = page.browser.find_by_text("Verify card")
        if verify and verify.visible:
            log.info("Handling card verification")
            page = page.fill_card(settings.card).click_verify_card(wait=1)

        log.info("Confirming payment method")
        page = page.click_use_this_payment_method()

        log.info("Placing order")
        page = page.click_place_your_order()

        s = "s" if index == 0 else ""
        log.info(f"Balance reloaded {index + 1} time{s}")
        page = pomace.visit("https://www.amazon.com/asv/reload/order")
