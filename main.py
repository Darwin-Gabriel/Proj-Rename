import os
import platform
import sys
from cryptography.fernet import Fernet


# Função para tornar o arquivo ou pasta oculto no Windows
def hide_file_windows(file_path):
    os.system(f"attrib +h {file_path}")


# Chave Fernet para criptografia e descriptografia
CRYPTO_KEY = "aSGQOfs0rTLL7dpaUPDAqTQiWi1ggGqUweoPNX4zipI="


def encrypt_data(data):
    f = Fernet(CRYPTO_KEY)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data):
    f = Fernet(CRYPTO_KEY)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data


# Verifica se o sistema é Windows
if platform.system() == "Windows":
    # Usando o caminho especificado
    folder_path = os.path.expandvars("C:\\Users\\%username%\\OneDrive\\Documentos\\KEY")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        hide_file_windows(folder_path)

    key_file_path = os.path.join(folder_path, ".pref.key")
else:
    # Mantém o caminho anterior caso não seja Windows
    key_file_path = ".pref.key"

if not os.path.exists(key_file_path):
    user_key = input("Digite sua chave KeyAuth pela primeira vez: ")
    encrypted_key = encrypt_data(user_key)
    with open(key_file_path, "wb") as key_file:
        key_file.write(encrypted_key)
    if platform.system() == "Windows":
        hide_file_windows(key_file_path)
    # Reiniciando o programa após inserir a chave
    os.execv(sys.executable, ['python'] + sys.argv)
else:
    with open(key_file_path, "rb") as key_file:
        encrypted_user_key = key_file.read()
        user_key = decrypt_data(encrypted_user_key)

import os
import webbrowser
import time
from tkinter import filedialog, Tk
from PyPDF2 import PdfReader

# Dicionário de meses
MONTHS = {
    'janeiro': '01', 'jan': '01', '01': '01', '1': '01',
    'fevereiro': '02', 'fev': '02', '02': '02', '2': '02',
    'março': '03', 'mar': '03', '03': '03', '3': '03',
    'abril': '04', 'abr': '04', '04': '04', '4': '04',
    'maio': '05', 'mai': '05', '05': '05', '5': '05',
    'junho': '06', 'jun': '06', '06': '06', '6': '06',
    'julho': '07', 'jul': '07', '07': '07', '7': '07',
    'agosto': '08', 'ago': '08', '08': '08', '8': '08',
    'setembro': '09', 'set': '09', '09': '09', '9': '09',
    'outubro': '10', 'out': '10', '10': '10',
    'novembro': '11', 'nov': '11', '11': '11',
    'dezembro': '12', 'dez': '12', '12': '12'
}


def format_day(day):
    # Garante que o dia tenha dois dígitos
    return f"{day:02}"


def get_new_filename(prefix, year, month, day, directory):
    filename = f"{prefix}-{year}-{month}-{day}.pdf"
    counter = 2
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{prefix}-{year}-{month}-{day}-{counter}.pdf"
        counter += 1
        if counter > 9:
            raise ValueError("Too many duplicate filenames.")
    return filename


def main():
    # Janela de seleção de arquivos
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

    if not files:  # Se nenhum arquivo foi selecionado
        return

    prefix = input("Digite o prefixo desejado: ")
    year = None

    for file in files:
        webbrowser.open(file)  # Abre o arquivo PDF para visualização

        # Se o ano já foi definido, perguntar se deseja manter o mesmo ou alterar
        if year:
            change_year = input(
                f"Quer continuar com o ano {year}? (Deixe em branco para manter, digite 1 para alterar): ")
            if change_year == "1":
                year = input("Digite o novo ano: ")
            elif change_year == "s2":
                prefix = input("Digite o novo prefixo: ")
                year = input("Digite o novo ano: ")
            elif change_year == "2":
                prefix = input("Digite o novo prefixo: ")
            elif change_year == "0":
                print("Pulando este arquivo...")
                # Fecha o Acrobat Reader
                os.system("taskkill /f /im Acrobat.exe")
                time.sleep(1.5)  # Aguarda por 1.5 segundos
                continue
        else:
            year = input("Digite o ano: ")

        month = input("Digite o mês: ").lower()
        month = MONTHS.get(month, '00')  # Se não encontrar o mês no dicionário, atribui '00'

        day = format_day(int(input("Digite o dia: ")))

        # Mostra uma prévia do nome do arquivo
        new_filename_preview = get_new_filename(prefix, year, month, day, os.path.dirname(file))
        print(f"Prévia do nome do arquivo: {new_filename_preview}")

        # Pergunta se deseja continuar
        confirm = input("Pressione Enter para continuar ou digite 1 para alterar os detalhes: ")
        while confirm == "1":
            # Pergunta se deseja manter o ano atual
            change_year = input(
                f"Quer continuar com o ano {year}? (Deixe em branco para manter, digite 1 para alterar): ")
            if change_year == "1":
                year = input("Digite o novo ano: ")
            elif change_year == "s2":
                prefix = input("Digite o novo prefixo: ")
                year = input("Digite o novo ano: ")
            elif change_year == "2":
                prefix = input("Digite o novo prefixo: ")

            month = input("Digite o mês: ").lower()
            month = MONTHS.get(month, '00')
            day = format_day(int(input("Digite o dia: ")))

            new_filename_preview = get_new_filename(prefix, year, month, day, os.path.dirname(file))
            print(f"Prévia do nome do arquivo: {new_filename_preview}")
            confirm = input("Pressione Enter para continuar ou digite 1 para alterar os detalhes: ")

        # Fecha o Acrobat Reader
        os.system("taskkill /f /im Acrobat.exe")
        time.sleep(1.5)  # Aguarda por 1.5 segundos

        # Renomeia o arquivo
        os.rename(file, os.path.join(os.path.dirname(file), new_filename_preview))
        print(f"Arquivo renomeado para: {new_filename_preview}")


if __name__ == "__main__":
    main()
