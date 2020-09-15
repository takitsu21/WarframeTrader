import logging


logger = logging.getLogger('warframe')

class Pool:
    async def u_prefix(self, _id, prefix):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute("UPDATE guild_settings SET prefix=%s WHERE id=%s", (prefix, _id, ))
                await conn.commit()
                await cur.close()


    async def i_prefix(self, values):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute("INSERT INTO guild_settings(id, prefix) VALUES(%s, %s)", (values, ))
                await conn.commit()
                await cur.close()


    async def read_prefix(self, _id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT prefix FROM guild_settings WHERE id=%s", (_id, ))
                r, = await cur.fetchone()
                await cur.close()
                return r

    async def read_user_lang(self, _id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT lang FROM users WHERE id=%s", (_id, ))
                r, = await cur.fetchone()
                await cur.close()
                return r

    async def insert_user_lang(self, _id, lang):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute("INSERT INTO users(id, lang) VALUES(%s, %s)", (_id, lang, ))
                await conn.commit()
                await cur.close()


    async def update_lang_server(self, _id, lang):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute("UPDATE guild_settings SET lang=%s WHERE id=%s", (lang, _id, ))
                await conn.commit()
                await cur.close()

    async def read_settings(self, _id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT to_delete, delay, lang FROM guild_settings WHERE id=%s", (_id, ))
                to_delete, delay, lang = await cur.fetchone()
                await cur.close()
                return to_delete, delay, lang

    async def i_guild_settings(self, _id: int, prefix: str, to_delete: int, delay: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO guild_settings(id, prefix, to_delete, delay) VALUES(%s, %s, %s, %s)", (_id, prefix, to_delete, delay, ))
                await conn.commit()
                await cur.close()

    async def u_guild_settings(self, _id: int, to_delete: int, delay: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = """UPDATE guild_settings SET
                        to_delete=%s,
                        delay=%s
                        WHERE id=%s"""
                await cur.execute(sql, (to_delete, delay, _id, ))
                await conn.commit()
                await cur.close()

    async def d_guild(self, _id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM guild_settings WHERE id=%s", (_id, ))
                await conn.commit()
                await cur.close()


