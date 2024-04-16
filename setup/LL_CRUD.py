import mysql.connector
from mysql.connector import Error

DATABASE_NAME = "LL_database"

# Utility function to execute a query with error handling
def run_query(query, parameters=(), is_select=False):
    try:
        conn = mysql.connector.connect(
            host='localhost',        #potentially replace
            database=DATABASE_NAME,
            user='your_username',    # need to replace
            password='your_password' #need to replace
        )
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        if is_select:
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        conn.commit()
        last_row_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_row_id
    except Error as e:
        print(f"SQL Error: {e}")

# CRUD for CHAMPION
def create_champion(cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id):
    return run_query("INSERT INTO CHAMPION VALUES (%s, %s, %s, %s)",
                     (cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id))
 
def read_champion(cname):
    return run_query("SELECT * FROM CHAMPION WHERE cname = %s", (cname,), is_select=True)
 
def update_champion(cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id):
    return run_query("UPDATE CHAMPION SET recommend_build_id = %s, recommended_skillorder_id = %s, recommended_runepage_id = %s WHERE cname = %s",
                     (recommend_build_id, recommended_skillorder_id, recommended_runepage_id, cname))
 
def delete_champion(cname):
    return run_query("DELETE FROM CHAMPION WHERE cname = %s", (cname,))
 
# CRUD for BUILD
# requested params: item1, item2, item3, cname
def create_build(game_count, win_count, item1, item2, item3, cname):
    return run_query("INSERT INTO BUILD VALUES (%s, %s, %s, %s, %s, %s)",
                     (game_count, win_count, item1, item2, item3, cname))
# requested params: item1, item2, item3, cname
def read_build(id):
    return run_query("SELECT * FROM BUILD WHERE id = %s", (id,), is_select=True)
# requested params: item1, item2, item3, cname, winLossIncrement (this will be a 0 or a 1 to note if you should add 1 to win_count)
def update_build(id, game_count, win_count, item1, item2, item3, cname):
    return run_query("UPDATE BUILD SET game_count = %s, win_count = %s, item1 = %s, item2 = %s, item3 = %s WHERE id = %s",
                     (game_count, win_count, item1, item2, item3, id))
 
def delete_build(id):
    return run_query("DELETE FROM BUILD WHERE id = %s", (id,))
 
# CRUD for SKILL_ORDER
# requested params: skill1, skill2, skill3, cname
def create_skill_order(game_count, win_count, skill1, skill2, skill3, cname):
    return run_query("INSERT INTO SKILL_ORDER VALUES (%s, %s, %s, %s, %s, %s)",
                     (game_count, win_count, skill1, skill2, skill3, cname))
# requested params: skill1, skill2, skill3, cname
def read_skill_order(id):
    return run_query("SELECT * FROM SKILL_ORDER WHERE id = %s", (id,), is_select=True)
# requested params: skill1, skill2, skill3, cname, winLossIncrement (this will be a 0 or a 1 to note if you should add 1 to win_count)
def update_skill_order(id, game_count, win_count, skill1, skill2, skill3, cname):
    return run_query("UPDATE SKILL_ORDER SET game_count = %s, win_count = %s, skill1 = %s, skill2 = %s, skill3 = %s WHERE id = %s",
                     (game_count, win_count, skill1, skill2, skill3, id))
 
def delete_skill_order(id):
    return run_query("DELETE FROM SKILL_ORDER WHERE id = %s", (id,))
 
# CRUD for RUNE_PAGE
# requested params: slot1, slot2, slot3, slot4, slot5, slot6, cname
def create_rune_page(game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname):
    return run_query("INSERT INTO RUNE_PAGE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname))
# requested params: slot1, slot2, slot3, slot4, slot5, slot6, cname
def read_rune_page(id):
    return run_query("SELECT * FROM RUNE_PAGE WHERE id = %s", (id,), is_select=True)
# requested params: slot1, slot2, slot3, slot4, slot5, slot6, cname, winLossIncrement(this will be a 0 or a 1 to note if you should add 1 to win_count)
def update_rune_page(id, game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, cname):
    return run_query("UPDATE RUNE_PAGE SET game_count = %s, win_count = %s, slot1 = %s, slot2 = %s, slot3 = %s, slot4 = %s, slot5 = %s, slot6 = %s WHERE id = %s",
                     (game_count, win_count, slot1, slot2, slot3, slot4, slot5, slot6, id))
 
def delete_rune_page(id):
    return run_query("DELETE FROM RUNE_PAGE WHERE id = %s", (id,))
#CRUD for MATCH
def create_match(id):
    return run_query("INSERT INTO MATCH VALUES (%s)" , (id,));
def read_match(id):
  return run_query("SELECT * FROM MATCH WHERE ID = %s" (id,), is_select=True)
def delete_match(id):
    return run_query("DELETE FROM MATCH WHERE id = %s", (id,))
 
