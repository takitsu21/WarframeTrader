import sqlite3

def clean_db():
    cur = conn.cursor()
    sql = "DROP TABLE IF EXISTS settings"
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS settings (
        `id` BIGINT PRIMARY KEY,
        `delete` BOOLEAN,
        `delay` INT
    )"""
    cur.execute(sql)
    conn.commit()

def clean_prefix():
    cur = conn.cursor()
    sql = "DROP TABLE IF EXISTS guild_prefix"
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS guild_prefix (
        `id` BIGSERIAL,
        `prefix` VARCHAR(5)
    )"""
    cur.execute(sql)
    conn.commit()

def u_prefix(values):
    cur = conn.cursor()
    sql = """UPDATE guild_prefix SET id=?, prefix=?"""
    cur.execute(sql, values)
    conn.commit()

def i_prefix(values):
    cur = conn.cursor()
    sql = """INSERT INTO guild_prefix(id, prefix) VALUES(?, ?)"""
    cur.execute(sql, values)
    conn.commit()

def read_prefix(values):
    cur = conn.cursor()
    sql = """SELECT prefix FROM guild_prefix WHERE id=?"""
    cur.execute(sql, values)
    rows = cur.fetchall()
    print(rows)
    return rows

def read_settings(values):
    sql = """SELECT `delete`, delay FROM settings WHERE id=?"""
    cur = conn.cursor()
    cur.execute(sql, values)
    rows = cur.fetchall()
    return rows

def i_guild_settings(values):
    cursor = conn.cursor()
    sql = """INSERT INTO settings(id, `delete`, delay) VALUES(?, ?, ?)"""
    cursor.execute(sql, values)
    conn.commit()


def u_guild_settings(values):
    cursor = conn.cursor()
    sql = """UPDATE settings SET 
            `delete`=?,
            `delay`=?
            WHERE id=?"""
    cursor.execute(sql, values)
    conn.commit()

def d_guild(values):
    cursor = conn.cursor()
    sql = """DELETE FROM settings WHERE id=?"""
    cursor.execute(sql, values)
    conn.commit()

try:
    conn = sqlite3.connect('./db/settings.db')
    # clean_db()
    # clean_prefix()
    # u_prefix((55555555, 'a',))
    # print(read_prefix())
    # clean_db()
    # create_prefix()
    # print(read_prefix((146952202815012864,)))
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
