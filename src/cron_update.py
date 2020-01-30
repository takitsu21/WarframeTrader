import datetime
import requests
import pymysql
from decouple import config


def _to_string_time(expiry) -> list:
    f = "%Y-%m-%dT%H:%M:%S.%fZ"
    de = datetime.datetime.strptime(expiry, f)
    da = datetime.datetime.now()
    delta = de - da
    days, seconds = delta.days, delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return days, hours, minutes, seconds

def ws_offi():
    uri = "http://content.warframe.com/dynamic/worldState.php"
    r = requests.get(uri)
    if r.status_code == 200:
        return r.json()

def sentient_node(code: int) -> str:
    nodes = {
        505: 'Ruse War Field',
        510: 'Gian point',
        550: 'Nsu Grid',
        551: 'Ganalen\'s Grave',
        552: 'Rya',
        553: 'Flexa',
        554: 'H-2 Cloud',
        555: 'R-9 Cloud'
    }
    return nodes[code]

def bd_sentient():
    conn.ping(reconnect=True)
    sql = """SELECT next_activation FROM sentient"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    rows = cur.fetchall()
    cur.close()
    return rows

def update_sentient_activation():
    now = datetime.datetime.now()
    delta = bd_sentient()[0][0] - now
    if (delta.seconds) <= 0:
        conn.ping(reconnect=True)
        cur = conn.cursor()
        
        next_activation = now + datetime.timedelta(hours=2, minutes=45)
        expiry = now + datetime.timedelta(minutes=30)
        
        Tmp = ws_offi()['Tmp']
        try:
            Tmp = int(Tmp[7:10])
            sql = """UPDATE sentient SET
                activation=%s,
                expiry=%s,
                next_activation=%s,
                node=%s"""
            cur.execute(sql, (now, expiry, next_activation, sentient_node(Tmp),))
        except:
            
            sql = """UPDATE sentient SET
                    node=%s"""
            cur.execute(sql, (None,))
        conn.commit()
        cur.close()
    

def main():
    update_sentient_activation()
    # now = datetime.datetime.now()
    # delta = bd_sentient()[0][0] - now
    # print(delta.seconds)
    # print(bd_sentient()[0][0] - now)
        # tracker_ids = read_table()
        
        # for t_id in tracker_ids:
        #     update_tracker(t_id, 'sentient', sentient_node(Tmp))
        #     update_tracker(t_id, 'sentient', sentient_node(Tmp))


if __name__ == "__main__":
    try:
        conn = pymysql.connect(
                        host=config('db_host'),
                        user=config('user'),
                        password=config('password'),
                        db=config('db')
                    )
        main()
    except pymysql.Error as error:
        print(f"{type(error).__name__} : {error}")
    conn.close()