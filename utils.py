import hashlib
import os

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()