from lingua import Language, LanguageDetectorBuilder


def detect_cyrillic_language(text):
    detector = LanguageDetectorBuilder.from_all_languages_with_cyrillic_script().build()
    return detector.detect_language_of(text)


def get_language(text):
    detector = LanguageDetectorBuilder.from_all_languages().build()
    if detector.detect_language_of(text) == Language.RUSSIAN:
        return True
    else:
        return False
