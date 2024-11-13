# Класс шифровки/дешифровки пароля
from cryptography.fernet import Fernet
import base64
import hashlib


class Crypto:
    """Шифрует/дешифрует пароль. Менять на свой страх и риск"""

    @staticmethod
    def generate_cipher_suite(user_password):
        """Без понятия, что это"""
        # Преобразование пароля в байты
        password_bytes = user_password.encode('utf-8')

        # Хеширование пароля для получения 32 байт ключа
        key = hashlib.sha256(password_bytes).digest()

        # Преобразование ключа в base64
        base64_key = base64.urlsafe_b64encode(key)

        # Создание шифра на основе ключа
        cipher_suite = Fernet(base64_key)
        return cipher_suite

    @staticmethod
    def encrypt(plain_text, user_password):
        """Шифрует пароль"""
        cipher_suite = Crypto.generate_cipher_suite(user_password)
        encrypted_text = cipher_suite.encrypt(plain_text.encode())
        encrypted_text = Crypto.bytes_to_utf8(encrypted_text)
        return encrypted_text

    @staticmethod
    def decrypt(encrypted_text, user_password):
        """Расшифровывает"""
        cipher_suite = Crypto.generate_cipher_suite(user_password)
        encrypted_bytes = Crypto.utf8_to_bytes(encrypted_text)
        decrypted_text = cipher_suite.decrypt(encrypted_bytes).decode()
        return decrypted_text

    @staticmethod
    def bytes_to_utf8(byte_string):
        """Без понятия, что это"""
        return byte_string.decode('utf-8')

    @staticmethod
    def utf8_to_bytes(utf8_string):
        """Без понятия, что это"""
        return utf8_string.encode('utf-8')
