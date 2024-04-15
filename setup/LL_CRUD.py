import sqlite3
 
DATABASE_NAME = “LL_database.db"
 
# Utility function to execute a query with error handling
def run_query(query, parameters=(), is_select=False):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            if is_select:
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError as ie:
        print(f"Integrity Error: {ie}")
    except sqlite3.DataError as de:
        print(f"Data Error: {de}")
    except sqlite3.OperationalError as oe:
        print(f"Operational Error: {oe}")
    except sqlite3.DatabaseError as db_err:
        print(f"Database Error: {db_err}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
 
# CRUD for CHAMPION
def create_champion(cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id):
    return run_query("INSERT INTO CHAMPION VALUES (?, ?, ?, ?)",
                     (cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id))
 
def read_champion(cname):
    return run_query("SELECT * FROM CHAMPION WHERE cname = ?", (cname,), is_select=True)
 
def update_champion(cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id):
    return run_query("UPDATE CHAMPION SET recommend_build_id = ?, recommended_skillorder_id = ?, recommended_runepage_id = ? WHERE cname = ?",
                     (recommend_build_id, recommended_skillorder_id, recommended_runepage_id, cname))
 
def delete_champion(cname):
    return run_query("DELETE FROM CHAMPION WHERE cname = ?", (cname,))
 
# CRUD for BUILD
def create_build(id, game_count, win_count, item1, item2, item3, cname):
    return run_query("INSERT INTO BUILD VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (id, game_count, win_count, item1, item2, item3, cname))
 
def read_build(id):
    return run_query("SELECT * FROM BUILD WHERE id = ?", (id,), is_select=True)
 
def update_build(id, game_count, win_count, item1, item2, item3, cname):
    return run_query("UPDATE BUILD SET game_count = ?, win_count = ?, item1 = ?, item2 = ?, item3 = ? WHERE id = ?",
                     (game_count, win_count, item1, item2, item3, id))
 
def delete_build(id):
    return run_query("DELETE FROM BUILD WHERE id = ?", (id,))
 
# CRUD for SKILL_ORDER
def create_skill_order(id, game_count, win_count, skill1, skill2, skill3, cname):
    return run_query("INSERT INTO SKILL_ORDER VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (id, game_count, win_count, skill1, skill2, skill3, cname))
 
def read_skill_order(id):
    return run_query("SELECT * FROM SKILL_ORDER WHERE id = ?", (id,), is_select=True)
 
def update_skill_order(id, game_count, win_count, skill1, skill2, skill3, cname):
    return run_query("UPDATE SKILL_ORDER SET game_count = ?, win_count = ?, skill1 = ?, skill2 = ?, skill3 = ? WHERE id = ?",
                     (game_count, win_count, skill1, skill2, skill3, id))
 
def delete_skill_order(id):
    return run_query("DELETE FROM SKILL_ORDER WHERE id = ?", (id,))
 
# CRUD for RUNE_PAGE
def create_rune_page(id, game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname):
    return run_query("INSERT INTO RUNE_PAGE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (id, game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname))
 
def read_rune_page(id):
    return run_query("SELECT * FROM RUNE_PAGE WHERE id = ?", (id,), is_select=True)
 
def update_rune_page(id, game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname):
    return run_query("UPDATE RUNE_PAGE SET game_count = ?, win_count = ?, slot1 = ?, slot2 = ?, slot3 = ?, slot4 = ?, slot5 = ?, slot6 = ? WHERE id = ?",
                     (game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, id))
 
def delete_rune_page(id):
    return run_query("DELETE FROM RUNE_PAGE WHERE id = ?", (id,))
#CRUD for MATCH
def create_match(id):
    return run_query("INSERT INTO MATCH VALUES (?)" , (id));
def read_match(id):
  return run_query("SELECT * FROM MATCH WHERE ID = ?" (id,), is_select=True)
def delete_match(id):
    return run_query("DELETE FROM MATCH WHERE id = ?", (id,))
 
