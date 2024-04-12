import gettext
import os


class Translator:
    DEFAULT_LOCALE_PATH = "locales"

    def __init__(self, lang, locale_dir=DEFAULT_LOCALE_PATH):
        self.lang = lang
        self.locale_dir = os.path.join(os.getcwd(), locale_dir)
        self._init_translator()

    def _init_translator(self):
        self.translator = gettext.translation(
            "messages", self.locale_dir, languages=[self.lang], fallback=True
        )
        self.translator.install()

    def translate(self, msg):
        return self.translator.gettext(msg)


def create_translator(lang):
    lang_map = {"ja": "ja_JP", "en": "en"}
    selected_lang = lang_map.get(lang, "en")
    return Translator(selected_lang).translate
