from typing import List, Any
import time

import selenium
import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# phantom = dict(DesiredCapabilities.PHANTOMJS)
# phantom["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
#     "Chrome/74.0.3729.169 YaBrowser/19.6.0.1574 Yowser/2.5 Safari/537.36")
# phantom["browserName"] = ("Mozilla Firefox")
# browser = webdriver.PhantomJS(desired_capabilities=phantom)
# browser.set_window_size(1600, 900)
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox()

browser.get('https://www.myscore.ru/')

team_one_goal = 0
team_two_goal = 0
team_one_missing = 0
team_two_missing = 0

team_one_goal_home = 0
team_two_goal_home = 0
team_one_goal_away = 0
team_two_goal_away = 0
team_one_missing_home = 0
team_one_missing_away = 0
team_two_missing_home = 0
team_two_missing_away = 0

The_end = []
z = -1
garbage = 0
try:
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "tabs__text")))
except selenium.common.exceptions.TimeoutException:
    browser.refresh()
    browser.refresh()
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "tabs__text")))

browser.find_elements_by_class_name("tabs__text")[1].click()

List_scroll = browser.find_elements_by_css_selector(".event__expander.icon--expander.expand")


for x in List_scroll:
    try:
        List_scroll[z].click()
        z -= 1
    except selenium.common.exceptions.ElementClickInterceptedException:
        y = int(x.location.get("y")) - 30
        browser.execute_script("window.scrollTo(0," + str(y) + ")")
        List_scroll[z].click()
        z -= 1
    except selenium.common.exceptions.ElementClickInterceptedException:
        y = int(x.location.get("y")) + 30
        browser.execute_script("window.scrollTo(0," + str(y) + ")")
        List_scroll[z].click()
        z -= 1

browser.execute_script("window.scrollTo(0, 0)")
List_match = browser.find_elements_by_class_name("event__match")
# Время матча
List_garbage = browser.find_elements_by_class_name("event__stage--block")

for x in List_garbage:
    try:
        if int(str(x.text).replace("+", "")) > 20:
            List_match.__delitem__(garbage)
        else:
            print(str(x.text).replace("+", ""))
            garbage += 1
    except ValueError:
        List_match.__delitem__(garbage)
        # garbage += 1


# if List_match.__len__() == 0:
#     List_garbage = browser.find_elements_by_class_name("event__stage--block")
#     garbage = 0
#     print("25")
#     for x in List_garbage:
#         try:
#             if int(str(x.text).replace("+", "")) > 25:
#                 List_match.__delitem__(garbage)
#             else:
#                 garbage += 1
#         except ValueError:
#             garbage += 1
# elif List_match.__len__() == 0:
#     List_garbage = browser.find_elements_by_class_name("event__stage--block")
#     garbage = 0
#     print("35")
#     for x in List_garbage:
#         try:
#             if int(str(x.text).replace("+", "")) > 35:
#                 List_match.__delitem__(garbage)
#             else:
#                 garbage += 1
#         except ValueError:
#             garbage += 1

