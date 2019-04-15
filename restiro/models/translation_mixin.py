

class TranslationMixin:
    __translation_keys__: tuple = ()

    def extract_translations(self):
        return [
            getattr(self, key)
            for key in self.__translation_keys__
            if getattr(self, key) is not None
        ]

    def translate(self, translator):
        for key in self.__translation_keys__:
            value = getattr(self, key)
            if value is None:
                continue
            setattr(self, key, translator(value))
