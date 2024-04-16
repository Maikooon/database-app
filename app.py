from flask import Flask, render_template, request, g, redirect, url_for, session, flash
import uuid
import hashlib
import sqlite3
import os, datetime
from dataclasses import dataclass
from datetime import timedelta


DATABASE = "database.db"
app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = '1234'
app.debug = True


@app.before_request
def before_request():
    # リクエストのたびにセッションの寿命を更新する
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)
    session.modified = True


"""
データベース接続
"""
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


"""
ビュー
"""
@app.route('/')
def home():
   
    # セッションにuser_idがない場合、未ログインなのでusernameを渡さずにHTMLをレンダリング
    if 'user_id' not in session:
        return render_template('home.html')
    # ユーザ情報がある場合、データベースに接続しuser_idからユーザ名を検索して渡す
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute('SELECT * FROM LoginUser WHERE username = ?', (session['user_id'],)).fetchone()
    return render_template('home.html', username=user['username'])


@app.route('/report')
def report():
    # セッションにuser_idがない場合、未ログインなのでusernameを渡さずにHTMLをレンダリング
    if 'user_id' not in session:
        return render_template('report.html')
    # ユーザ情報がある場合、データベースに接続しuser_idからユーザ名を検索して渡す
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute('SELECT * FROM LoginUser WHERE username = ?', (session['user_id'],)).fetchone()
    return render_template('report.html', username=user['username'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    error = None
    # POSTはこの関数の一番下のlogin.htmlから呼ばれ、その中のフォームを送信する。フォームの内容に基づき、ユーザ情報を照合する
    if request.method == 'POST':
        # フォームの内容を取得する
        username = request.form['username']
        password = request.form['password']
        # パスワードは平文ではなくハッシュ値で照合する
        h = hashlib.md5(password.encode())
        conn = get_db()
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM LoginUser WHERE username = ? AND password = ?', (username, h.hexdigest())).fetchone()
        if user is None:
            # ユーザ認証されなかった場合、エラーメッセージをレンダリングする。メッセージはこのように引数で渡すこともできるし、else以下のようにflashを使用することもできる。
            error = 'Invalid username or password'
        else:
            # ユーザ認証された場合、セッションに記録する
            session['user_id'] = username
            # flashメッセージを設定する
            flash("Logged in")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


import hashlib  # Import the hashlib module for password hashing

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = get_db()
    cur = conn.cursor()
    request_valid = True

    if request.method == 'POST':
        # フォームの内容を取得し、バリデーションを行う。エラーがあればflashメッセージで通知する
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        birth = request.form['birth']
        pict = request.form['pict']  
        
        # ユーザー名とパスワードの文字数にそれぞれ制限を設ける
        if not username or len(username.strip()) < 3:
            flash('Username must be at least 3 characters long')
            request_valid = False
        if not password or len(password) < 3:
            flash('Password must be at least 3 characters long')
            request_valid = False
        if password != confirm:
            flash('Passwords do not match')
            request_valid = False
        if not pict:
            flash('Input image file')
            request_valid = False
        if cur.execute('SELECT * FROM LoginUser WHERE username = ?', (username,)).fetchone():
            # ユーザーがすでに存在している場合はエラーを表示する
            flash('This username is already taken')
            request_valid = False

        if request_valid:
            # 新しいユーザーを作成する
            # パスワードはハッシュ値により格納している
            h = hashlib.md5(password.encode())
            cur.execute('INSERT INTO LoginUser (username, password, birth, pict) VALUES (?, ?, ?, ?)',
                        (username, h.hexdigest(), birth, pict))
            conn.commit()
            # ログインページにリダイレクトする
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    if session.pop('user_id', None):
        flash("Logged out")
    return redirect(url_for('home'))


@app.route('/Mypage')
def mypage():
    if 'user_id' not in session:
        return redirect(url_for('login'))


    user_id = session['user_id']


    # ユーザー情報を取得
    conn = get_db()
    cur = conn.cursor()
    okini = cur.execute("SELECT * FROM Favorites").fetchall()
   
    user = cur.execute('SELECT * FROM LoginUser WHERE username = ?;', (user_id,)).fetchone()


    cur2 = conn.cursor()
    fav = cur2.execute('SELECT * FROM Favorites f JOIN drink ON drink.id = f.drink_id WHERE f.user_id = ?;', (user_id,)).fetchall()
    cur3 = conn.cursor()
    favfood = cur3.execute('SELECT * FROM Favoritesfood ff JOIN food ON food.id=ff.food_id  WHERE user_id = ?;', (user_id,)).fetchall()
    print(favfood)
    return render_template('mypage.html', user=user, fav=fav,favfood=favfood)




@app.route("/food", methods=["GET", "POST"])
def food():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
       
        elist = cur.execute("SELECT * FROM food WHERE food.foodName LIKE ? ORDER BY food.id", ('%'+request.form["foodName"]+'%', )).fetchall()
       
        return render_template("food.html", counts=len(elist), elist=elist, query_name=request.form["foodName"])
    else:
        # GETの場合全件のデータベースルックアップをする。返ってくるテーブルの属性名で属性にアクセスするので、SQLで属性名を適切に設定する
        elist = cur.execute("SELECT * FROM food").fetchall()
       
        return render_template("food.html", counts=len(elist), elist=elist)
   
   


@app.route("/food/<id>")
def food_master(id):
    #print(id)
    #print('aaa')
    #詳細情報
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM food f WHERE f.id = ?", (id,))
    emp = cur.fetchone()
    cur.close()


    cur2 = conn.cursor()
    cur2.execute("SELECT * FROM drink d  JOIN  drink_food df ON df.drink_id=d.id  WHERE  df.food_id = ?", (emp[0],))
    withdrink = cur2.fetchone()
    cur2.close()


    if not emp:
        flash(f"Error: No employee entry {id}", "error")
        return redirect(url_for("food"))
    return render_template("food_detail.html", emp=emp,withdrink = withdrink)




@app.route("/drink", methods=["GET", "POST"])
def drink():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    
    #ここから選択ボタンが押された時野処理
    if "selectedButton" in request.form:
      selected_button = request.form["selectedButton"]
       # "all" ボタンが選択された場合の処理
      if selected_button == "all":
          # print("11111")
           elist = cur.execute("SELECT * FROM drink").fetchall()
           return render_template("drink.html", counts=len(elist), elist=elist, query_name="")
        # "Coffee" ボタンが選択された場合の処理
      elif selected_button == "Coffee":
           elist = cur.execute("SELECT * FROM drink WHERE drink.TypeTempId = 'Cof1' OR drink.TypeTempId = 'Cof2' ORDER BY drink.id").fetchall()
           return render_template("drink.html", counts=len(elist), elist=elist, query_name="")
      # "Tea" ボタンが選択された場合の処理
      elif selected_button == "Tea":
           elist = cur.execute("SELECT * FROM drink WHERE drink.TypeTempId = 'Tea1'  OR drink.TypeTempId = 'Tea2' ORDER BY drink.id").fetchall()
           return render_template("drink.html", counts=len(elist), elist=elist, query_name="")
      # "Frap" ボタンが選択された場合の処理
      elif selected_button == "Frap":
          elist = cur.execute("SELECT * FROM drink WHERE drink.TypeTempId = 'Frap'  ORDER BY drink.id").fetchall()
          return render_template("drink.html", counts=len(elist), elist=elist, query_name="")
 


      #検索するとPOSTされる
    if request.method == "POST":
            # 検索ボタンが押された場合の処理
            elist = cur.execute("SELECT * FROM drink WHERE drink.drinkName LIKE ? ORDER BY drink.id", ('%' + request.form["drinkName"] + '%',)).fetchall()
            return render_template("drink.html", counts=len(elist), elist=elist, query_name=request.form["drinkName"])
    else:
        # GETの場合全件のデータベースルックアップをする。返ってくるテーブルの属性名で属性にアクセスするので、SQLで属性名を適切に設定する
        elist = cur.execute("SELECT * FROM drink").fetchall()
      #  print(elist)
        return render_template("drink.html", counts=len(elist), elist=elist)




# ドリンクのお気に入り追加
@app.route("/add_favorite", methods=['POST'])
def add_favorite():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    drink_id = request.form['drinkId']
    conn = get_db()
    cur = conn.cursor()


     # Check if not  the drink is already in favorites for the user
    cur.execute('SELECT * FROM Favorites WHERE user_id=? AND drink_id=?', (user_id, drink_id))
    existing_favorite = cur.fetchone()
    if existing_favorite:
        # Drink is already in favorites, you can handle this case accordingly
        print("This is already add to your favorite list")
        return 'Already added to favorites', 400
   
    #if not int the data in the data
    cur.execute('INSERT INTO Favorites (user_id, drink_id) VALUES (?, ?)', (user_id, drink_id))
    conn.commit()
    return 'OK', 200


@app.route("/add_favoritefood", methods=['POST'])
def add_favoritefood():
    if 'user_id' not in session:
        return redirect(url_for('login'))


    user_id = session['user_id']
    food_id = request.form['foodId']


    conn = get_db()
    cur = conn.cursor()
     # Check if not  the drink is already in favorites for the user
    cur.execute('SELECT * FROM Favoritesfood WHERE user_id=? AND food_id=?', (user_id, food_id))
    existing_favoritefood = cur.fetchone()
    if existing_favoritefood:
        # Drink is already in favorites, you can handle this case accordingly
        print("This is already add to your favorite list")
        return 'Already added to favorites', 400
   
    #if not int the data in the data
    cur.execute('INSERT INTO Favoritesfood (user_id, food_id) VALUES (?, ?)', (user_id, food_id))
    conn.commit()
    return 'OK', 200


@app.route("/drink/<id>", methods=['GET', 'POST'])
def drink_master(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
   
    if request.method == 'POST':
        user_id = session['user_id']
        drink_id = request.form['drinkId']
       
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO Favorites (user_id, drink_id) VALUES (?, ?)', (user_id, drink_id))
        conn.commit()
        return 'OK', 200
   
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drink d WHERE d.id = ?", (id,))
    emp = cur.fetchone()
    cur.close()
   
    cur2 = conn.cursor()
    cur2.execute("SELECT * FROM topping t JOIN drink_topping dt ON t.id = dt.topping_id WHERE dt.drink_id = ?", (emp[0],))
    top = cur2.fetchone()
    cur2.close()


    cur3 = conn.cursor()
    cur3.execute("SELECT * FROM food f JOIN  drink_food df ON df.food_id=f.id  WHERE  df.drink_id = ?", (emp[0],))
    match = cur3.fetchone()
    cur3.close()


    if not emp:
        flash(f"Error: No employee entry {id}", "error")
        return redirect(url_for("drink"))
   
    return render_template("drink_detail.html", emp=emp, top=top, match=match)




@app.route("/shop", methods=["GET", "POST"])
def shop():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    #
   
    if "selectedButton" in request.form:
      print("111111")
      selected_button = request.form["selectedButton"]
       # "all" ボタンが選択された場合の処理
      if selected_button == "All":
           print("11111")
           elist = cur.execute("SELECT * FROM shop").fetchall()
           return render_template("shop.html", counts=len(elist), elist=elist, query_name="")
        # "hokkaido" ボタンが選択された場合の処理
      elif selected_button == "Hokkaido":
           elist = cur.execute("SELECT * FROM shop JOIN region ON shop.region_id = region.id WHERE region.regionName = '北海道' ORDER BY shop.id").fetchall()
           return render_template("shop.html", counts=len(elist), elist=elist, query_name="")
      # "tokyo" ボタンが選択された場合の処理
      elif selected_button == "Tokyo":
           elist = cur.execute("SELECT * FROM shop JOIN region ON shop.region_id = region.id WHERE region.regionName = '東京' ORDER BY shop.id").fetchall()
           return render_template("shop.html", counts=len(elist), elist=elist, query_name="")
      # "aichi" ボタンが選択された場合の処理
      elif selected_button == "Aichi":
          elist = cur.execute("SELECT * FROM shop JOIN region ON shop.region_id = region.id WHERE region.regionName = '愛知' ORDER BY shop.id").fetchall()
          return render_template("shop.html", counts=len(elist), elist=elist, query_name="")
      # "KYOTO" ボタンが選択された場合の処理
      elif selected_button == "Kyoto":
          elist = cur.execute("SELECT * FROM shop JOIN region ON shop.region_id = region.id WHERE region.regionName = '京都' ORDER BY shop.id").fetchall()
          return render_template("shop.html", counts=len(elist), elist=elist, query_name="")
     
    #
    if request.method == "POST":
        elist = cur.execute("SELECT * FROM shop  WHERE shop.shopName LIKE ? ORDER BY shop.id", ('%'+request.form["shopName"]+'%', )).fetchall()
        return render_template("shop.html", counts=len(elist), elist=elist, query_name=request.form["shopName"])
    else:
        # GETの場合全件のデータベースルックアップをする。返ってくるテーブルの属性名で属性にアクセスするので、SQLで属性名を適切に設定する
        elist = cur.execute("SELECT * FROM shop").fetchall()    
        return render_template("shop.html", counts=len(elist), elist=elist)
   
   
@app.route("/shop/<id>")
def shop_master(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  shop s  WHERE s.id = ?;", (id,))
    emp = cur.fetchone()
    cur.close()
    print(emp[2])
   
    cur2 =  conn.cursor()
    cur2.execute("SELECT *  FROM region r WHERE r.id = ?;",(emp[2],))
    regions = cur2.fetchone()
    cur.close()


    cur3 =  conn.cursor()
    cur3.execute("SELECT *  FROM ShopType st WHERE st.id = ?;",(emp[3],))
    types = cur3.fetchone()
    print(types)


    cur4 =  conn.cursor()
    drinklist = cur4.execute("SELECT * FROM drink  JOIN shop_drink sd ON sd.drink_id = drink.id WHERE sd.shop_id =?;", (emp[0],) ).fetchall()
    #該当するものが二次元配列として出てきた
    cur4.close()


    cur5 =  conn.cursor()
    foodlist = cur5.execute("SELECT * FROM food  JOIN shop_food sf ON sf.food_id = food.id WHERE sf.shop_id =?;", (emp[0],) ).fetchall()
    #該当するものが二次元配列として出てきた
    cur5.close()
   
    if not emp:
        flash(f"Error: No employee entry {id}", "error")
        return redirect(url_for("shop"))
    return render_template("shop_detail.html", emp=emp,regions = regions,types =types,counts = len(drinklist), drinklist =  drinklist,foodlist = foodlist)


@app.route("/edit_user", methods=["GET", "POST"])
def edit_user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db()
    cur = conn.cursor()
    emp = cur.execute('SELECT * FROM LoginUser WHERE username = ?', (user_id,)).fetchone()
    
    if not emp:
        flash(f"Invalid id {user_id}", "error")
        return redirect(url_for("mypage"))

    if request.method == "GET":
        return render_template('edit_user.html', emp=emp)

    if request.method == "POST":
        request_valid = True
        return_data = {"emp": {**emp, **request.form}}
        
            
        # ファイルを確認
        file = request.files["pict"] if 'pict' in request.files else None
        if not file:
            filename = emp["pict"]
        elif not file.filename.endswith(('jpg', 'jpeg', 'png')):
            request_valid = False
            return_data["pict_invalid"] = "画像の拡張子が不正です。"
        elif request_valid:
            filename = str(user_id) + os.path.splitext(file.filename)[1]
            file.save(os.path.join('./static/pict', filename))
         # 更新を行う
        if request_valid:
            try:
                cur.execute('UPDATE LoginUser SET birth=?, pict=? WHERE username=?',
                            (request.form['birth'], filename, user_id))
            except sqlite3.Error as e:
                print('sqlite3.Error occurred:', e.args[0])
                request_valid = False
                return_data['db_error'] = True
            conn.commit()  # 更新はcommitが必要

        if request_valid:
            flash(f"Updated {emp['username']} (ID: {user_id})")
            return redirect(url_for("mypage"))
        else:
            return render_template("edit_user.html", user_id=user_id, **return_data)


@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()
    user_id = session['user_id']
    emp = cur.execute('SELECT username FROM LoginUser L WHERE L.username = ?', (user_id,)).fetchone()

    if request.method == "GET":
        return render_template('delete_user.html', emp=emp)  # Render the confirmation template

    if request.method == "POST":
        confirm = request.form.get('confirm')  # Check if the user confirmed the deletion
        if confirm == 'yes':
            try:
                cur.execute('DELETE FROM LoginUser WHERE username = ?', (user_id,))
                conn.commit()
                flash(f"Deleted {emp['username']} (ID: {user_id})")
                session.pop('user_id', None)  # Remove user_id from the session
                return redirect(url_for("login"))
            except sqlite3.Error as e:
                print('sqlite3.Error occurred:', e.args[0])
                return redirect(url_for("mypage", user_id=user_id))
        else:
            flash('Deletion canceled')  # Display a message if deletion is canceled
            return redirect(url_for("mypage", user_id=user_id))




        # pythonを直接実行したときでもflask run --debugと同じ挙動となるようにする
if __name__ == '__main__':
    app.run(debug=True)





