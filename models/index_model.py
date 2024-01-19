import pandas
import sqlite3

def get_case(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM "case"
    ''', conn)

def get_suspect(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM "suspect_witness"
    WHERE sus_wit_type = "suspect"
    ''', conn)

def get_witness(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM "suspect_witness"
    WHERE sus_wit_type = "witness"
    ''', conn)

def get_evidance(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM "evidance"
    ''', conn)

def get_selected_suspect(conn: sqlite3.Connection, suspects_id):
    MY_SQL = '''
            SELECT *
            FROM "suspect_witness"
            WHERE sus_wit_id IN ({0})
            '''\
            .format(', '.join(['?' for _ in suspects_id]))

    return pandas.read_sql(MY_SQL, conn, params=suspects_id)


def get_selected_witness(conn: sqlite3.Connection, witnesses_id):
    MY_SQL = '''
            SELECT *
            FROM "suspect_witness"
            WHERE sus_wit_id IN ({0})
            '''\
            .format(', '.join(['?' for _ in witnesses_id]))

    return pandas.read_sql(MY_SQL, conn, params=witnesses_id)


def get_selected_evidance(conn: sqlite3.Connection, evidances_id):
    MY_SQL = '''
            SELECT *
            FROM "evidance"
            WHERE evidance_id IN ({0})
            '''\
            .format(', '.join(['?' for _ in evidances_id]))

    return pandas.read_sql(MY_SQL, conn, params=evidances_id)

def get_filter_case(conn: sqlite3.Connection, suspects_id, witnesses_id, evidances_id, actuality):

    sql_actuality = ""
    if (actuality == "opened"):
        sql_actuality = "closed = 0"
    elif (actuality == "closed"):
        sql_actuality = "closed = 1"

    if (len(suspects_id) == 0 and len(witnesses_id) == 0 and len(evidances_id) == 0):
        if sql_actuality == "":
            return pandas.read_sql('SELECT * FROM "case"', conn)
        else:
            return pandas.read_sql('SELECT * FROM "case" WHERE ' + sql_actuality, conn)
    
    print(suspects_id)
    cur = conn.cursor()
    if len(suspects_id) == 0:
        cur.execute('SELECT sus_wit_id FROM "suspect_witness" WHERE sus_wit_type = "suspect"')
        suspects_id = [x[0] for x in cur.fetchall()]
    if len(witnesses_id) == 0:
        cur.execute('SELECT sus_wit_id FROM "suspect_witness" WHERE sus_wit_type = "witness"')
        witnesses_id = [x[0] for x in cur.fetchall()]
    if len(evidances_id) == 0:
        cur.execute("SELECT evidance_id FROM evidance")
        evidances_id = [x[0] for x in cur.fetchall()]

    MY_SQL = '''
            SELECT DISTINCT "case".*
            FROM "case"
            JOIN sus_wit_case AS swc1 USING(case_id)
            JOIN sus_wit_case AS swc2 USING(case_id)
            JOIN evidance_case USING(case_id)
            WHERE swc1.sus_wit_id IN ({0}) AND swc2.sus_wit_id IN ({1}) AND evidance_id IN ({2})
            '''\
            .format(', '.join(['?' for _ in suspects_id]), ', '.join(['?' for _ in witnesses_id]), ', '.join(['?' for _ in evidances_id]))
    
    if (actuality == "opened"):
        MY_SQL += "AND closed = 0"
    elif (actuality == "closed"):
        MY_SQL += "AND closed = 1"

    
    return pandas.read_sql(MY_SQL, conn, params=(suspects_id + witnesses_id + evidances_id))

def get_closest_interogations(conn):
    return pandas.read_sql(
        '''
        SELECT case_id AS 'Номер дела', interogation_id AS 'Номер допроса', date AS 'Дата и время допроса', sus_wit_name AS 'Имя свидетеля/подозреваемого'
        FROM "interogation"
        JOIN "sus_wit_case" USING(swc_id)
        JOIN "suspect_witness" USING(sus_wit_id)
        WHERE testimony IS NULL
        ORDER BY date ASC
        ''', conn
    )

def get_work_schedule(conn):
    return pandas.read_sql(
    '''
    SELECT * FROM "work_schedule"
    ''', conn)

def set_new_inter_date(conn: sqlite3.Connection, inter_id, date_time):
    cur = conn.cursor()

    cur.execute('''
                    UPDATE interogation
                    SET date = :date
                    WHERE interogation_id = :inter_id
                ''', {"inter_id": inter_id, "date": date_time})
    conn.commit()

def set_new_testimony(conn: sqlite3.Connection, inter_id, testimony):
    cur = conn.cursor()

    cur.execute('''
                    UPDATE interogation
                    SET testimony = :testim
                    WHERE interogation_id = :inter_id
                ''', {"inter_id": inter_id, "testim": testimony})
    conn.commit()
    
    