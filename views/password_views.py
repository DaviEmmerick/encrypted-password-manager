import string
import secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken  # type: ignore

class CriptoHasher:
    # Conjunto de caracteres para gerar strings aleatórias
    RANDOM_STRING = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent  # Diretório base do projeto
    KEY_DIR = BASE_DIR / 'keys'  # Diretório onde as chaves serão armazenadas

    def __init__(self, key):
        # Verifica se a chave é uma string, se for, converte para bytes
        if not isinstance(key, bytes):
            key = key.encode()
        # Inicializa o objeto Fernet com a chave para criptografia
        self.fernet = Fernet(key)

    @classmethod
    def string_random(cls):
        # Gera uma string aleatória de 10 caracteres
        return ''.join(secrets.choice(cls.RANDOM_STRING) for _ in range(10))

    @classmethod
    def create_key(cls, archive=False):
        # Gera uma string aleatória e a utiliza para criar um hash SHA-256
        value = cls.string_random()
        hasher = hashlib.sha256(value.encode("utf-8")).digest()
        # Codifica o hash em base64 para ser usado como chave
        key = base64.b64encode(hasher)
        # Se archive=True, a chave será salva em um arquivo
        if archive:
            cls.KEY_DIR.mkdir(parents=True, exist_ok=True)  # Cria o diretório 'keys' se não existir
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        # Define o nome do arquivo como 'key.key' ou gera um novo nome se o arquivo já existir
        file = 'key.key'
        while (cls.KEY_DIR / file).exists():
            file = f'key_{cls.string_random()}.key'
        # Salva a chave em um arquivo no diretório 'keys'
        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key)
        return cls.KEY_DIR / file

    def encrypt(self, value):
        # Converte o valor para bytes, se ainda não estiver nesse formato
        if not isinstance(value, bytes):
            value = value.encode()
        # Criptografa o valor e retorna o resultado
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        # Converte o valor para bytes, se ainda não estiver nesse formato
        if not isinstance(value, bytes):
            value = value.encode()
        try:
            # Tenta descriptografar o valor e retornar como string
            return self.fernet.decrypt(value).decode()
        except InvalidToken:
            # Retorna uma mensagem de erro se a chave estiver incorreta ou o token for inválido
            return 'Token inválido.'
