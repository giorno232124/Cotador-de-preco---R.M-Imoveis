import csv
import sys

class Simulacao:
    def __init__(self, tipo, valor_aluguel, quartos, vagas, tem_crianca=None):
        self.tipo = tipo
        self.valor_aluguel_mensal = valor_aluguel
        self.valor_contrato = 0
        self.quartos = quartos
        self.vagas = vagas
        self.tem_crianca = 'Sim' if tem_crianca else ('Não' if tem_crianca is False else 'N/A')
        self.num_parcelas_contrato = 0
        self.valor_parcela_contrato = 0.0
        self.total_mensal_com_parcela = valor_aluguel


class ImobiliariaApp:
    
    def __init__(self, valor_contrato=2000):
        self.valor_contrato_padrao = valor_contrato
        self.simulacoes_salvas = []
        print('--- Aplicação R.M Imobiliaria (POO) ---')

    def _confirmar_interesse(self):
        print('\nIrei te fazer umas perguntas sobre seu imovel, tudo bem? ')
        opcao_aceitar = input('Digite sua opcao (Sim/Não): ').strip().lower()
        if opcao_aceitar in ('sim', 's'):
            print('Perfeito, daremos continuidade!')
            return True
        else:
            print('Retornando ao menu principal...')
            return False

    def _apresentar_resultado_e_salvar(self, simulacao):
        
        simulacao.valor_contrato = self.valor_contrato_padrao
        
        print(f'\n--- Resumo da Simulação ({simulacao.tipo}) ---')
        print(f'Valor total do aluguel estimado mensal: R$ {simulacao.valor_aluguel_mensal:.2f}')
        print(f'Valor total do contrato: R$ {simulacao.valor_contrato:.2f}')
        
        total_com_contrato = simulacao.valor_aluguel_mensal + simulacao.valor_contrato
        print(f'Valor total (Aluguel + Contrato): R$ {total_com_contrato:.2f}')
        
        print('\nVoce tem interesse em parcelar o contrato (Sim/Não)? ')
        resposta = input('').strip().lower()
        
        if resposta in ('s', 'sim'):
            try:
                parcelas = int(input('Quantas vezes voce tem interesse em parcelar? (Max 5x): '))
                if parcelas <= 0:
                    parcelas = 1
                elif parcelas > 5:
                    parcelas = 5
                
                valor_parcelado = self.valor_contrato_padrao / parcelas
                simulacao.num_parcelas_contrato = parcelas
                simulacao.valor_parcela_contrato = valor_parcelado
                simulacao.total_mensal_com_parcela = simulacao.valor_aluguel_mensal + valor_parcelado
                
                print(f'\nO valor da parcela do contrato será: {parcelas}x de R$ {valor_parcelado:.2f}')
                print(f'O valor total do pagamento mensal (Aluguel + Parcela) será de: R$ {simulacao.total_mensal_com_parcela:.2f}')
                
            except ValueError:
                print("Número de parcelas inválido. Contrato não será parcelado.")
        
        self.simulacoes_salvas.append(simulacao)
        print(f"\n[OK] Simulação para '{simulacao.tipo}' salva.")
        print('-------------------------------------------')

    def _simular_apartamento(self):
        valor_base = 700
        print('\n--- Opção: Apartamento ---')
        
        if not self._confirmar_interesse():
            return

        try:
            qnt_quartos = int(input('Quantos quartos voce tem interesse? '))
            qnt_vagas = int(input('Quantas vagas de garagem voce tem interesse? '))
            
            adicional_garagem = (qnt_vagas - 1) * 300 if qnt_vagas > 1 else 0
            adicional_quarto = (qnt_quartos - 1) * 200 if qnt_quartos > 1 else 0

            if adicional_garagem > 0:
                print(f'[+] Adicional de R$ {adicional_garagem} por {qnt_vagas - 1} vaga(s) extra(s).')
            if adicional_quarto > 0:
                print(f'[+] Adicional de R$ {adicional_quarto} por {qnt_quartos - 1} quarto(s) extra(s).')

            print('Você possui alguma criança (Sim/Não)? ')
            opcao_crianca = input('').strip().lower()
            tem_crianca = True
            desconto_crianca = 0

            if opcao_crianca in ('não', 'n'):
                tem_crianca = False
                valor_preliminar = valor_base + adicional_garagem + adicional_quarto
                desconto_crianca = valor_preliminar * 0.05
                print(f'[-] Desconto de R$ {desconto_crianca:.2f} (5%) por não ter crianças.')
            
            valor_total_aluguel = valor_base + adicional_garagem + adicional_quarto - desconto_crianca

            simulacao = Simulacao(
                tipo="Apartamento",
                valor_aluguel=valor_total_aluguel,
                quartos=qnt_quartos,
                vagas=qnt_vagas,
                tem_crianca=tem_crianca
            )
            
            self._apresentar_resultado_e_salvar(simulacao)

        except ValueError:
            print("[ERRO] Entrada inválida. Por favor, digite apenas números.")
            
    def _simular_casa(self):
        valor_base = 900
        print('\n--- Opção: Casa ---')
        
        if not self._confirmar_interesse():
            return

        try:
            qnt_quartos = int(input('Quantos quartos voce tem interesse? '))
            qnt_vagas = int(input('Quantas vagas de garagem voce tem interesse? '))
            
            adicional_garagem = (qnt_vagas - 1) * 300 if qnt_vagas > 1 else 0
            adicional_quarto = (qnt_quartos - 1) * 250 if qnt_quartos > 1 else 0

            if adicional_garagem > 0:
                print(f'[+] Adicional de R$ {adicional_garagem} por {qnt_vagas - 1} vaga(s) extra(s).')
            if adicional_quarto > 0:
                print(f'[+] Adicional de R$ {adicional_quarto} por {qnt_quartos - 1} quarto(s) extra(s).')
                
            valor_total_aluguel = valor_base + adicional_garagem + adicional_quarto
            
            simulacao = Simulacao(
                tipo="Casa",
                valor_aluguel=valor_total_aluguel,
                quartos=qnt_quartos,
                vagas=qnt_vagas
            )
            
            self._apresentar_resultado_e_salvar(simulacao)
            
        except ValueError:
            print("[ERRO] Entrada inválida. Por favor, digite apenas números.")

    def _simular_estudio(self):
        valor_base = 1200
        print('\n--- Opção: Estúdio ---')
        
        if not self._confirmar_interesse():
            return

        try:
            qnt_vagas = int(input('Quantas vagas de garagem voce tem interesse? '))
            
            adicional_garagem = (qnt_vagas - 1) * 250 if qnt_vagas > 1 else 0

            if adicional_garagem > 0:
                print(f'[+] Adicional de R$ {adicional_garagem} por {qnt_vagas - 1} vaga(s) extra(s).')
                
            valor_total_aluguel = valor_base + adicional_garagem
            
            simulacao = Simulacao(
                tipo="Estúdio",
                valor_aluguel=valor_total_aluguel,
                quartos=1,
                vagas=qnt_vagas
            )
            
            self._apresentar_resultado_e_salvar(simulacao)
            
        except ValueError:
            print("[ERRO] Entrada inválida. Por favor, digite apenas números.")

    def exportar_para_csv(self, nome_arquivo="simulacoes_imobiliaria.csv"):
        print(f"\nExportando {len(self.simulacoes_salvas)} simulação(ões) para '{nome_arquivo}'...")
        
        if not self.simulacoes_salvas:
            print("Nenhuma simulação para exportar.")
            return

        fieldnames = self.simulacoes_salvas[0].__dict__.keys()

        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for sim in self.simulacoes_salvas:
                    writer.writerow(sim.__dict__)
            
            print(f"[SUCESSO] Arquivo '{nome_arquivo}' salvo!")
        
        except IOError as e:
            print(f"[ERRO] Não foi possível escrever no arquivo: {e}")
        except Exception as e:
            print(f"[ERRO] Ocorreu um erro inesperado: {e}")

    def run(self):
        while True:
            print("\n--- Menu Principal ---")
            print("Digite a opção desejada (1-4)")
            print("1 - Simular Apartamento")
            print("2 - Simular Casa")
            print("3 - Simular Estúdio")
            print("4 - Salvar simulações (CSV) e Sair")
            
            opcao = input('Digite a opção desejada: ')
            
            if opcao == '1':
                self._simular_apartamento()
            elif opcao == '2':
                self._simular_casa()
            elif opcao == '3':
                self._simular_estudio()
            elif opcao == '4':
                self.exportar_para_csv()
                print("Obrigado por usar a R.M Imobiliaria. Saindo...")
                sys.exit()
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    app = ImobiliariaApp(valor_contrato=2000)
    app.run()