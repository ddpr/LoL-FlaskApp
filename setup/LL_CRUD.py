import pymysql
from pymysql import err

DATABASE_NAME = "LL_database"

# Utility function to execute a query with error handling
def run_query(query, parameters=None, is_select=False):
    result = None
    try:
        conn = pymysql.connect(
            host='localhost',          # Replace 
            db=DATABASE_NAME,
            user='your_username',      # Replace 
            password='your_password',  # Replace 
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute(query, parameters)
            if is_select:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
    except err.MySQLError as e:
        print(f"SQL Error: {e}")
    finally:
        if conn:
            conn.close()
    return result

# CRUD operations for the 'CHAMPION' table
def create_champion(cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id):
    query = """
    INSERT INTO CHAMPION (cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id)
    VALUES (%s, %s, %s, %s)
    """
    return run_query(query, (cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id))

def read_champion(cname):
    query = "SELECT * FROM CHAMPION WHERE cname = %s"
    return run_query(query, (cname,), is_select=True)

def update_champion(cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id):
    query = """
    UPDATE CHAMPION SET recommend_build_id = %s, recommended_skillorder_id = %s, recommended_runepage_id = %s
    WHERE cname = %s
    """
    return run_query(query, (recommend_build_id, recommended_skillorder_id, recommended_runepage_id, cname))

def delete_champion(cname):
    query = "DELETE FROM CHAMPION WHERE cname = %s"
    return run_query(query, (cname,))

# CRUD operations for the 'BUILD' table
def create_build(win_count, item1, item2, item3, cname):
    query = """
    INSERT INTO BUILD (game_count, win_count, item1, item2, item3, cname)
    VALUES (1, %s, %s, %s, %s, %s)
    """
    return run_query(query, (win_count, item1, item2, item3, cname))

def read_build(item1, item2, item3, cname):
    query = """
    SELECT * FROM BUILD WHERE item1 = %s AND item2 = %s AND item3 = %s AND cname = %s
    """
    return run_query(query, (item1, item2, item3, cname), is_select=True)

def update_build(winOrLoss, item1, item2, item3, cname):
    getWinsGamesQ = """
    SELECT win_count, game_count FROM BUILD WHERE item1 = %s AND item2 = %s AND item3 = %s AND cname = %s
    """
    result = run_query(getWinsGamesQ, (item1, item2, item3, cname), is_select=True)
    if result:
        current_wins, current_games = result[0]['win_count'], result[0]['game_count']
        query = """
        UPDATE BUILD SET game_count = %s, win_count = %s WHERE item1 = %s AND item2 = %s AND item3 = %s AND cname = %s
        """
        return run_query(query, (current_games + 1, current_wins + winOrLoss, item1, item2, item3, cname))

def delete_build(item1, item2, item3, cname):
    query = """
    DELETE FROM BUILD WHERE item1 = %s AND item2 = %s AND item3 = %s AND cname = %s
    """
    return run_query(query, (item1, item2, item3, cname))

# CRUD operations for the 'SKILL_ORDER' table
def create_skill_order(win_count, skill1, skill2, skill3, cname):
    query = """
    INSERT INTO SKILL_ORDER (game_count, win_count, skill1, skill2, skill3, cname)
    VALUES (1, %s, %s, %s, %s, %s)
    """
    return run_query(query, (win_count, skill1, skill2, skill3, cname))

def read_skill_order(skill1, skill2, skill3, cname):
    query = """
    SELECT * FROM SKILL_ORDER WHERE skill1 = %s AND skill2 = %s AND skill3 = %s AND cname = %s
    """
    return run_query(query, (skill1, skill2, skill3, cname), is_select=True)

def update_skill_order(winOrLoss, skill1, skill2, skill3, cname):
    getWinsGamesQ = """
    SELECT win_count, game_count FROM SKILL_ORDER WHERE skill1 = %s AND skill2 = %s AND skill3 = %s AND cname = %s
    """
    result = run_query(getWinsGamesQ, (skill1, skill2, skill3, cname), is_select=True)
    if result:
        current_wins, current_games = result[0]['win_count'], result[0]['game_count']
        query = """
        UPDATE SKILL_ORDER SET game_count = %s, win_count = %s WHERE skill1 = %s AND skill2 = %s AND skill3 = %s AND cname = %s
        """
        return run_query(query, (current_games + 1, current_wins + winOrLoss, skill1, skill2, skill3, cname))

def delete_skill_order(skill1, skill2, skill3, cname):
    query = """
    DELETE FROM SKILL_ORDER WHERE skill1 = %s AND skill2 = %s AND skill3 = %s AND cname = %s
    """
    return run_query(query, (skill1, skill2, skill3, cname))

# CRUD operations for the 'RUNE_PAGE' table
def create_rune_page(win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname):
    query = """
    INSERT INTO RUNE_PAGE (game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname)
    VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return run_query(query, (win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname))

def read_rune_page(slot1, slot2, slot3, slot4, slot5, slot6, cname):
    query = """
    SELECT * FROM RUNE_PAGE WHERE slot1 = %s AND slot2 = %s AND slot3 = %s AND slot4 = %s AND slot5 = %s AND slot6 = %s AND cname = %s
    """
    return run_query(query, (slot1, slot2, slot3, slot4, slot5, slot6, cname), is_select=True)

def update_rune_page(winOrLoss, slot1, slot2, slot3, slot4, slot5, slot6, cname):
    getWinsGamesQ = """
    SELECT win_count, game_count FROM RUNE_PAGE WHERE slot1 = %s AND slot2 = %s AND slot3 = %s AND slot4 = %s AND slot5 = %s AND slot6 = %s AND cname = %s
    """
    result = run_query(getWinsGamesQ, (slot1, slot2, slot3, slot4, slot5, slot6, cname), is_select=True)
    if result:
        current_wins, current_games = result[0]['win_count'], result[0]['game_count']
        query = """
        UPDATE RUNE_PAGE SET game_count = %s, win_count = %s WHERE slot1 = %s, slot2 = %s, slot3 = %s, slot4 = %s, slot5 = %s, slot6 = %s, cname = %s
        """
        return run_query(query, (current_games + 1, current_wins + winOrLoss, slot1, slot2, slot3, slot4, slot5, slot6, cname))

def delete_rune_page(slot1, slot2, slot3, slot4, slot5, slot6, cname):
    query = """
    DELETE FROM RUNE_PAGE WHERE slot1 = %s, slot2 = %s, slot3 = %s, slot4 = %s, slot5 = %s, slot6 = %s, cname = %s
    """
    return run_query(query, (slot1, slot2, slot3, slot4, slot5, slot6, cname))

# CRUD operations for the 'MATCHES' table
def create_match(id):
    query = "INSERT INTO MATCHES (id) VALUES (%s)"
    return run_query(query, (id,))
    
def read_all_matches():
    query = "SELECT * FROM MATCHES"
    return run_query(query, (), is_select=True)
    
def delete_match(id):
    query = "DELETE FROM MATCHES WHERE id = %s"
    return run_query(query, (id,))
