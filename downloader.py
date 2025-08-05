from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time, os
from utils import *

# Tudo de um semestre
def navigate_all_materiais(driver, url, download_path, target_folder, stats):
  materiais = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Material didático')]")

  for i in range(len(materiais)):
    material = materiais[i]
    material.click()

    navigate_disciplina(driver, url, download_path, target_folder, stats)

    driver.get(url)
    materiais = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Material didático')]")

# Tudo de uma disciplina
def navigate_disciplina(driver, url, download_path, target_folder, stats, is_pagination=False,):
  # Se não for paginação, criar pasta da disciplina
  if not is_pagination:
    title = get_title(driver)
    target_folder = make_folder(target_folder, title)
    
    if title not in stats["subjects"]:
      stats["subjects"].append(title)

  table = get_table(driver)
  downloaded_files_count = 0
  skipped_files_count = 0

  for i in range(len(table)):
    tr = table[i]
    links = tr.find_elements(by=By.TAG_NAME, value = 'a')

    try:
      if links[1].get_attribute('type') == 'default':
        links[1].click()

        # Baixar material
        navigate_disciplina(driver, url, download_path, target_folder, stats)
        driver.back()

        table = get_table(driver)

      elif not file_exists(links[1].get_attribute('innerHTML'), target_folder):
        downloaded_files_count += 1
        links[1].click()
      else:
        skipped_files_count += 1

    except Exception:
      continue
  
  time.sleep(1)
  wait_for_downloads(download_path, downloaded_files_count)

  # Mover para targe folder
  move(download_path, target_folder)

  stats["downloaded_files_count"] += downloaded_files_count
  stats["skipped_files_count"] += skipped_files_count
  # Checar paginação
  check_pagination(driver, url, download_path, target_folder, stats)

def wait_for_downloads(download_dir, size):
  timeout = 60 * (size if size != 0 else 1) 

  seconds = 0
  while seconds < timeout:
    if not any((filename.endswith(".tmp") or filename.endswith('.crdownload')) for filename in os.listdir(download_dir)):
      return True
    time.sleep(1)
    seconds += 1
  raise TimeoutError("Download did not complete within the given timeout.")

def check_pagination(driver, url, download_path, target_folder, stats):
  try:
    pagination = driver.find_element(by=By.CLASS_NAME, value='pagination')
    pages = pagination.find_elements(by=By.TAG_NAME, value='li')

    next_button = pages[-1]
    if 'disabled' not in next_button.get_attribute('class'):
      next_button.click()
      navigate_disciplina(driver, url, download_path, target_folder, stats, True)
    
  except Exception as e:
    return
  
def open_semester(url, path, folder, semester):
  options = Options()
  prefs = {
    "download.default_directory": path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False
  }

  options.add_argument("--headless=new")
  options.add_experimental_option('prefs', prefs)

  driver = webdriver.Chrome(options=options)
  driver.get(url)

  # Criar pasta do semestre
  semester_path = make_folder(path, folder)

  stats = {
    "semester": semester[-1],
    "subjects": [],
    "downloaded_files_count": 0,
    "skipped_files_count": 0
  }

  if '/file' in url:
    navigate_disciplina(driver, url, path, semester_path, stats)
  else:
    navigate_all_materiais(driver, url, path, semester_path, stats)

  driver.quit()

  stats["date"] = datetime.now().strftime("%x")
  stats["time"] = datetime.now().strftime("%X")

  return stats
