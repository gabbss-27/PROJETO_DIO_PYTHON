import textwrap

# Constantes
LIMITE_SAQUES = 3
AGENCIA = "0001"
LIMITE_DEPÓSITO = 10000
LIMITE_SAQUE = 500

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato

    if valor > LIMITE_DEPÓSITO:
        print(f"\n@@@ Operação falhou! O valor máximo para depósito é R$ {LIMITE_DEPÓSITO:.2f}. @@@")
        return saldo, extrato

    saldo += valor
    extrato += f"Depósito:\tR$ {valor:.2f}\n"
    print("\n=== Depósito realizado com sucesso! ===")
    return saldo, extrato


def sacar(saldo, valor, extrato, limite, numero_saques):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato

    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        return saldo, extrato

    if valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        return saldo, extrato

    if numero_saques >= LIMITE_SAQUES:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        return saldo, extrato

    saldo -= valor
    extrato += f"Saque:\t\tR$ {valor:.2f}\n"
    numero_saques += 1
    print("\n=== Saque realizado com sucesso! ===")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

  
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Não há contas cadastradas. @@@")
        return

    for conta in contas:
        linha = f"""\ 
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    saldo = 0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(saldo, valor, extrato, LIMITE_SAQUE, numero_saques)

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()