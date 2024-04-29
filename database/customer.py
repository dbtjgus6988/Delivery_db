import time
import argparse
from helpers.connection import conn
import json
from DataTime import datatime

def info(cur, args):
    if len(args.property) == 1:
        sql = "SELECT address FROM customer WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id})
        rows = cur.fetchall()
        print("Address of Customer ", args.id)
        count = 0
        for row in rows:
            count+=1
            print(count, ". ", row[0])


    else:
        sql = "SELECT * FROM customer WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id})
        row = cur.fetchone()
        print("Info of Customer ", args.id)
        print("ID: ", row[0])
        print("name: ", row[1])
        print("phone: ", row[2])
        print("local: ", row[3])
        print("domain: ", row[4])
        print("passwd: ", row[5])
        print("payment: ", row[6])
        print("lat/lng: ", row[7],"/",row[8])
    pass

def update(cur, args):
    if args.property[1] == "-c" or args.property[1] == "--create":
        sql = "SELECT address FROM customer WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id})
        adds = cur.fetchone() #list 안에 tuple
        #print(adds)
        adds = adds[0]
        if adds is None:
            adds = [args.property[2]]
        else:
            adds.append(args.property[2])
        sql = "UPDATE customer SET address = %(create)s WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id, "create": adds})
        conn.commit()

    if args.property[1] == "-e" or args.property[1] == "--edit":
        sql = "SELECT address FROM customer WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id})
        adds = cur.fetchone() #tuple 안에 list
        adds = adds[0]
        if adds is None:
            raise Exception("No address to edit")
        else:
            adds[int(args.property[2])-1] = args.property[3]
            sql = "UPDATE customer SET address = %(adds)s WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id, "adds": adds})
            conn.commit()

    if args.property[1] == "-r" or args.property[1] == "--remove":
        sql = "SELECT address FROM customer WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id})
        adds = cur.fetchone() #tuple 안에 list
        adds = adds[0]
        if adds is None:
            raise Exception("No address to remove")
        else:
            bye = int(args.property[2]) #1
            adds = adds.remove(adds[bye-1])
            sql = "UPDATE customer SET address = %(adds)s WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id, "adds": adds})
            conn.commit()
    pass

def pay(cur, args):
    if len(args.property) == 0:
        sql = "SELECT payments FROM customer WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.id})
        rows = cur.fetchone()
        count = 0
        row = rows[0]
        num = len(row)
        print("Index | Customer ID | Payment")
        for i in range(num):
            count += 1
            print(count, args.id, row[i])

    if len(args.property) == 3:
        if 20 > len(args.property[2]) > 0:
            sql = "SELECT payments FROM customer WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})
            adds = cur.fetchone() #tuple 안에 list안에 dictionary
            json_acc = {
                "data": {
                    "bid": args.property[1],
                    "acc_num": args.property[2]},
                "type": "account"
            }
            adds = adds[0]
            if adds is None:
                adds = [json_acc]
                adds = json.dumps(adds)
                sql = "UPDATE customer SET payments = %(adds)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "adds": adds})
                conn.commit()
            else:
                adds.append(json_acc)
                adds = json.dumps(adds)
                sql = "UPDATE customer SET payments = %(add)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "add": adds})
                conn.commit()

    else:
        if args.property[0] == "--add-card":
            if 17 > len(args.property[1]) > 13:
                sql = "SELECT payments FROM customer WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                adds = cur.fetchone() #tuple 안에 list안에 dictionary
                json_card = {
                    "data": {
                        "card_num": int(args.property[1])},
                    "type": "card"
                }
                adds = adds[0] #[{}]
                if adds is None:
                    adds = [json_card]
                    adds = json.dumps(adds)
                    sql = "UPDATE customer SET payments = %(adds)s WHERE id=%(id)s;"
                    cur.execute(sql, {"id": args.id, "adds": adds})
                    conn.commit()
                else:
                    adds.append(json_card)
                    adds = json.dumps(adds)
                    sql = "UPDATE customer SET payments = %(add)s WHERE id=%(id)s;"
                    cur.execute(sql, {"id": args.id, "add": adds})
                    conn.commit()

        if args.property[0] == "-r" or args.property[0] == "--remove":
            sql = "SELECT payments FROM customer WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})
            adds = cur.fetchone()
            adds = adds[0] #[{}]
            if adds is None:
                raise Exception("No payment to remove")
            else:
                adds.remove(adds[int(args.property[1])-1])
                adds = json.dumps(adds)
                sql = "UPDATE customer SET payments = %(adds)s WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id, "adds": adds})
                conn.commit()

def select(cur, args):
    sql = "SELECT menu FROM menu WHERE sid=%(sid)s"
    cur.execute(sql, {"sid": args.property[0]})
    rows = cur.fetchall()
    count = 0
    print("MENU of Store", args.property[0])
    for row in rows:
        count += 1
        print(count, row[0])
    sql = "UPDATE customer SET jjim = %(sid)s WHERE id=%(id)s;"
    cur.execute(sql, {"id": args.id, "sid": args.property[0]})
    conn.commit()

def cart(cur, args):
    if len(args.property) == 0:
        sql = "SELECT sid, menu FROM menu WHERE sid::TEXT IN (SELECT jjim FROM customer WHERE id=%(id)s);"
        cur.execute(sql, {"id": args.id})
        rows = cur.fetchall()
        print("Menus of Store", rows[0][0])
        count = 0
        for row in rows:
            count += 1
            print(count, ". ", row[1])

    else:
        #if args.property[0] == "-c":

        if args.property[0] == "-l":
            sql = "SELECT cart FROM customer WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                print(row)

        if args.property[0] == "-r":
            json_bin = {
            }
            bin = json.dumps(json_bin)
            b = []
            dump = b.append(bin)
            sql = "UPDATE customer SET cart = %(dump)s WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id, "dump": dump})
            conn.commit()

        if args.property[0] == "-p":
            sql = "SELECT jjim, cart, payments FROM customer WHERE id=%(id)s"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            row = rows[0]
            pay = row[2]
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            sql = "INSERT INTO orders (id, cid, sid, menu, payment, status, date, order_time) VALUES (COUNT(*)+1, %(id)s, " \
                  "%(sid)s, %(menu)s, %(payment)s, %(order)s, %(date)s, %(order_time)s;"
            cur.execute(sql, {"id": args.id, "sid": row[0], "menu": row[1], "payment": pay[0], "order": "order", "date": date,
                              "order_time": time})
            conn.commit()

def main(args):
    # TODO

    print(args)
    print(args.id)
    print(args.option)

    try:
        cur = conn.cursor()
        print("database is connected")
        if args.option == "info":
            info(cur, args)

        if args.option == "update":
            update(cur, args)

        if args.option == "pay":
            pay(cur, args)

        if args.option == "select":
            select(cur, args)

        if args.option == "cart":
            cart(cur, args)

    except Exception as err:
        print(err)

    pass


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    # TODO
    parser.add_argument("id", help="ID of Store")
    parser.add_argument("option", help="options of store")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")

    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
