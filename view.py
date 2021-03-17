import eel
import desktop
import pos_system_eel
import datetime

app_name="html"
end_point="index.html"
size=(700,600)

global code_list
global name_list
global price_list
global volume_list
global subtotal_list
global flag
global data_now

now = datetime.datetime.now()
data_now = now.strftime('%Y%m%d_%H%M%S')
print(data_now)
code_list = []
name_list = []
price_list = []
volume_list=[]
subtotal_list=[]
flag_list = []

pos_system_eel.Fail(data_now)
#@ eel.expose
#def now(data):
    #global data_now
    #data_now = data

@ eel.expose
def registration(search_csv):
    order=pos_system_eel.Order(data_now)
    order.registration(1,search_csv)

@ eel.expose
def view(search_code,volume,search_csv):
    order=pos_system_eel.Order(data_now)
    order.registration(0,search_csv)
    result = order.view(search_code,volume)
    if result[0] == 1:
        code_list.append(result[1])
        name_list.append(result[2])
        price_list.append(result[3])
        volume_list.append(result[4])
        subtotal_list.append(result[5])
        flag_list.append(1)
    else:
        print("商品一覧から選択お願いします。")

@ eel.expose
def list_all(Write_flag):
    global total_price
    total_price = -1 #初期値
    order=pos_system_eel.Order(data_now)
    result1 = order.list_all(code_list,name_list,price_list,volume_list,subtotal_list,Write_flag)
    total_price = result1

#step4_POSシステム追加機能　ラジオボタンで現金値引き後合計金額再表示
@ eel.expose
def discount(flag):
    global discounted_price
    discounted_price = -1 #初期値
    order=pos_system_eel.Order(data_now)
    result2 = order.discount(flag,total_price)
    discounted_price = result2

@ eel.expose
def bill(money,select):
    check_flag = 0
    for flag in flag_list:
        if flag == 1:
            check_flag += 1

    if check_flag >= 1:
        if select == 0:
            order=pos_system_eel.Order(data_now)
            order.credit_bill(total_price)

        elif select == 1:
            if discounted_price > 0:
                order=pos_system_eel.Order(data_now)
                order.cash_bill(money,discounted_price)
            else:
                order=pos_system_eel.Order(data_now)
                order.cash_bill(money,total_price)

        elif select == 2:
            order=pos_system_eel.Order(data_now)
            order.pay_bill(total_price)

    if check_flag == 0:
        print("商品が選択されていません")
        eel.monitor4("商品が選択されていません")


# @ eel.expose
# def view1(search_code,volume):
#     eel.monitor2("AAAA")
#     pos_system_eel.view1(search_code,volume)


    
desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)