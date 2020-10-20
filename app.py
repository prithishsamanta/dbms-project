from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import datetime
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

count_item = [101]
count_table = [11]
count_chef = [11]
count_waiter = [11]
count_order = [11]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/itemtables', methods=['GET', 'POST'])
def seeitemstable():
    cur = mysql.connection.cursor()
    if(request.method == 'POST'):
        item_id = 'I'+str(count_item[0])
        count_item[0] += 1
        itemname = request.form['Itemname']
        price = request.form['price']
        itype = request.form['type']
        cur.execute('''INSERT INTO items VALUES (%s, %s, %s, %s)''', (item_id, itemname, price, itype))
        mysql.connection.commit()
        cur.close()
        return redirect('/itemtables')
    else:
        results = cur.execute('''SELECT * FROM items ORDER BY type DESC''')
        count_item[0] = results + 101
        iteminfo = cur.fetchall()
        return render_template('itemtable.html', iteminfo = iteminfo, item_id = 'I'+str(count_item[0]))

@app.route('/orderitemtables', methods=['GET', 'POST'])
def seeorderitemstable():
    show_tableinfo = ""
    cur = mysql.connection.cursor() 
    if(request.method == 'POST'):
        if(request.form['ordersub'] == "ADD THIS TO ORDER"):
            order_id = 'OI'+str(count_order[0])
            count_order[0] += 1
            table_no = request.form['table_no']
            chef_id = request.form['chef_id']
            waiter_id = request.form['waiter_id']
            cur.execute('''SELECT SUM(t_price) FROM order_item WHERE order_id = "%s"''' % order_id)
            amount = cur.fetchall()
            cur.execute('''INSERT INTO orders VALUES (%s, %s, %s, %s,  %s)''', (order_id, table_no[:3:], chef_id[:3:], waiter_id[:3:], amount[0][0]))
            mysql.connection.commit()
            cur.close()
            return redirect('/orderitemtables')
        if(request.form['ordersub'] == "ADD THIS TO ORDER_ITEMS"):
            order_id = 'OI'+str(count_order[0])
            iname = request.form['itemname']
            cur.execute('''SELECT item_id from items where itemname = "%s"''' % (iname))
            item_id = cur.fetchall()[0]
            quantity = request.form['quantity']
            cur.execute('''SELECT price FROM items WHERE itemname = "%s"''' % (iname))
            t_price = int(quantity) * int(cur.fetchall()[0][0])
            cur.execute('''INSERT INTO order_item VALUES (%s, %s, %s, %s)''', (order_id, item_id, quantity, t_price))
            mysql.connection.commit()
            cur.close()
            return redirect('/orderitemtables')
    else:
        results = cur.execute('''SELECT * FROM order_item ORDER BY order_id DESC''')
        count_item[0] = results + 101
        iteminfo = cur.fetchall()
        results = cur.execute('''SELECT itemname FROM items''')
        item_names = cur.fetchall()
        cur.execute('''SELECT * FROM tables''')
        show_tableinfo = cur.fetchall()
        cur.execute('''SELECT chef_name, chef_id FROM chef''')
        show_chefinfo = cur.fetchall()
        cur.execute('''SELECT waiter_name, waiter_id FROM waiter''')
        show_waiterinfo = cur.fetchall()
        count_order[0] = cur.execute('''SELECT * from orders''') + 11
        return render_template('orderitems.html', iteminfo = iteminfo, item_names = (item_names), order_id = 'OI'+str(count_order[0]),
        show_tableinfo = show_tableinfo, show_chefinfo = show_chefinfo, show_waiterinfo = show_waiterinfo)

@app.route('/tablestables', methods=['GET', 'POST'])
def seetablestables():
    cur = mysql.connection.cursor()
    if(request.method == 'POST'):
        table_no = 'T'+str(count_table[0])
        count_table[0] += 1
        seat_capacity = request.form['seat_capacity']
        cur.execute('''INSERT INTO tables VALUES (%s, %s)''', (table_no, seat_capacity))
        mysql.connection.commit()
        cur.close()
        return redirect('/tablestables')
    else:
        results = cur.execute('''SELECT * FROM tables''')
        count_table[0] = results + 11
        iteminfo = cur.fetchall()
        return render_template('tables.html', iteminfo = iteminfo, table_no = 'T'+str(count_table[0]))

