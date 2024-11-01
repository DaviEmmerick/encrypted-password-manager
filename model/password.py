from datetime import datetime
from pathlib import Path

class BaseModel:
    # Diretório base do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent
    # Diretório onde os arquivos de banco de dados serão armazenados
    DB_DIR = BASE_DIR / 'db'

    def save(self):
        # Define o caminho do arquivo de dados da classe, usando o nome da classe
        table_path = Path(self.DB_DIR / f'{self.__class__.__name__}.txt')
        if not table_path.exists():
            table_path.touch()  # Cria o arquivo se não existir

        # Concatena todos os valores dos atributos do objeto em uma string separada por "|"
        string = ""
        for i in self.__dict__.values():
            string += f'{i}|'

        # Escreve a string resultante no arquivo, criando uma nova linha
        with open(table_path, 'a') as arq:
            arq.write(string)
            arq.write('\n')

    @classmethod
    def get(cls):
        # Define o caminho do arquivo de dados da classe
        table_path = Path(cls.DB_DIR / f'{cls.__name__}.txt')
        if not table_path.exists():
            table_path.touch()  # Cria o arquivo se ele ainda não existir

        # Lê todas as linhas do arquivo
        with open(table_path, 'r') as arq:
            x = arq.readlines()

        results = []
        # Obtém todos os atributos definidos na classe para usar como chaves de dicionário
        attributes = vars(cls())
        
        # Itera sobre cada linha do arquivo
        for i in x:
            # Divide a linha pelos separadores '|' para obter os valores
            split_v = i.split('|')
            # Cria um dicionário associando os atributos da classe aos valores lidos
            tmp_dict = dict(zip(attributes, split_v))
            results.append(tmp_dict)  # Adiciona o dicionário à lista de resultados
        
        return results  # Retorna a lista com todos os registros

class Password(BaseModel):
    # A classe Password herda de BaseModel e adiciona atributos específicos
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain  # Domínio ou identificador da senha
        self.password = password  # A senha criptografada
        self.create_at = datetime.now().isoformat()  # Data de criação, no formato ISO
