import pandas as pd
import datetime
import eel

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price
###レシートファイル（テキスト）出力
class Fail:
    def __init__(self,data_now):
        self.data_now = data_now
        #now = datetime.datetime.now()
        #self.failname = now.strftime('%Y%m%d_%H%M%S') 

    def file_write(self,str):
        #with openにすれば自動でファイルが閉じる　　引数　、mode='w'書き込み用、encoding = utf-8-sig：デフォルト状態
        #mode='a'追記
        with open("receipt_fail_{}.txt".format(self.data_now),mode='a',encoding = "utf-8-sig") as log_file:
            log_file.write(str+"\n")
            #print(str)

### オーダークラス
class Order:
    #def __init__(self,item_master):
    def __init__(self,data_now):
        self.file_seve = Fail(data_now)
        self.item_master = []
        self.all_note =  ""
        self.total_price = 0
        self.data_now = data_now
    
    def registration(self,prit_flag,search_csv):
        index = 0
        df = pd.read_csv("./{}.csv".format(search_csv),header=None,encoding = "utf-8-sig")  #CSV読み込み
        for num,name,price in zip(df[0],df[1],df[2]):
            if index == 0:
                index += 1
                continue
            self.item_master.append(Item(num,name,price))
            if prit_flag == 1:
                if index == 1:
                    print("■メニュー■")
                print("商品コード:{},商品名:{:　>5},価格:{}".format(num,name,price))
                eel.monitor1("商品コード:{},商品名:{:　>5},価格:{}".format(num,name,price))
            index += 1

    #課題2_オーダーをコンソール（ターミナル）から登録  
    def orders(self):
        count = 0
        while True:
            accept = int(input("購入したい商品コードを入力してください。終了したい場合は 0 を入力    "))
            if accept == 0:
                if count == 0:
                    print("またのご利用をお待ちしております。")
                    break
                else:
                    print("■ご購入品リスト■")
                    self.all("",1,0)
                    break
            else:
                count += 1
                accept_zero = str(accept).zfill(3)
                self.view(search_code,volume)

    #step4_POSシステム追加機能　ラジオボタンで現金値引き後合計金額再表示
    def discount(self,flag,total_price):
        #5%OFF
        discounted_price = int(total_price)*0.95
        print("現金値引き　5%OFF\n割引後　合計{}円".format(round(discounted_price)))
        eel.monitor3("現金値引き　5%OFF\n割引後{}円".format(round(discounted_price)))
        if flag == 1:
            self.file_seve.file_write("現金値引き　5%OFF\n割引後{}円".format(round(discounted_price)))
        return discounted_price

    #クレジット支払い　お預かり金額、お釣り
    def credit_bill(self,total_price):
            print("クレジット支払い\n{}円です。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(total_price))
            eel.monitor4("クレジット支払い\n{}円です。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(total_price))
            self.file_seve.file_write("クレジット支払い\n{}円\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(total_price))

    #現金支払い　お預かり金額、お釣り
    def cash_bill(self,money,total_price):
        change = int(money) - int(total_price)
        if change < 0:
            print("お支払い金額が不足しています。\n再度、お支払い金額を入力してください。")
            eel.monitor4("お支払い金額が不足しています。\n再度、お支払い金額を入力してください。")
        #if change == 0:
        #    print("{}円ちょうど頂きます。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(money))
        #    eel.monitor4("{}円ちょうど頂きます。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(money)
        else:
            print("現金支払い\n{}円お預かりいたします。".format(money))
            print("お釣りは{}円です。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(change))
            eel.monitor4("現金支払い\n{}円お預かりいたします。".format(money))
            eel.monitor4("お釣りは{}円です。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(change))
            self.file_seve.file_write("現金支払い\n{}円\nお釣り {}円\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(money,change))
        #self.file_seve.file_write("お支払い金額：{}円".format(deposit_money))
        #self.file_seve.file_write("お釣り：{}円\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(change))

    #楽天pay支払い　お預かり金額、お釣り
    def pay_bill(self,total_price):
            print("楽天pay支払い\n{}円です。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(total_price))
            eel.monitor4("楽天pay支払い\n{}円です。\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(total_price))
            self.file_seve.file_write("楽天pay支払い\n{}円\n\nご購入ありがとうございました。\nまたのご利用をお待ちしております。".format(total_price))

    #オーダーした商品の商品名、小計価格、合計金額を表示
    def list_all(self,code_list,name_list,price_list,volume_list,subtotal_list,Write_flag):
        #df= pd.DataFrame(index=[num,code_list,name_list,price_list,volume_list,subtotal_list])        
        #df= pd.DataFrame([[menu.item_code,menu.item_name,menu.price,volume,subtotal]],index=[num],columns=['商品コード','商品名','単価','個数','小計'])
        if Write_flag == 1:
            df= pd.DataFrame({'商品コード':code_list,'商品名':name_list,'単価':price_list,'個数':volume_list,'小計':subtotal_list})
            df.to_csv("購入リスト_{}.csv".format(self.data_now),mode='a',encoding="utf_8-sig")
            print("購入商品一覧")
        total_price = 0
        for code,name,price,volume,subtotal in zip(code_list,name_list,price_list,volume_list,subtotal_list):
            total_price += subtotal
            eel.monitor2("商品コード:{},商品名:{:　>5},単価:{},個数:{},小計{}円".format(code,name,price,volume,subtotal))
            if Write_flag == 1:
                print("商品コード:{},商品名:{:　>5},単価:{},個数:{},小計{}円".format(code,name,price,volume,subtotal))
        print("合計{}円".format(total_price))
        eel.monitor3("{}円".format(total_price))
        return total_price

    #オーダー登録した商品名、価格を表示    
    def view(self,search_code,volume):
        item_code = str(search_code).zfill(3)
        flag = 0
        for menu in self.item_master:
            if item_code == menu.item_code:
                subtotal = int(volume) * int(menu.price)
                #format {:　>3}はスペース、右埋め　>、文字数 3
                print("商品コード:{},商品名:{:　>5},単価:{},個数:{},小計{}円".format(menu.item_code,menu.item_name,menu.price,volume,subtotal))
                eel.monitor2("商品コード:{},商品名:{:　>5},単価:{},個数:{},小計{}円".format(menu.item_code,menu.item_name,menu.price,volume,subtotal))
                self.file_seve.file_write("商品コード:{},商品名:{:　>5},単価:{},個数:{},小計{}円".format(menu.item_code,menu.item_name,menu.price,volume,subtotal))
                flag = 1
                return flag,menu.item_code,menu.item_name,menu.price,volume,subtotal
        if flag == 0:
            print("申し訳ございません商品がありません、、、（涙）") 
            eel.monitor2("申し訳ございません商品がありません、、、（涙）")
            return "none"

### メイン処理
def main():
    # オーダー登録
    order=Order()
    order.registration()
    order.orders() 


if __name__ == "__main__":
    main()