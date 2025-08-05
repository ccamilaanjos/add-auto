import shutil, os
from selenium.webdriver.common.by import By

def make_folder(path, folder):
  subfolder_path = os.path.join(path, folder)
  os.makedirs(subfolder_path, exist_ok=True)

  return subfolder_path

def file_exists(file_name, folder):
  file_path = os.path.join(folder, file_name)
  if os.path.exists(file_path):
    return True
  return False

def move(download_path, target_folder):
  os.makedirs(target_folder, exist_ok=True)

  for item in os.listdir(download_path):
    if item == "download_log.txt":
      continue

    base, ext = os.path.splitext(item)
    src_path = os.path.join(download_path, item)
    dst_path = os.path.join(target_folder, item)
    counter = 1

    if os.path.isfile(src_path):
      while os.path.exists(dst_path):
        dst_path = os.path.join(target_folder, f'{base} ({counter}){ext}')
        counter += 1

      shutil.move(src_path, dst_path)

def get_title(driver):
  h1 = driver.find_element(by=By.CLASS_NAME, value='pagetitle')
  title = h1.find_element(by=By.TAG_NAME, value = 'a')
  title = title.get_attribute('innerHTML')
  
  return title.strip()

def get_table(driver):
  table = driver.find_element(by=By.CLASS_NAME, value='table')
  table = table.find_element(by=By.TAG_NAME, value='tbody')
  table = table.find_elements(by=By.TAG_NAME, value='tr')
  table = table[1:]

  return table
