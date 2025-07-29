from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url_ads = 'https://ads.ifba.edu.br/Semestre-1'

def navigate_materiais(driver):
  materiais = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Material didático')]")

  for i in range(len(materiais)):
    material = materiais[i]
    material.click()

    download_materiais()

    driver.get(url_ads)
    materiais = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Material didático')]")

def download_materiais():
  print("Baixando os materiais...")

def main():
  options = Options()
  # Ative essa opção para rodar em segundo plano
  options.add_argument("--headless=new")

  driver = webdriver.Chrome(options=options)

  driver.get(url_ads)
  navigate_materiais(driver)
  driver.quit()

if __name__ == "__main__":
  main()
