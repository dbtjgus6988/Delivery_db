import time
import argparse
from helpers.connection import conn

def info(cur, args):
    sql = "SELECT id, name, phone, local, domain FROM seller WHERE id=%(id)s;"
    cur.execute(sql, {"id": args.id})
    row = cur.fetchone()
    print("ID: ", row[0])
    print("Name: ", row[1])
    print("Phone: ", row[2])
    print("Local: ", row[3])
    print("Domain: ", row[4])
    # end
    pass

def update(cur, args):
    if args.property[0] == "id":
        raise Exception("Except id")

    else:
        sql = "UPDATE seller SET "+ args.property[0] + " = %s WHERE id=%s;"
        data = args.property[1], args.id
        cur.execute(sql, data)
        conn.commit()
    pass

def main(args):
    # TODO
    # you can edit the example code below whatever you want.
    # example code
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

    except Exception as err:
        print(err)
    # end
    pass

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    # TODO
    # you can edit the example code below whatever you want.
    # example code
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("option", help="options of seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")
    # end

    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
