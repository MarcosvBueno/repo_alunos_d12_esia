"""Cadastro de clientes."""

import re

_CLIENTES = []
_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def _digito_verificador(digitos):
    """Calcula o dígito verificador do CPF para a sequência de dígitos dada."""
    soma = sum(d * p for d, p in zip(digitos, range(len(digitos) + 1, 1, -1)))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def _cpf_valido(cpf):
    """R3.2: dígitos verificadores válidos, sem todos os dígitos iguais; aceita pontuação."""
    if not isinstance(cpf, str):
        return False
    digitos = [int(c) for c in cpf if c in "0123456789"]
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    return digitos[9] == _digito_verificador(digitos[:9]) and digitos[10] == _digito_verificador(digitos[:10])


def _email_valido(email):
    """R3.3: formato texto@texto.texto."""
    return isinstance(email, str) and _EMAIL.fullmatch(email) is not None


def _preenchido(valor):
    return isinstance(valor, str) and valor.strip() != ""


def _validar(payload):
    """R3.1, R3.2, R3.3: devolve a lista de todos os erros, sem parar no primeiro."""
    erros = []
    if not _preenchido(payload.get("nome")):
        erros.append({"campo": "nome", "erro": "campo obrigatório"})
    if not _preenchido(payload.get("email")):
        erros.append({"campo": "email", "erro": "campo obrigatório"})
    elif not _email_valido(payload["email"]):
        erros.append({"campo": "email", "erro": "email inválido"})
    if not _preenchido(payload.get("cpf")):
        erros.append({"campo": "cpf", "erro": "campo obrigatório"})
    elif not _cpf_valido(payload["cpf"]):
        erros.append({"campo": "cpf", "erro": "cpf inválido"})
    return erros


def cadastrar_cliente(payload):
    """Cadastra um cliente. R3.4: cadastro inválido responde 422 com todos os erros."""
    erros = _validar(payload)
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
