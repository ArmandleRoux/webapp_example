def query_db(db, query, args=(), one=False):
    cur = db.execute(query, args)
    result = cur.fetchall()
    cur.close()
    db.commit()
    return (result[0] if result else None) if one else result