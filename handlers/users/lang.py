from translate import Translator


def translate_uz_to_ru(text):
    translator = Translator(from_lang="uz", to_lang="ru")
    translation = translator.translate(text=text)
    return translation