class RC4:
    def __init__(self):
        self.S_lazy_loaded = [i for i in range(0, 256)]

    def __ksa__(self, key_in_array: list):
        j = 0
        S = self.S_lazy_loaded.copy()
        for i in range(0, len(S)):
            j = (j + S[i] + key_in_array[i % len(key_in_array)]) % len(S)
            S[i], S[j] = S[j], S[i]
        return S

    def __pgra__(self, S: list):
        i = j = 0
        key_stream = []

        for k in range(0, len(S)):
            i = (i + 1) % len(S)
            j = (j + S[i]) % len(S)

            S[i], S[j] = S[j], S[i]
            current_key_stream_value = (S[i] + S[j]) % len(S)
            key_stream.append(S[current_key_stream_value])
        return key_stream

    def __xor__(self, key_stream: list, phrase_stream: list):
        cipher_text = []
        for i in range(len(phrase_stream)):
            c = key_stream[i] ^ phrase_stream[i]
            cipher_text.append(c)
        return cipher_text

    def __generate_key_stream__(self, key: str):
        key_array = list(map(ord, list(key)))
        s = self.__ksa__(key_array)
        k_stream = self.__pgra__(s)
        return k_stream

    def __make_key_array_the_same_lenght_as_the_key__(self, difference, key_array):
        if difference != 0:
            for i in range(0, difference):
                key_array.append(key_array[i])
        return key_array

    def encrypt(self, key: str, phrase: str):
        key_stream = self.__generate_key_stream__(key)
        phrase_array = list(map(ord, list(phrase)))
        encrypted_text = self.__xor__(key_stream, phrase_array)
        return encrypted_text

    def decrypt(self, key: str, phrase: str):
        key_array = list(map(ord, list(key)))
        phrase_array = list(map(ord, list(phrase)))

        difference = int(len(self.S_lazy_loaded) - len(key_array))
        key_array = self.__make_key_array_the_same_lenght_as_the_key__(difference, key_array)

        S = self.__ksa__(key_array)
        key_stream = self.__pgra__(S)
        original_text = self.__xor__(key_stream, phrase_array)
        return original_text
