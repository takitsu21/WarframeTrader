# import sqlite3
import pymysql

def u_prefix(_id, prefix):
    cur = conn.cursor()
    sql = """UPDATE guild_settings SET prefix=%s WHERE id=%s"""
    cur.execute(sql, (prefix, _id,))
    conn.commit()

def i_prefix(values):
    cur = conn.cursor()
    sql = """INSERT INTO guild_settings(id, prefix) VALUES(%s, %s)"""
    cur.execute(sql, values)
    conn.commit()

def read_prefix(_id: int):
    cur = conn.cursor()
    sql = """SELECT prefix FROM guild_settings WHERE id=%s"""
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0][0]
    return rows

def read_settings(_id):
    sql = """SELECT to_delete, delay FROM guild_settings WHERE id=%s"""
    cur = conn.cursor()
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0]
    return rows[0], rows[1]

def i_guild_settings(_id: int, prefix: str, to_delete: int, delay: int):
    cursor = conn.cursor()
    sql = """INSERT INTO guild_settings(id, prefix, to_delete, delay)
    VALUES(%s, %s, %s, %s)"""
    cursor.execute(sql, (_id, prefix, to_delete, delay, ))
    conn.commit()

def read_table(*selector):
    selector = ', '.join(selector)
    sql = """SELECT %s FROM `guild_settings`"""
    cur = conn.cursor()
    cur.execute(sql, (selector,))
    conn.commit()
    rows = cur.fetchall()
    return rows

def u_guild_settings(_id: int, to_delete: int, delay: int):
    cursor = conn.cursor()
    sql = """UPDATE guild_settings SET 
            to_delete=%s,
            delay=%s
            WHERE id=%s"""
    cursor.execute(sql, (to_delete, delay, _id, ))
    conn.commit()

def d_guild(_id):
    cursor = conn.cursor()
    sql = """DELETE FROM guild_settings WHERE id=%s"""
    cursor.execute(sql, (_id,))
    print(_id, 'removed')
    conn.commit()

try:
    conn = pymysql.connect(
                    host='node03.cluster.stan-tab.fr',
                    user='dylann_wf',
                    password='nK2sgPWGx7nRQ01W',
                    db='dylann_wf'
                    )
except pymysql.Error as error:
    print("Error while connecting to sqlite", error)
