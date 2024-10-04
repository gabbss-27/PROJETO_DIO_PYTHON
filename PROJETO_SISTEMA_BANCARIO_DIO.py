# Banco de dados fictício
usuarios = []
contas = []

# Funções
def depositar(saldo, valor):
    """Deposita um valor ao saldo."""
    saldo += valor
    return saldo

def sacar(*, saldo, valor, numero_saques, limite_saques):
    """Saca um valor do saldo se as condições forem atendidas."""
    if valor <= 0:
        return saldo, "Operação falhou! O valor informado é inválido."
    if valor > saldo:
        return saldo, "Operação falhou! Você não tem saldo suficiente."
    if valor > limite:
        return saldo, "Operação falhou! O valor do saque excede o limite."
    if numero_saques >= limite_saques:
        return saldo, "Operação falhou! Número máximo de saques excedido."
    
    saldo -= valor
    numero_saques += 1
    return saldo, f"Saque: R$ {valor:.2f}\n"

def extrato(saldo, *, extrato):
    """Exibe o extrato e o saldo atual."""
    return (extrato if extrato else "Não foram realizadas movimentações."), saldo

def cadastrar_usuario():
    """Cadastra um novo usuário."""
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")
    cpf = input("CPF: ")
    
    # Verificar se o CPF já existe
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("CPF já cadastrado!")
        return

    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")
    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    print("Usuário cadastrado com sucesso!")

def cadastrar_conta(usuario):
    """Cadastra uma nova conta para um usuário."""
    conta_numero = len(contas) + 1
    conta = {
        'agencia': '0001',
        'numero_conta': conta_numero,
        'usuario': usuario
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {conta['agencia']}, Conta: {conta_numero}")

def buscar_usuario(cpf):
    """Busca um usuário pelo CPF."""
    return next((u for u in usuarios if u['cpf'] == cpf), None)

# Função principal
def main():
    saldo = 0
    limite = 500
    extrato_movimentacao = ""
    numero_saques = 0
    limite_saques = 3

    while True:
        opcao = input("""
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [cu] Cadastrar Usuário
        [cc] Cadastrar Conta Corrente
        [q] Sair

        => """)

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
                if valor <= 0:
                    raise ValueError
                saldo = depositar(saldo, valor)
                extrato_movimentacao += f"Depósito: R$ {valor:.2f}\n"
            except ValueError:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
                saldo, mensagem = sacar(saldo=saldo, valor=valor, numero_saques=numero_saques, limite_saques=limite_saques)
                if "Saque" in mensagem:
                    extrato_movimentacao += mensagem
                print(mensagem)
                numero_saques += 1 if "Saque" in mensagem else 0
            except ValueError:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            extrato_movimentacao, saldo = extrato(saldo, extrato=extrato_movimentacao)
            print("\n================ EXTRATO ================")
            print(extrato_movimentacao)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        elif opcao == "cu":
            cadastrar_usuario()

        elif opcao == "cc":
            if not usuarios:
                print("Cadastre um usuário primeiro.")
                continue
            cpf = input("Informe o CPF do usuário: ")
            usuario = buscar_usuario(cpf)
            if usuario:
                cadastrar_conta(usuario)
            else:
                print("Usuário não encontrado.")

        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Execução do programa
if __name__ == "__main__":
    main()