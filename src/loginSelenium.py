from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import re
from DBClient import *
from user_settings import BENEFIT
import datetime

# ---headON mode---------
# driver = webdriver.Chrome()

# #---headless mode-----------------------------


options = webdriver.ChromeOptions()
# ---headlessで動かすために必要なオプション---
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# メイン処理
url = "https://www.benefit401k.com/customer/RkDCMember/Common/JP_D_BFKLogin.aspx"
# Google検索画面にアクセス
driver.get(url)

# htmlからStringを探しsend_keysでStringを入力する
txtUserID = driver.find_element_by_name("txtUserID")
txtUserID.send_keys(BENEFIT['user'])

txtUserID = driver.find_element_by_name("txtPassword")
txtUserID.send_keys(BENEFIT['password'])

# 探してきたボタンなどをクリックする
driver.find_element_by_link_text("ログイン").click()

driver.find_element_by_link_text("資産残高を詳しく見る").click()

profitAndLoss = driver.find_element_by_xpath(
    "/html/body/form/div[1]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td").text

# htmlのPath(String)で探したあとにinnerText値取得
profitAndLossRatio = driver.find_element_by_xpath(
    "/html/body/form/div[1]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td").text

print(datetime.datetime.today())
print(profitAndLoss)
print(profitAndLossRatio)

profitAndLossList = driver.find_element_by_xpath(
    "/html/body/form/div[1]/div[3]/div[2]/div[2]/table[1]/tbody/tr/td/table")
profitAndLossList = profitAndLossList.find_elements_by_tag_name("tr")
profitAndLossList.pop(0)

histories = list()

for i, row in enumerate(profitAndLossList):
    # 損益と損益率を取得するための一時変数にいれている
    tmp = row.find_element_by_xpath(".//td[7]").text.split("\n")

    # 待機資金は処理しない
    product_type = row.find_element_by_xpath(".//td[1]").text
    if product_type == '待機資金':
        continue
    history = History(
        product_name=row.find_element_by_xpath(".//td[2]").text,
        balance=re.sub('[\D\.]', '', row.find_element_by_xpath(".//td[5]").text),
        price=row.find_element_by_xpath(".//td[6]").text.replace("円", "").replace(",", ""),
        pl_price=tmp[0].replace("円", "").replace(",", ""),
        pl_rate=tmp[1].replace("％", "")
    )
    histories.append(history)

# print(items)
# 最後に必ず明記する　もし明記せず実行を繰り返すとメモリーを大量に使われる
driver.quit()

db_client = DBClient()
connect = db_client.get_connect()
connect.add_all(histories)

# for row in connect.query(Product).all():
#     print(row.id, row.name, row.type)
#
# for row in connect.query(History).all():
#     print(row.id, row.balance, row.price, row.pl_price, row.pl_rate)

connect.commit()
