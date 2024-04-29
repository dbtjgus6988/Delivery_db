import time
import argparse
from helpers.connection import conn

def status(cur, args):
    if len(args.property) == 0:
        sql = "SELECT id FROM orders WHERE did=%(id)s AND status=delivering;"
        cur.execute(sql, {"did": args.id})
        rows = cur.fetchall()
        for row in rows:
            print(row)

    if len(args.property) == 2:
        if args.property[0] == "-e":
            sql = "UPDATE orders SET status = %(done)s WHERE did=%(did)s AND id=%(id)s;"
            cur.execute(sql, {"did": args.id, "done": "delivered", "id": args.property[1]})
            conn.commit()

    else:
        if args.property[0] == "-a":
            sql = "SELECT id, status FROM orders WHERE did=%(did)s;"
            cur.execute(sql, {"did": args.id})
            rows = cur.fetchall()
            print("Delivery status | Order id")
            for row in rows:
                print(row[1], row[0])


def main(args):
    # TODO
    print(args)
    print(args.id)
    print(args.option)

    try:
        cur = conn.cursor()
        print("database is connected")
        if args.option == "status":
            status(cur, args)

    except Exception as err:
        print(err)
    pass


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    # TODO
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("option", help="options of seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")

    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
