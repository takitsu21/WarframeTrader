import pymysql
from decouple import config
import logging
import uuid
import datetime
import time    

logger = logging.getLogger('warframe')

def create_lobby(_id, lobbyname, player1, tagplayer1, date, expiry):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """INSERT INTO lobby(id, lobbyname, lobbykey, player1, tagplayer1, date, expiry) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (_id, lobbyname, str(uuid.uuid4()), player1, tagplayer1, date, expiry,))
    conn.commit()
    cur.close()

def u_prefix(_id, prefix):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """UPDATE guild_settings SET prefix=%s WHERE id=%s"""
    cur.execute(sql, (prefix, _id,))
    conn.commit()
    cur.close()
    
def i_prefix(values):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """INSERT INTO guild_settings(id, prefix) VALUES(%s, %s)"""
    cur.execute(sql, values)
    conn.commit()
    cur.close()

def read_prefix(_id: int):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """SELECT prefix FROM guild_settings WHERE id=%s"""
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0][0]
    cur.close()
    return rows

def read_settings(_id):
    conn.ping(reconnect=True)
    sql = """SELECT to_delete, delay FROM guild_settings WHERE id=%s"""
    cur = conn.cursor()
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0]
    cur.close()
    return rows[0], rows[1]

def i_guild_settings(_id: int, prefix: str, to_delete: int, delay: int):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """INSERT INTO guild_settings(id, prefix, to_delete, delay)
    VALUES(%s, %s, %s, %s)"""
    cur.execute(sql, (_id, prefix, to_delete, delay, ))
    conn.commit()
    cur.close()

def read_table(*selector):
    conn.ping(reconnect=True)
    selector = ', '.join(selector)
    sql = """SELECT %s FROM `guild_settings`"""
    cur = conn.cursor()
    cur.execute(sql, (selector,))
    conn.commit()
    rows = cur.fetchall()
    cur.close()
    return rows

def u_guild_settings(_id: int, to_delete: int, delay: int):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """UPDATE guild_settings SET 
            to_delete=%s,
            delay=%s
            WHERE id=%s"""
    cur.execute(sql, (to_delete, delay, _id, ))
    conn.commit()
    cur.close()

def d_guild(_id):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """DELETE FROM guild_settings WHERE id=%s"""
    cur.execute(sql, (_id,))
    logger.info(_id, 'removed')
    conn.commit()
    cur.close()

try:
    conn = pymysql.connect(
                    host=config('db_host'),
                    user=config('user'),
                    password=config('password'),
                    db=config('db')
                    )
    # n = datetime.datetime.now()
    # expiry = n + datetime.timedelta(hours=1)
    # create_lobby(111119456, "test", "ash", "azeqs#3131", time.strftime('%Y-%m-%d %H:%M:%S'), expiry.strftime('%Y-%m-%d %H:%M:%S'))
except pymysql.Error as error:
    logger.error(error, exc_info=True)
    logger.info('Connection closed')

