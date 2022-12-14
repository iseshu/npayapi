from flask import Flask,request,jsonify
from flask_cors import CORS
from seleniumwire import webdriver
from bs4 import BeautifulSoup
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {'Access-Control-Allow-Origin': '*'}})
op = webdriver.ChromeOptions()
#op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
op.add_argument('--headless')
op.add_argument('--no-sandbox')
op.add_argument('--disable-dev-sh-usage')



def get(pageSource,mobile):
    try:
        soup = BeautifulSoup(pageSource,"html.parser")
        name = soup.find("span",id="firstname").text
        id = soup.find("span",id="lblStuID").text
        f_name = soup.find("span",id="lblFatherName").text
        b_name = soup.find("span",id="lblMotherName").text
        clas = soup.find("span",id="lblCode").text
        due = soup.find("span",id="lblBalanceAmount").text
        #mobile = soup.find("span",id="mobile").text
        return {"status":True,"due_amount":due,"mobile":mobile,"father_name":f_name,"name":name,"id_no":id,"branch":b_name,"class_n":clas}
    except:
        return {"status":False}

@app.route("/")
def home():
    return {"status":True}


@app.route("/get")
def do():
    a= request.args.get("id")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://payonline.narayanagroup.com/")
    id_num = driver.find_element_by_id("txtUid")
    id_num.send_keys(int(a))
    btn = driver.find_element_by_id("BtnStuGetData")
    btn.click()
    pageSource = driver.page_source
    amount = driver.find_element_by_id("txtCourseFee")
    amount.send_keys(1280)
    btn1 = driver.find_element_by_id("btnsubmit")
    btn1.click()
    for reqest in driver.requests:
        if reqest.url == "https://secure.payu.in/_payment":
            phone = reqest.params['phone']
    data = get(pageSource,phone)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

