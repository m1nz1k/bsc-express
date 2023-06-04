from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
# Создание объекта опций Chrome
chrome_options = Options()

# Включение headless-режима
chrome_options.add_argument('--headless')
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")  # Замените "Your User Agent" на ваш по

def get_dividends():
    driver = webdriver.Chrome(options=chrome_options)


    try:
        driver.get("https://bcs-express.ru/dividednyj-kalendar")
        # Нахождение элемента таблицы по классу
        table_element = driver.find_element(By.CLASS_NAME, "S7ur")

        # Нахождение всех строк таблицы
        rows = table_element.find_elements(By.CSS_SELECTOR, "[data-component='table-row']")

        # Создание списка для хранения результатов
        data_dividends = []

        # Обход строк таблицы
        for row in rows:
            # Нахождение ячеек в строке
            cells = row.find_elements(By.CSS_SELECTOR, "[data-id='table-cell']")

            # Извлечение значений из ячеек и добавление их в список результатов
            name = cells[0].text
            last_day_to_buy = cells[1].text
            dividend_closure_date = cells[2].text
            dividend_size = cells[3].text
            closing_price = cells[4].text
            dividend_yield = cells[5].text

            data_dividends.append([name, last_day_to_buy, dividend_closure_date, dividend_size, closing_price, dividend_yield])


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        # Создание DataFrame с помощью pandas
        df = pd.DataFrame(data_dividends, columns=["Наименование", "Последний день для покупки акций", "Дата закрытия реестра под дивиденды", "Размер дивиденда", "Цена акции на закрытие", "Дивидендная доходность, %"])

        # Сохранение DataFrame в Excel-файл
        df.to_excel("dividends.xlsx", index=False)
        print('Скрипт завершил работу.')

get_dividends()