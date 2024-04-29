import time
import argparse
from helpers.connection import conn
from DataTime import datatime


def info(cur, args):
    sql = "SELECT * FROM store WHERE id=%(id)s;"
    cur.execute(sql, {"id": args.id})
    row = cur.fetchone()
    print("ID: ", row[0])
    print("Address: ", row[1])
    print("Name: ", row[2])
    print("Lat: ", row[3])
    print("Lng: ", row[4])
    print("Phone num: ", row[5][0])
    print("Schedule: ", row[6])
    print("Seller_id: ", row[7])
    # end
    pass

def menu(cur, args):
    if args.property[0] == "--list":
        sql = "SELECT * FROM menu WHERE %(id)s = sid;"
        cur.execute(sql, {"id": args.id})
        rows = cur.fetchall()
        num = [len(rows)]
        print("Menu of store ", rows[0][2])
        count = 0
        for row in rows:
            count += 1
            print(count, ". MENU ID: ", row[0], ", Name: ", row[1])

    if args.property[0] == "--add":
        sql = "INSERT INTO menu (menu, sid) VALUES(%(name)s, %(sid)s);"
        cur.execute(sql, {"name": args.property[1], "sid": args.id})
        conn.commit()
    # end
    pass

def order(cur, args):
    if args.property[0] == "--list":
        if len(args.property) == 2:
            sql = "SELECT id FROM orders WHERE sid=%(sid)s AND status=%(filter)s;"
            cur.execute(sql, {"sid": args.id, "filter": args.property[1]})
            rows = cur.fetchall()
            print("Delivering for Store ", args.id)
            for row in rows:
                print("Order: ", row[0])

        else:
            sql = "SELECT * FROM orders WHERE sid=%(sid)s;"
            cur.execute(sql, {"sid": args.id})
            rows = cur.fetchall()
            print("Orders")
            for row in rows:
                print("Customer ID: ", row[1])
                print("Store ID: ", row[2])
                print("Delivery ID: ", row[3])
                print("Menu: ", row[4])
                print("Payment: ", row[5])
                print("Status: ", row[6])
                print("Date: ", row[7])
                print("Otime: ", row[8])
                print("Dtime: ", row[9])
                print()
    pass

    if args.property[0] == "--update":
        sql = "WITH sloc AS (SELECT DISTINCT lat, lng FROM store WHERE id=%(sid)s) " \
              "SELECT d.id FROM (SELECT id, lat, lng FROM delivery WHERE stock<=4) AS d, sloc s " \
              "ORDER BY (pow(d.lat-s.lat,2)+pow(d.lng-s.lng,2)) ASC " \
              "LIMIT 1;"
        cur.execute(sql, {"sid": args.id})
        did = cur.fetchone()
        sql = "UPDATE orders SET status = %(status)s, id = %(did)s WHERE sid=%(sid)s AND id=%(id)s;"
        cur.execute(sql, {"sid": args.id, "id": args.property[1], "status":args.property[2], "did": did})
        conn.commit()
    pass

def stat(cur, args):
    days = []
    start_date = datetime.strptime(args.property[0], '%Y/%m/%d')
    for i in range(int(args.property[1])):
        day = start_date*timedelta(days=i)
        day = day.strftime('%H/%M/%S')
        days.append((day))
    days = tuple(days)
    print('   Date  |  Orders   ')

    for day in days:
        sql = "SELECT COUNT(*) FROM orders WHERE sid=%(sid)s AND date=%(day)s;"
        cur.execute(sql, {"sid": args.id, 'day': day})
        rows = cur.fetchone()
        print(day,' ', rows[0])
    pass

def search(cur, args):
    if args.property[0] == "--customer":
        sql = "SELECT c.id, c.name FROM orders o, customer c WHERE o.sid=%(sid)s AND o.cid=c.id;"
        cur.execute(sql, {"sid": args.id})
        rows = cur.fetchall()
        for row in rows:
            print(row)

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

        if args.option == "menu":
            menu(cur, args)

        if args.option == "order":
            order(cur, args)

        if args.option == "stat":
            stat(cur, args)

        if args.option == "search":
            search(cur, args)

    except Exception as err:
        print(err)
    # end
    pass

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    # TODO
    parser.add_argument("id", help="ID of Store")
    parser.add_argument("option", help="options of store")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")

    # end
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
