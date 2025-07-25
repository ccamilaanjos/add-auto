import pyautogui
import time
import webbrowser
from data import data_code_path

def print_subjects_by_semester(semester):
  print(list(data_code_path[semester][1].keys()))

def main():
  url_ads = 'https://ads.ifba.edu.br/'

  semester = 0
  while semester < 1 or semester > 6:
    semester = int(input('Digite o número do semestre (1-6): ')) # TODO: Adicionar validação

    print('\n')
    print_subjects_by_semester(semester)
    print('\n')
    sub = str(input('Insira o código da disciplina (ou 0 para baixar todas do semestre): ')) # TODO: Adicionar validação
    
    if sub == 0:
      print() # baixar todas
    
    else:
      webbrowser.open(url_ads + 'file' + (data_code_path[semester][1][f'{sub}']))
      time.sleep(1)
      pyautogui.press('enter')

if __name__ == "__main__":
  main()