from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from nltk.corpus import stopwords
import html2text as h2t
import re
import time

email1 = 'emailexample1@inbox.lv'
email2 = 'emailexample2@inbox.lv'
urls = ['https://github.com/password_reset', 'https://trello.com/forgot', 'https://9gag.com/recover', 'https://www.allmusic.com/forgot-password',
        'https://kr.battle.net/account/recovery/en/identify-account.html?requestType=PASSWORD_RESET', 'https://new.edmodo.com/account_recovery',
        'https://gen.xyz/account/pwreset.php', 'https://www.netflix.com/ru-en/LoginHelp', 'https://ltv.tapjoy.com/s/l#session/forgot',
        'https://twitter.com/account/begin_password_reset', 'https://vimeo.com/forgot_password',
        'https://www.duolingo.com/forgot_password', 'https://nanowrimo.org/forgot-password']

# urls = ['https://ltv.tapjoy.com/s/l#session/forgot', 'https://nanowrimo.org/forgot-password']


def htmlToText(html):
    h = h2t.HTML2Text()
    h.ignore_links = True
    text = h.handle(html)
    text = re.sub(r'\*\s+.*|#+\s*.*', '', text)
    text = re.sub(r'!\S+', '', text)
    text = re.sub(r'\S.jpeg|\S.jpg|\S.svg|\S.png', '', text)
    text = text.lower()
    text = text.replace("'", ' ')
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    stop_words = set(stopwords.words('english'))
    stop_words.difference_update({'should', 'no', 'not'})
    stop_words.update({'one', 'distribution', 'ace', 'rewards', 'cookies', 'create', 'online', 'music', 'youtube', 'english',
                       'video', 'privacy', 'terms', 'upload', 'new', 'love', 'espaol', 'portugus', 'streaming', 'log'})
    for word in text.split():
        if(word in stop_words):
            text = re.sub(rf'\b{word}\b', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text


'''
Метод для поиска поля ввода email
Принимает лист из WebEelement, возрващает найденный WebElement или None
'''


def find_email_input(elements):
    if len(elements) == 1:
        return elements[0]
    elements1 = []
    for element in elements:
        type_attr = element.get_attribute("type")
        if type_attr is not None and re.search(r'text|mail|account|user', type_attr, re.IGNORECASE) and (element not in elements1):
            elements1.append(element)
    if len(elements1) == 1:
        return elements1[0]
    elements2 = []
    for element in elements:
        name_attr = element.get_attribute("name")
        if name_attr is not None and re.search(r'mail|account|user', name_attr, re.IGNORECASE) and (element not in elements2):
            elements2.append(element)
    if len(elements2) == 1:
        return elements2[0]
    elements3 = []
    for element in elements:
        placeholder_attr = element.get_attribute("placeholder")
        if placeholder_attr is not None and re.search(r'@|mail|user|account|example', placeholder_attr, re.IGNORECASE) and (element not in elements3):
            elements3.append(element)
    if len(elements3) == 1:
        return elements3[0]
    return None


'''
Метод для поиска кнопки сброса пароля
Возвращает WebElement или None
'''


def find_button(driver):
    inputs = driver.find_elements_by_tag_name("input")
    buttons = driver.find_elements_by_tag_name("button")
    if buttons:
        buttons1 = []
        for element in buttons:
            element_html = element.get_attribute("outerHTML")
            soup = BeautifulSoup(element_html, "html.parser")
            type_attr = soup.find("button").attrs.get("type")
            if isinstance(type_attr, list):
                type_attr = " ".join(type_attr)
            # type_attr = element.get_attribute("type")
            if type_attr is not None and re.search(r'submit', type_attr, re.IGNORECASE) and (element not in buttons1):
                buttons1.append(element)
        if len(buttons1) == 1:
            return buttons1[0]
        buttons2 = []
        for element in buttons:
            element_html = element.get_attribute("outerHTML")
            soup = BeautifulSoup(element_html, "html.parser")
            class_attr = soup.find("button").attrs.get("class")
            if isinstance(class_attr, list):
                class_attr = " ".join(class_attr)
            # class_attr = element.get_attribute("class")
            if class_attr is not None and re.search(r'recover|next|forgot|pass', class_attr, re.IGNORECASE) and (element not in buttons2):
                buttons2.append(element)
        if len(buttons2) == 1:
            return buttons2[0]
    inputs1 = []
    for element in inputs:
        element_html = element.get_attribute("outerHTML")
        soup = BeautifulSoup(element_html, "html.parser")
        type_attr = soup.find("input").attrs.get("type")
        if isinstance(type_attr, list):
            type_attr = " ".join(type_attr)
        # type_attr = element.get_attribute("type")
        if type_attr is not None and re.search(r'submit|but|btn|', type_attr, re.IGNORECASE) and (element not in inputs1):
            inputs1.append(element)
    if len(inputs1) == 1:
        return inputs1[0]
    inputs2 = []
    for element in inputs:
        element_html = element.get_attribute("outerHTML")
        soup = BeautifulSoup(element_html, "html.parser")
        value_attr = soup.find("input").attrs.get("value")
        if isinstance(value_attr, list):
            value_attr = " ".join(value_attr)
        # value_attr = element.get_attribute("value")
        if value_attr is not None and re.search(r'submit|send|reset|continue|next|email|search|help', value_attr, re.IGNORECASE) and (element not in inputs2):
            inputs2.append(element)
    if len(inputs2) == 1:
        return inputs2[0]
    inputs3 = []
    for element in inputs:
        element_html = element.get_attribute("outerHTML")
        soup = BeautifulSoup(element_html, "html.parser")
        class_attr = soup.find("input").attrs.get("class")
        if isinstance(class_attr, list):
            class_attr = " ".join(class_attr)
        # class_attr = element.get_attribute("class")
        if class_attr is not None and re.search(r'btn|but', class_attr, re.IGNORECASE) and (element not in inputs3):
            inputs3.append(element)
    if len(inputs3) == 1:
        return inputs3[0]
    return None


def reset_pas(driver, url, email):
    count = 0
    timeout = False
    while(1):
        try:
            if not timeout:
                driver.get(url)
            # Найти все элементы с тэгом input
            elements = driver.find_elements_by_tag_name("input")
            # Найти среди них поле ввода email
            element = find_email_input(elements)
            if element is None:
                print("Email input field not found")
                return False
            # Ввести в поле данные
            element.send_keys(email)
            time.sleep(1)
            # Нажать Enter
            element.send_keys(Keys.ENTER)
            while(1):
                page_state = driver.execute_script("return document.readyState;")
                if page_state == "complete":
                    break
            time.sleep(1)
            return driver.page_source
        except ElementNotInteractableException:
            if count > 2:
                print("Element not interactable 3 times")
                return False
            count += 1
        except TimeoutException:
            timeout = True


def main():
    options = webdriver.ChromeOptions()
    # Скрыть окно браузера или нет
    options.headless = False
    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
    driver.set_page_load_timeout(10)
    driver.get('https://www.google.com/')
    for url in urls:
        print('*' * 10, url, '*' * 10)

        html1 = reset_pas(driver, url, email2)
        if not html1:
            continue
        html2 = reset_pas(driver, url, email2)
        if not html2:
            continue
        html3 = reset_pas(driver, url, email2)
        if not html3:
            continue
        html4 = reset_pas(driver, url, email1)
        if not html4:
            continue

        # text1 = htmlToText(html1)
        text2 = htmlToText(html2)
        text3 = htmlToText(html3)
        text4 = htmlToText(html4)

        # print(text2)
        # print(text3)

        if text2 != text3:
            print("Do not know")
        else:
            if text2 == text4:
                print("No")
            else:
                print("Yes")


if __name__ == '__main__':
    main()