for x in List_match:
    try:
        try:
            x.click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            up = int(x.location.get("y")) + 30
            browser.execute_script("window.scrollTo(0," + str(up) + ")")
            x.click()
        # except selenium.common.exceptions.StaleElementReferenceException:
        browser.switch_to.window(browser.window_handles[-1])
        element = WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                                   '//*[@id="li-match-head-2-head"]')))

        browser.find_element_by_class_name("li2").click()
        # Проверка загрузки последних матчей
        try:
            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                             'table/thead/tr/td')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
        try:
            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[1]/table/'
                                                                             'tbody/tr[1]/td[@class="name highTeam"]')))

            name_one_team = browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/'
                                                          'tbody/tr[1]/td[@class="name highTeam"]').text
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                             'table/tbody/tr[1]/td[2]')))
            browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[1]/td[2]').click()

            WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                         '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                             'table/tbody/tr[1]/td[2]')))
            # Находим количество матчей
            max_match = browser.find_elements_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr').__len__()
            if max_match < 5:
                for y in range(1, max_match + 1):
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                                     'table/tbody/tr[' + str(
                                                                                         y) + ']/td[2]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                                     'table/tbody/tr[' + str(
                                                                                         y) + ']/td[2]')))
                    browser.find_element_by_xpath(
                        '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        try:
                            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                             '//*[@id="flashscore"]/div[1]/'
                                                                                             'div[1]/div[2]/div/div/a')))
                        except selenium.common.exceptions.TimeoutException:
                            browser.close()
                            browser.switch_to.window(browser.window_handles[-1])
                            browser.find_element_by_xpath(
                                '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                            browser.switch_to.window(browser.window_handles[-1])

                        if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a') \
                                .text.find(name_one_team) == -1:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-summary"]')))
                            team_one_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                            team_one_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                            team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                  'div[1]/div[1]/div[2]/span[1]').text)
                        else:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-summary"]')))
                            team_one_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                            team_one_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[1]').text)
                            team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                  'div[1]/div[1]/div[2]/span[2]').text)
                        browser.close()
                        browser.switch_to.window(browser.window_handles[-1])
                    except selenium.common.exceptions.NoSuchElementException:
                        print("Чет не получилось )")
                    except ImportError:
                        print("Не нашел счет, ля!")
            else:
                for y in range(1, 6):
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                                 'table/tbody/tr[' + str(y) + ']/td[2]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                                     'table/tbody/tr[' + str(
                                                                                         y) + ']/td[2]')))
                    browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        try:
                            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="flashscore"]/div[1]/'
                                                                                         'div[1]/div[2]/div/div/a')))
                        except selenium.common.exceptions.TimeoutException:
                            browser.close()
                            browser.switch_to.window(browser.window_handles[-1])
                            browser.find_element_by_xpath(
                                '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                            browser.switch_to.window(browser.window_handles[-1])

                        if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a')\
                                .text.find(name_one_team) == -1:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                        '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                            '//*[@id="li-match-summary"]')))
                            team_one_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                            team_one_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                            team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                       'div[1]/div[1]/div[2]/span[1]').text)
                        else:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                        '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                            '//*[@id="li-match-summary"]')))
                            team_one_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                            team_one_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[1]').text)
                            team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                        browser.close()
                        browser.switch_to.window(browser.window_handles[-1])
                    except selenium.common.exceptions.NoSuchElementException:
                        print("Чет не получилось )")
                    except ImportError:
                        print("Не нашел счет, ля!")
        except selenium.common.exceptions.TimeoutException:
            print("Нет инфы у первой команды")
            name_one_team = "Не найдено"

        except selenium.common.exceptions.NoSuchElementException:
            print("Нету инфы!")
        except selenium.common.exceptions.TimeoutException:
            print("Хз, чет не смог он найти.")
        try:
            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[2]/table/'
                                                                             'tbody/tr[1]/td[@class="name highTeam"]')))
            # Находим название второй команды
            name_two_team = browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/'
                                                          'tbody/tr[1]/td[@class="name highTeam"]').text

            WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                         '//*[@id="tab-h2h-overall"]/div[2]/'
                                                                         'table/tbody/tr[1]/td[2]')))
            # Находим количество матчей
            max_match = browser.find_elements_by_xpath('/html/body/div[1]/div[1]/div[3]/div[9]/'
                                              'div[2]/div[4]/div[2]/table/tbody/tr').__len__()
            # print("Max match " + str(max_match))
            if max_match < 5:
                for y in range(1, max_match + 1):
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="tab-h2h-overall"]/div[2]/'
                                                                                 'table/tbody/tr[' + str(y) + ']/td[2]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="tab-h2h-overall"]/div[2]/'
                                                                                     'table/tbody/tr[' + str(
                                                                                         y) + ']/td[2]')))
                    browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        try:
                            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="flashscore"]/div[1]/'
                                                                                         'div[1]/div[2]/div/div/a')))
                        except selenium.common.exceptions.TimeoutException:
                            browser.close()
                            browser.switch_to.window(browser.window_handles[-1])
                            browser.find_element_by_xpath(
                                '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                            browser.switch_to.window(browser.window_handles[-1])

                        if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a')\
                                .text.find(name_two_team) == -1:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-summary"]')))
                            team_two_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                             '//*[@id="summary-content"]/'
                                                                                            'div[1]/div[1]/div[2]/span[2]')))
                            team_two_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                            team_two_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                       'div[1]/div[1]/div[2]/span[1]').text)
                        else:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                        '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                            '//*[@id="li-match-summary"]')))
                            team_two_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                            team_two_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[1]').text)
                            team_two_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                        browser.close()
                        browser.switch_to.window(browser.window_handles[-1])
                    except selenium.common.exceptions.NoSuchElementException:
                        print("Чет не получилось )")
                    except ImportError:
                        print("Не нашел гол, ля!")
            else:
                for y in range(1, 6):
                    try:
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="tab-h2h-overall"]/div[2]/'
                                                                                 'table/tbody/tr[' + str(y) + ']/td[2]')))
                    except selenium.common.exceptions.TimeoutException:
                        browser.refresh()
                        WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                     '//*[@id="tab-h2h-overall"]/div[2]/'
                                                                                     'table/tbody/tr[' + str(
                                                                                         y) + ']/td[2]')))
                    browser.find_element_by_xpath('//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        try:
                            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                         '//*[@id="flashscore"]/div[1]/'
                                                                                         'div[1]/div[2]/div/div/a')))
                        except selenium.common.exceptions.TimeoutException:
                            browser.close()
                            browser.switch_to.window(browser.window_handles[-1])
                            browser.find_element_by_xpath(
                                '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                            browser.switch_to.window(browser.window_handles[-1])

                        if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a')\
                                .text.find(name_two_team) == -1:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="li-match-summary"]')))
                            team_two_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                            WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                             '//*[@id="summary-content"]/'
                                                                                            'div[1]/div[1]/div[2]/span[2]')))
                            team_two_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                            team_two_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                       'div[1]/div[1]/div[2]/span[1]').text)
                        else:
                            try:
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                        '//*[@id="li-match-head-2-head"]')))
                            except selenium.common.exceptions.TimeoutException:
                                browser.refresh()
                                WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                            '//*[@id="li-match-summary"]')))
                            team_two_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                            team_two_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[1]').text)
                            team_two_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                                    'div[1]/div[1]/div[2]/span[2]').text)
                        browser.close()
                        browser.switch_to.window(browser.window_handles[-1])
                    except selenium.common.exceptions.NoSuchElementException:
                        print("Чет не получилось )")
                    except ImportError:
                        print("Не нашел гол, ля!")
        except selenium.common.exceptions.TimeoutException:
            print("Нет инфы у второй команды")
            name_two_team = "Не найдено"
        except selenium.common.exceptions.NoSuchElementException:
            print("Нету инфы!")
        The_end.append(name_one_team + " - " + str((team_one_goal / 5) * 100) + "%" + " | " +
                       str((team_two_goal / 5) * 100) + "%" + " - " + name_two_team)

        try:
            one = team_one_goal/team_one_missing
        except ZeroDivisionError:
            one = 0
        # try:
        #     two = (team_one_goal_away*2)/(team_two_missing_home*2)
        # except ZeroDivisionError:
        #     two = 0
        try:
            three = team_two_goal/team_two_missing
        except ZeroDivisionError:
            three = 0
        # try:
        #     four = (team_two_goal_away*2)/(team_one_missing_home*2)
        # except ZeroDivisionError:
        #     four = 0

        The_end.append(name_one_team + " - " + str(round(one, 2)) + " | " + str(round(three, 2))
                       + " - " + name_two_team + "\n")
        print(name_one_team + " | " + name_two_team)

        team_one_goal = 0
        team_two_goal = 0
        team_one_missing = 0
        team_two_missing = 0

        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        with open('List_chapter.txt', 'a', encoding='utf-8') as file1:
            file1.writelines("%s\n" % place for place in The_end)
        The_end.clear()
    except IndexError:
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        print("Где этот сраный матч??")

browser.close()

