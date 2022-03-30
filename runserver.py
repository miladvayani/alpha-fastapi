from UserMS import create_app
from UserMS.core.i18n import cli
from configs import Development

application = create_app(Development())

if __name__ == "__main__":
    cli.cmd()