@app.route('/cheftables', methods=['GET', 'POST'])
def seecheftables():
    cur = mysql.connection.cursor()
    if(request.method == 'POST'):
        chef_id = 'C'+str(count_chef[0])
        chef_name = request.form['chef_name']
        dob = request.form['dob']
        day = int(dob.split('-')[0])
        month = int(dob.split('-')[1])
        year = int(dob.split('-')[2])
        salary = request.form['salary']
        contact = request.form['contact']
        if (datetime.datetime.now().month >= month):
            age = datetime.datetime.now().year - day
        else:
            age = datetime.datetime.now().year - day - 1
        cur.execute('''INSERT INTO chef VALUES (%s, %s, %s, %s, %s, %s)''', (chef_id, chef_name, str(day)+'-'+str(month)+'-'+str(year), salary, contact, age))
        mysql.connection.commit()
        cur.close()
        return redirect('/cheftables')
    else:
        results = cur.execute('''SELECT * FROM chef''')
        count_chef[0] = results + 11
        iteminfo = cur.fetchall()       
        return render_template('chef.html', iteminfo = iteminfo, chef_id = 'C'+str(count_chef[0]))

@app.route('/waitertables', methods=['GET', 'POST'])
def seewaitertables():
    cur = mysql.connection.cursor()
    if(request.method == 'POST'):
        waiter_id = 'W'+str(count_waiter[0])
        waiter_name = request.form['waiter_name']
        dob = request.form['dob']
        day = int(dob.split('-')[0])
        month = int(dob.split('-')[1])
        year = int(dob.split('-')[2])
        salary = request.form['salary']
        contact = request.form['contact']
        if (datetime.datetime.now().month >= month):
            age = datetime.datetime.now().year - day
        else:
            age = datetime.datetime.now().year - day - 1
        cur.execute('''INSERT INTO waiter VALUES (%s, %s, %s, %s, %s, %s)''', (waiter_id, waiter_name, str(day)+'-'+str(month)+'-'+str(year), salary, contact, age))
        mysql.connection.commit()
        cur.close()
        return redirect('/waitertables')
    else:
        results = cur.execute('''SELECT * FROM waiter''')
        count_waiter[0] = results + 11
        iteminfo = cur.fetchall()
        return render_template('waiter.html', iteminfo = iteminfo, waiter_id = 'W'+str(count_waiter[0]))

@app.route('/orderstable')
def seeordestable():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM orders''')
    iteminfo = cur.fetchall()
    return  render_template('orders.html', iteminfo = iteminfo)

@app.route('/feedbacktables', methods=['GET', 'POST'])
def seefeedbackstables():
    cur = mysql.connection.cursor()
    if(request.method == 'POST'):
        order_id = request.form['order_id']
        cust_name = request.form['cust_name']
        dob = request.form['dob']
        day = int(dob.split('-')[0])
        month = int(dob.split('-')[1])
        year = int(dob.split('-')[2])
        rating = request.form['rating']
        review = request.form['review']
        contact = request.form['contact']
        cur.execute('''INSERT INTO customer_feedback VALUES (%s, %s, %s, %s, %s, %s)''', (order_id, cust_name,
        str(day)+'-'+str(month)+'-'+str(year), rating, review, contact))
        mysql.connection.commit()
        cur.close()
        return redirect('/feedbacktables')
    else:
        results = cur.execute('''SELECT * FROM customer_feedback''')
        iteminfo = cur.fetchall()
        cur.execute('''SELECT order_id FROM orders ORDER BY order_id''')
        show_order_id = cur.fetchall()
        return render_template('feedbacks.html', iteminfo = iteminfo, show_order_id = show_order_id)

@app.route('/cheforderstable')
def seecheforderstable():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT chef_id, order_id, itemname, quantity FROM chef, order_item, items''')
    iteminfo = cur.fetchall()
    return  render_template('orderchef.html', iteminfo = iteminfo)

if __name__ == '__main__':
    app.run(debug = True)
