import sys
import time
from datetime import datetime
from pathlib import Path
from itertools import product
from functools import reduce


"""
  Criar combinacoes:
    Ex: (001), (002), (003)
"""
def create_combination(range_combination:list, num_combination:int):
  return list(product(range_combination, repeat=num_combination))

"""
  Compor os numeros do CPF baseado nas combinacoes fornecidas.

"""
def compose_cpfs(*, combinations:list, cpf:str, insert_cpf:str="last"):
  if insert_cpf not in ["last"]:
    return False
  
  results = []
  for combination in combinations:
    # Ex: (1, 2, 3) -> "123"
    aux_combination = "".join([str(n) for n in combination])
    
    if insert_cpf == "last":
      result = aux_combination + cpf
      results.append(result)
  
  return results

"""
  Busca o digito verificador do CPF - os ultimos 2 digitos.
"""
def find_VD(cpf:str):
  
  # Transforma o CPF (string) em uma lista de int:
  cpf_arr = [int(n) for n in cpf]
  
  for _ in range(2):
    # Captura os ultimos 9 digitos:
    aux_cpf = cpf_arr[-9:]

    """
    Os algarismo sao multiplicados pela sequencia: 10, 9, 8 ... 2.
    Ex:
      idx: 0 | 0
      idx: 1 | 1
      ...
      idx: 8 | 9
    
    Para facilitar a multiplicacao nessa ordem, percorremos o arr de forma inversa.
    Ex:
      idx: 2 | 9
      idx: 3 | 7
      ...
      idx: 10 | 0
    """
    result_multi = [(i + 2) * v for i, v in enumerate(aux_cpf[-1::-1])]
    
    # Reduz o arr em um unico valor:
    reduce_dv = reduce(lambda a, b: a+b, result_multi)    
    
    # Subtrai 11 do resto da divisao da multiplicacao por 11.
    resto = reduce_dv%11
    if resto <= 1:
      digit = 0
    else:
      digit = 11-resto
    
    cpf_arr.append(digit)

  final_cpf = "".join([str(n) for n in cpf_arr])
  return final_cpf


def create_file(data:list):
    filename = str(Path(__file__).parent / f"resultCPFs_qtde_{len(data)}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt")
    
    # Tratamento da quebra de linha para cada CPF.
    new_data = []
    for idx, line in enumerate(data):
      if idx == len(data) - 1:
        new_data.append(line)
      else:
        new_data.append(line + "\n")
  
    # Escrever no arquivo:
    try:
      with open(filename, "w") as f:
        f.writelines(new_data)
    except:
      return False
        
    return True



def main() -> None:
  """
  Exemplo:
    Nome: Lucas da Silva Goncalves
    CPF: ***.036.888-**
    33264668 BANCOBCO XP S.A.
    Agencia: ****
    Conta: ****
  """

  cpf_busca = "036888"
  insert_cpf = "last"
  print(f"--> Iniciando a busca do CPF: '{cpf_busca}' <--")

  """
  Criacao dos numeros de intervalo:
    Exemplo: [0, 1, 2, ...]
    Neste caso, quero o intervalo de 0 a 9
  """
  num_max_range_combination = 9
  arr_max_range_combination = [_ for _ in range(num_max_range_combination + 1)]

  """
  Combinacoes possiveis entre o intervalo do numero.
    Exemplo: 
      Combinacao = 3 -> (0, 0, 0)
      Combinacao = 2 -> (0, 0)
  """
  num_combination = 3
  result_combinations = create_combination(arr_max_range_combination, num_combination)

  """
  Compor a primeira etapa do CPF.
    Exemplo: 000.036.888
    Neste caso, ja temos os 3 digitos do meio e os 3 digitos finais da primeira etapa.
  """
  result_compose_combinations = compose_cpfs(combinations=result_combinations, cpf=cpf_busca, insert_cpf=insert_cpf)
  if result_compose_combinations is None:
    print("-> Erro ao gerar a composicao do CPF.")
    return
  
  final_generated_cpfs = list(map(find_VD, result_compose_combinations))

  result_file = create_file(final_generated_cpfs)
  if not result_file:
    print("-> Erro ao criar o arquivo dos CPFs.")
    return
  
  print(f"--> Resultado dos CPFs gerados -> '{len(final_generated_cpfs)}'")
  return


if __name__ == "__main__":
  main()  