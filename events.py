from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
# Создание объекта опций Chrome
chrome_options = Options()

# Включение headless-режима
chrome_options.add_argument('--headless')
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")  # Замените "Your User Agent" на ваш по

def get_events():
    driver = webdriver.Chrome(options=chrome_options)
    data_events = []
    try:
        driver.maximize_window()
        driver.get("https://bcs-express.ru/ozhidaemye-sobytiya")
        # Нахождение всех элементов таблицы событий
        events = driver.find_elements(By.CLASS_NAME, "events-table__item")

        # Итерация по каждому элементу таблицы и извлечение данных
        for event in events:
            date = event.find_element(By.CLASS_NAME, "events-table__item-date").text
            event_name = event.find_element(By.CLASS_NAME, "events-table__item-event").text
            importance = event.find_element(By.CLASS_NAME, "events-table__item-importance").get_attribute("class")

            # Обработка класса важности для определения фактической важности
            if "_high" in importance:
                importance = "High"
            elif "_medium" in importance:
                importance = "Medium"
            elif "_low" in importance:
                importance = "Low"
            else:
                importance = "Unknown"

            # Добавление данных в список
            data_events.append([date, event_name, importance])

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        # Создание DataFrame с помощью pandas
        df = pd.DataFrame(data_events, columns=["Дата", "Событие", "Важность"])

        # Сохранение DataFrame в Excel-файл
        df.to_excel("events.xlsx", index=False)
        print('Скрипт завершил работу.')

get_events()
