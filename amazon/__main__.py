import sys
import log

from . import reload_balance


if __name__ == "__main__":
    try:
        reload_balance(*sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        breakpoint()
