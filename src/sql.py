import pymysql
from decouple import config
import logging
import uuid
import datetime
import time

logger = logging.getLogger('warframe')

def all_lobbys():
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """SELECT * FROM lobby"""
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return rows

def insert_player_lobby(lobbykey, player_frame, player_tag):
    lobbys = get_lobby(lobbykey)[0]
    pos = 2
    for to_add in lobbys[5:8]:
        if to_add is None:
            player = "player" + str(pos)
            tag = "tagplayer" + str(pos)
            break
        pos += 1
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = "UPDATE lobby SET {}=%s, {}=%s WHERE lobbykey=%s".format(player, tag)
    cur.execute(sql, (player_frame, player_tag, lobbykey, ))
    conn.commit()
    cur.close()

def get_lobby(lobbykey):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """SELECT * FROM lobby WHERE lobbykey=%s"""
    cur.execute(sql, (lobbykey, ))
    rows = cur.fetchall()
    cur.close()
    return rows

def create_lobby(_id, lobbyname, mode,  player1, tagplayer1, date, expiry):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """INSERT INTO lobby(id, lobbyname, mode, lobbykey, player1, tagplayer1, activation, expiry) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (_id, lobbyname, mode, str(uuid.uuid4()), player1, tagplayer1, date, expiry,))
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

def read_user_lang(_id):
    conn.ping(reconnect=True)
    sql = """SELECT lang FROM users WHERE id=%s"""
    cur = conn.cursor()
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0]
    cur.close()
    return rows[0]

def insert_user_lang(_id, lang):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """INSERT INTO users(id, lang)
    VALUES(%s, %s)"""
    cur.execute(sql, (_id, lang,))
    conn.commit()
    cur.close()

def update_lang_user(_id, lang):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """UPDATE users SET lang=%s WHERE id=%s"""
    cur.execute(sql, (lang, _id,))
    conn.commit()
    cur.close()

def update_lang_server(_id, lang):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """UPDATE guild_settings SET lang=%s WHERE id=%s"""
    cur.execute(sql, (lang, _id,))
    conn.commit()
    cur.close()

def read_settings(_id):
    conn.ping(reconnect=True)
    sql = """SELECT to_delete, delay, lang FROM guild_settings WHERE id=%s"""
    cur = conn.cursor()
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0]
    cur.close()
    return rows[0], rows[1], rows[2]

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

def update_tracker(_id, channel_id, tracker, response_text):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """UPDATE tracker SET
            id=%s,
            channel=%s
            %s=%s"""
    cur.execute(sql, (_id, channel_id, tracker, response_text, ))
    conn.commit()
    cur.close()

def insert_tracker(_id, channel_id, tracker, response_text):
    conn.ping(reconnect=True)
    cur = conn.cursor()
    sql = """INSERT INTO tracker(id, channel, %s)
    VALUES(%s, %s, %s)"""
    cur.execute(sql, (tracker, _id, channel_id, response_text, ))
    conn.commit()
    cur.close()

try:
    conn = pymysql.connect(
                    host=config('db_host'),
                    user=config('user'),
                    password=config('password'),
                    db=config('db')
                    )
except pymysql.Error as error:
    logger.error(error, exc_info=True)
    logger.info('Connection closed')

