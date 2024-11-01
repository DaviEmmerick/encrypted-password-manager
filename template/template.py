import sys
import os

# Adiciona o diretório atual ao caminho de importação para acessar os módulos 'model' e 'views'
sys.path.append(os.path.abspath(os.curdir))

from model.password import Password  # Importa a classe Password para manipulação de dados de senhas
from views.password_views import CriptoHasher  # Importa CriptoHasher para criptografar/descriptografar senhas

# Pede ao usuário para escolher entre salvar uma nova senha ou visualizar uma senha salva
action = input('Digite 1 para salvar uma nova senha ou 2 para ver uma senha salva: ')

if action == '1':  # Opção para salvar uma nova senha
    # Se não houver nenhuma senha salva, cria uma nova chave de criptografia
    if len(Password.get()) == 0:
        key, path = CriptoHasher.create_key(archive=True)  # Gera uma chave nova e a salva em um arquivo
        print("Sua chave foi criada com sucesso!")
        print(f'Chave: {key.decode("utf-8")}')  # Mostra a chave gerada para o usuário

        if path:
            # Informa o usuário sobre o caminho do arquivo da chave e sugere removê-lo após salvar
            print("Chave salva no arquivo, lembre-se de remover o arquivo após tranferir de local: ")
            print(f"Caminho: {path}")   
    else:
        # Pede a chave já existente, caso o arquivo já tenha senhas
        key = input("Digite a sua chave utilizada para a criptografia: ")

    # Solicita o domínio e a senha que serão salvos
    domain = input("Domínio: ")
    password = input("Senha: ")
    
    # Cria uma instância de CriptoHasher usando a chave fornecida
    cripto_user = CriptoHasher(key)
    # Criptografa a senha e cria uma nova instância de Password com o domínio e senha criptografada
    p1 = Password(domain=domain, password=cripto_user.encrypt(password).decode('utf-8'))
    p1.save()  # Salva a nova senha no banco de dados

elif action == '2':  # Opção para visualizar uma senha salva
    # Solicita o domínio e a chave de criptografia
    domain = input("Domínio: ")
    key = input("Key: ")
    
    # Cria uma instância de CriptoHasher com a chave fornecida
    cripto_user = CriptoHasher(key)
    data = Password.get()  # Obtém todas as senhas salvas no banco de dados
    
    # Procura a senha correspondente ao domínio fornecido
    for i in data:
        if domain in i['domain']:
            password = cripto_user.decrypt(i['password'])  # Descriptografa a senha
    
    # Exibe a senha se encontrada, ou uma mensagem de erro se não houver correspondência
    if password:
        print(f'Sua senha: {password}')
    else:
        print("Nenhuma senha encontrada para o respectivo domínio.")
