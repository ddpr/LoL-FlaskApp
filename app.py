from flask import Flask, render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import pymysql
from pymysql import err
import datetime
from setup import LL_CRUD

app = Flask(__name__)

DATABASE_NAME = "LL_database"

def getrecs(cname):
    buildquery = """
                SELECT id, (win_count/game_count) as win_ratio, (win_count*(win_count/game_count)) as weighted_win_ratio 
                FROM build WHERE cname = %s 
                ORDER BY weighted_win_ratio DESC LIMIT 1
                """
    runequery = """
                SELECT id, (win_count/game_count) as win_ratio, (win_count*(win_count/game_count)) as weighted_win_ratio 
                FROM rune_page WHERE cname = %s 
                ORDER BY weighted_win_ratio DESC LIMIT 1
                """
    skillquery = """
                SELECT id, (win_count/game_count) as win_ratio, (win_count*(win_count/game_count)) as weighted_win_ratio 
                FROM skill_order WHERE cname = %s 
                ORDER BY weighted_win_ratio DESC LIMIT 1
                """
    recbuild = LL_CRUD.run_query(buildquery,cname,True)
    recrune = LL_CRUD.run_query(runequery,cname,True)
    recskill = LL_CRUD.run_query(skillquery,cname,True)
    print(recbuild,flush=True)  #Debug
    print(recbuild[0]["id"],flush=True) #Debug
    #recbuild = LL_CRUD.run_query(buildquery2,is_select=True)
    return recbuild[0]["id"],recskill[0]["id"],recrune[0]["id"]
    
@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/addchampion')
# def addchampion():
#     if request.method == 'POST':
#         cname = request.form['cname']
#         try:
#             LL_CRUD.create_champion(cname,None,None,None)
#         except:
#             print("Failed")
#     return render_template('addchampion')

@app.route('/champion', methods = ['GET', 'POST'])
def champsearch():
    if request.method =='POST':
        cn = request.form['champname']
        existquery = """
        SELECT cname FROM champion WHERE cname = %s
        """
        exist = [champ ['cname'] for champ in LL_CRUD.run_query(existquery,cn,True)]
        print(exist, flush=True) #Debug 
        if not exist:
            inserquery = """
            INSERT INTO champion (cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id) VALUES (%s,%s,%s,%s)
            """
            recbuild, recskill, recrune = getrecs(cn)
            LL_CRUD.run_query(inserquery,(cn,recbuild,recskill,recrune),False)
            print("Inserted:", cn,recbuild,recskill,recrune,"into champion table",  flush=True) #Debug

        query = """
        SELECT DISTINCT cname FROM champion WHERE cname = %s
        """
        champname = [champ ['cname'] for champ in LL_CRUD.run_query(query,cn,True)]

        return render_template('champbuilds.html', champname = champname)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)