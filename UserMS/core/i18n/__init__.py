import os
import os
import pathlib
from subprocess import run
from gettext import gettext, translation

basedir = pathlib.Path(__file__).parent.parent.parent

# The default locale to use if no locale selector is registered. This defaults to 'en'.
BABEL_DEFAULT_LOCALE: str = "fa"
# A semi-colon (;) separated string of absolute
# and relative (to the app root) paths to translation folders. Defaults to translations.
BABEL_TRANSLATION_DIRECTORIES: str = os.path.join(basedir, "lang")

# The message domain used by the application. Defaults to messages.
BABEL_DOMAIN: str = "messages.pot"

BABEL_CONFIG_FILE: str = os.path.join(basedir, "core", "i18n", "babel.cfg")

BABEL_MESSAGE_POT_FILE: str = os.path.join(basedir, BABEL_DOMAIN)


class Babel(object):
    __module_name__ = "pybabel"

    def __init__(self) -> None:
        self.__locale = BABEL_DEFAULT_LOCALE

    def extract(self, watch_dir: str) -> None:
        """extract all messages that annotated using gettext/_
        in the specified directory.

        for first time will create messages.pot file into the root
        directory.

        Args:
            watch_dir (str): directory to extract messages.
        """
        run(
            [
                Babel.__module_name__,
                "extract",
                "-F",
                BABEL_CONFIG_FILE,
                "-o",
                BABEL_MESSAGE_POT_FILE,
                watch_dir,
            ]
        )

    def init(self, lang: str) -> None:
        """Initialized lacale directory for first time.
        if there is already exists the directory, notice that your
        all comiled and initialized messages will remove, in this
        condition has better to use `Babel.update` method.

        Args:
            lang (str): locale directory name and path
        """
        run(
            [
                Babel.__module_name__,
                "init",
                "-i",
                BABEL_MESSAGE_POT_FILE,
                "-d",
                BABEL_TRANSLATION_DIRECTORIES,
                "-l",
                lang or BABEL_DEFAULT_LOCALE,
            ]
        )

    def update(self, watch_dir: str) -> None:
        """update the extracted messages after init command/initialized directory
        , Default is `./lang`"

        Args:
            watch_dir (str): locale directory name and path
        """
        run(
            [
                Babel.__module_name__,
                "update",
                "-i",
                BABEL_DOMAIN,
                "-d",
                watch_dir or BABEL_TRANSLATION_DIRECTORIES,
            ]
        )

    def compile(self):
        """
        compile all messages from translation directory in .PO to .MO file and is
        a binnary text file.
        """
        run([Babel.__module_name__, "compile", "-d", BABEL_TRANSLATION_DIRECTORIES])

    @property
    def gettext(self):
        if self.locale == "fa":
            gt = translation(
                "messages",
                BABEL_TRANSLATION_DIRECTORIES,
                [self.locale],
            )
            gt.install()
            return gt.gettext
        return gettext

    @property
    def locale(self):
        return self.__locale

    @locale.setter
    def locale(self, value):
        self.__locale = value


babel = Babel()


def make_gettext(message: str) -> str:
    """translate the message and retrieve message from .PO and .MO depends on
    `Babel.locale` locale.

    Args:
        message (str): message content

    Returns:
        str: transalted message.
    """
    return babel.gettext(message)


_ = make_gettext
