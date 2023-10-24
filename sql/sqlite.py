import sqlite3 as sq
import random




list_random_article = list(range(10000000, 99999999))
random_article = random.randint(10000000, len(list_random_article) - 1)

db = sq.connect('Mak_Gripe_bot\\sql\\database.db')
cur = db.cursor()



async def db_start() -> None:
    cur.execute(
        'CREATE TABLE IF NOT EXISTS applications(user_id TEXT PRIMARY KEY, '
        'time TEXT, '
        'type_product TEXT, '
        'article TEXT, '
        'username TEXT, '
        'message TEXT, '
        'remaining_sets TEXT)'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS tires(article TEXT PRIMARY KEY, '
        'photo TEXT, '
        'manufacturer TEXT, '
        'model TEXT, '
        'width TEXT, '
        'height TEXT, '
        'diameter TEXT, '
        'load TEXT, '
        'speed TEXT, '
        'season TEXT, '
        'remainder_tread TEXT, '
        'price TEXT, '
        'number_of_sets TEXT, '
        'msg_chanel_id TEXT)'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS wheels(article TEXT PRIMARY KEY, '
        'photo TEXT, '
        'manufacturer TEXT, '
        'model TEXT, '
        'rim_width TEXT, '
        'diameter TEXT, '
        'departure TEXT, '
        'number_of_holes TEXT, '
        'diameter_hole TEXT, '
        'central_hole TEXT, '
        'price TEXT, '
        'number_of_sets TEXT, '
        'msg_chanel_id TEXT)'
    )
    db.commit()



async def create_application(user_id) -> None:
    cur.execute(
        'REPLACE INTO applications VALUES(?, ?, ?, ?, ?, ?, ?)',
        (user_id, '', '', '', '', '', '')
    )
    db.commit()


async def edit_application(state, user_id) -> None:
    async with state.proxy() as data_application:
        cur.execute(
            'UPDATE applications SET time = "{}", '
            'type_product = "{}", '
            'article = "{}", '
            'username = "{}", '
            'message = "{}" '
            'WHERE user_id == "{}"'.format(data_application['time'],
                                           data_application['type_product'],
                                           data_application['article'],
                                           data_application['username'],
                                           data_application['message'],
                                           user_id)
        )
        db.commit()



async def create_tires(random_article) -> None:
    tire = cur.execute(
        'SELECT 1 FROM tires WHERE article == "{random_article}"'.format(
            random_article=random_article
        )
    ).fetchone()
    if not tire:
        cur.execute(
            'INSERT INTO tires VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (random_article, '', '', '', '', '', '', '', '', '', '', '', '', '')
        )
        db.commit()


async def edit_tires(state, random_article) -> None:
    async with state.proxy() as data_tires:
        cur.execute(
            'UPDATE tires SET photo = "{}", '
            'manufacturer = "{}", '
            'model = "{}", '
            'width = "{}", '
            'height = "{}", '
            'diameter = "{}", '
            'load = "{}", '
            'speed = "{}", '
            'season = "{}", '
            'remainder_tread = "{}", '
            'price = "{}", '
            'number_of_sets = "{}" '
            'WHERE article == "{}"'.format(data_tires['photo'],
                                           data_tires['manufacturer'],
                                           data_tires['model'],
                                           data_tires['width'],
                                           data_tires['height'],
                                           data_tires['diameter'],
                                           data_tires['load'],
                                           data_tires['speed'],
                                           data_tires['season'],
                                           data_tires['remainder_tread'],
                                           data_tires['price'],
                                           data_tires['number_of_sets'],
                                           random_article)
        )
        db.commit()




async def create_wheels(random_article) -> None:
    wheel = cur.execute(
        'SELECT 1 FROM wheels WHERE article == "{random_article}"'.format(
            random_article=random_article
        )
    ).fetchone()
    if not wheel:
        cur.execute(
            'INSERT INTO wheels VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (random_article, '', '', '', '', '', '', '', '', '', '', '', '')
        )
        db.commit()


async def edit_wheels(state, random_article) -> None:
    async with state.proxy() as data_wheels:
        cur.execute(
            'UPDATE wheels SET photo = "{}", '
            'manufacturer = "{}", '
            'model = "{}", '
            'rim_width = "{}", '
            'diameter = "{}", '
            'departure = "{}", '
            'number_of_holes = "{}", '
            'diameter_hole = "{}", '
            'central_hole = "{}", '
            'price = "{}", '
            'number_of_sets = "{}" '
            'WHERE article == "{}"'.format(data_wheels['photo'],
                                           data_wheels['manufacturer'],
                                           data_wheels['model'],
                                           data_wheels['rim_width'],
                                           data_wheels['diameter'],
                                           data_wheels['departure'],
                                           data_wheels['number_of_holes'],
                                           data_wheels['diameter_hole'],
                                           data_wheels['central_hole'],
                                           data_wheels['price'],
                                           data_wheels['number_of_sets'],
                                           random_article)
        )
        db.commit()
