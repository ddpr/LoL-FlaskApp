from flask import Flask, render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
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
    print("Recskills:", recskill,flush=True)  #Debug
    print("Recrune:", recrune,flush=True)  #Debug

    return recbuild[0]["id"],recskill[0]["id"],recrune[0]["id"],recbuild[0]["weighted_win_ratio"]
    
@app.route('/')
def index():
    return render_template("index.html")

###Endpoints for managing rune pages (CRUD Operations)

@app.route('/managerunepages')
def managerunepages():
    return render_template("managerunepage.html")

@app.route('/searchrunepages', methods = ['GET','POST'])
def searchrunepages():
    cn = request.form['champname']
    runequery = """
                SELECT id, slot1, slot2, slot3, slot4, slot5, slot6, win_count, game_count from rune_page WHERE cname = %s
                """
    runes = LL_CRUD.run_query(runequery,cn,True)
    return render_template('managerunepage.html',champion = cn, runes=runes)

@app.route('/addrunepage', methods = ('GET', 'POST'))
def addrunepage():
    if request.method == 'POST':
        cn = request.form['champname']
        slot1 = request.form['slot1']
        slot2 = request.form['slot2']
        slot3 = request.form['slot3']
        slot4 = request.form['slot4']
        slot5 = request.form['slot5']
        slot6 = request.form['slot6']
        win_count = int(request.form['win_count'])
        
        updatecheck = LL_CRUD.read_rune_page(slot1,slot2,slot3,slot4,slot5,slot6,cn)
        if len(updatecheck) == 0:
            LL_CRUD.create_rune_page(win_count,slot1,slot2,slot3,slot4,slot5,slot6,cn)
        else:
            LL_CRUD.update_rune_page(win_count,slot1,slot2,slot3,slot4,slot5,slot6,cn)
        return render_template('managerunepage.html')
    return render_template('addrunepage.html')

# @app.route('/editrunepage/<int:id>', methods = ('GET','POST'))
# def editrunepage(id):
#     query = """
#                 SELECT cname, slot1, slot2, slot3, slot4, slot5, slot6, win_count FROM rune_page WHERE id = %s
#             """
#     results = LL_CRUD.run_query(query,id,True)
#     cn = results[0]['cname']
#     slot1 = results[0]['slot1']
#     slot2 = results[0]['slot2']
#     slot3 = results[0]['slot3']
#     slot4 = results[0]['slot4']
#     slot5 = results[0]['slot5']
#     slot6 = results[0]['slot6']
#     win_count = results[0]['win_count']
#     if request.method == 'POST':
#         return render_template('managerunepage.html')
#     return render_template('addrunepage.html', edit = True, values = results)

@app.route('/deleterunepage/<int:id>',methods=('POST',))
def deleterunepage(id):
    query = """
            SELECT slot1, slot2, slot3, slot4, slot5, slot6, cname FROM rune_page WHERE id = %s
            """
    result = LL_CRUD.run_query(query,id,True)
    
    slot1 = result[0]['slot1']
    slot2 = result[0]['slot2']
    slot3 = result[0]['slot3']
    slot4 = result[0]['slot4']
    slot5 = result[0]['slot5']
    slot6 = result[0]['slot6']
    cn = result[0]['cname']
    print("result:", result,flush=True)
    LL_CRUD.delete_rune_page(slot1,slot2,slot3,slot4,slot5,slot6,cn)

    runequery = """
                SELECT id, slot1, slot2, slot3, slot4, slot5, slot6, win_count, game_count from rune_page WHERE cname = %s
                """
    runes = LL_CRUD.run_query(runequery,cn,True)
    return render_template('managerunepage.html',champion = cn, runes = runes)


###Endpoints for managing skill orders (CRUD Operations)

@app.route('/manageskillorders')
def manageskillorders():
    return render_template("manageskillorder.html")

@app.route('/searchskillorders', methods = ['GET','POST'])
def searchskillorders():
    cn = request.form['champname']
    skillquery = """
                SELECT id, skill1, skill2, skill3, win_count, game_count from skill_order WHERE cname = %s
                """
    skills = LL_CRUD.run_query(skillquery,cn,True)
    return render_template('manageskillorder.html',champion = cn, skills=skills)

@app.route('/addskillorder', methods = ('GET', 'POST'))
def addskillorders():
    if request.method == 'POST':
        cn = request.form['champname']
        skill1 = request.form['skill1']
        skill2 = request.form['skill2']
        skill3 = request.form['skill3']
        win_count = int(request.form['win_count'])
        LL_CRUD.create_skill_order(win_count,skill1,skill2,skill3,cn)
        updatecheck = LL_CRUD.read_skill_order(skill1,skill2,skill3,cn)
        if len(updatecheck) == 0:
            LL_CRUD.create_skill_order(win_count,skill1,skill2,skill3,cn)
        else:
            LL_CRUD.update_skill_order(win_count,skill1,skill2,skill3,cn)
        return render_template('manageskillorder.html')
    return render_template('addskillorder.html')

@app.route('/deleteskillorder/<int:id>',methods=('POST',))
def deleteskillorder(id):
    query = """
            SELECT skill1, skill2, skill3,  win_count, cname FROM skill_order WHERE id = %s
            """
    result = LL_CRUD.run_query(query,id,True)
    skill1 = result[0]['skill1']
    skill2 = result[0]['skill2']
    skill3 = result[0]['skill3']
    cn = result[0]['cname']

    LL_CRUD.delete_skill_order(skill1,skill2,skill3,cn)

    skillquery = """
                SELECT id, skill1, skill2, skill3, win_count, game_count from skill_order WHERE cname = %s
                """
    skills = LL_CRUD.run_query(skillquery,cn,True)

    return render_template('manageskillorder.html',champion = cn, skills = skills)




###Endpoints for managing builds (CRUD Operations)
 
@app.route('/managebuild')
def managebuild():
    return render_template("managebuilds.html")

@app.route('/searchbuilds', methods = ['GET','POST'])
def searchbuilds():
    cn = request.form['champname']
    buildquery = """
                SELECT id, item1, item2, item3, win_count, game_count from build WHERE cname = %s
                """
    builds = LL_CRUD.run_query(buildquery,cn,True)
    return render_template('managebuilds.html',champion = cn, builds = builds)

@app.route('/addbuild', methods = ('GET', 'POST'))
def addbuild():
    if request.method == 'POST':
        cn = request.form['champname']
        item1 = request.form['item1']
        item2 = request.form['item2']
        item3 = request.form['item3']
        win_count = int(request.form['win_count'])
        LL_CRUD.create_build(win_count,item1,item2,item3,cn)
        updatecheck = LL_CRUD.read_build(item1,item2,item3,cn)
        if len(updatecheck) == 0:
            LL_CRUD.read_build(item1,item2,item3,cn)
        else:
            LL_CRUD.update_build(win_count,item1,item2,item3,cn)
        return render_template('managebuilds.html')
    return render_template('addbuild.html')

@app.route('/deletebuild/<int:id>',methods=('POST',))
def deletebuild(id):
    query = """
            SELECT item1, item2, item3, win_count, cname FROM build WHERE id = %s
            """
    result = LL_CRUD.run_query(query,id,True)
    item1 = result[0]['item1']
    item2 = result[0]['item2']
    item3 = result[0]['item3']
    win_count = result[0]['win_count']
    cname = result[0]['cname']

    LL_CRUD.delete_build(item1,item2,item3,cname)

    buildquery = """
                SELECT id, item1, item2, item3, win_count, game_count from build WHERE cname = %s
                """
    builds = LL_CRUD.run_query(buildquery,cname,True)

    return render_template('managebuilds.html',champion = cname, builds = builds)

@app.route('/championsuggest', methods = ['GET','POST'])
def championsuggest():
    if request.method == 'POST':
        cn1 = request.form['champname1']
        cn2 = request.form['champname2']
        cn3 = request.form['champname3']
        cnlist = [cn1,cn2,cn3]
        heighest_weighted_win_ratio = 0
        for i in range(3):
            cn = cnlist[i]
            #Checking if champion is a valid champ at all (exist in build table)
            validchampquery = """
                        SELECT EXISTS (SELECT cname FROM build WHERE cname = %s) AS result
                        """
            validchamp = LL_CRUD.run_query(validchampquery,cn,True)[0]['result']
            print(validchamp, flush=True) #Debug
            
            #If champion is valid, check if its in the champion table, if not in champion table then add it along with it's recs
            if validchamp:
                existquery = """
                SELECT cname FROM champion WHERE cname = %s
                """
                exist = [champ ['cname'] for champ in LL_CRUD.run_query(existquery,cn,True)]
                print(exist, flush=True) #Debug 
                if not exist:
                    inserquery = """
                    INSERT INTO champion (cname, recommend_build_id, recommended_skillorder_id, recommended_runepage_id) VALUES (%s,%s,%s,%s)
                    """
                    recbuild, recskill, recrune, weighted_win_ratio = getrecs(cn)
                    print("weights: ", cn, weighted_win_ratio)
                    LL_CRUD.run_query(inserquery,(cn,recbuild,recskill,recrune),False)
                if weighted_win_ratio > heighest_weighted_win_ratio:
                    heighest_weighted_win_ratio = weighted_win_ratio
                    print("Inserted:", cn,recbuild,recskill,recrune,"into champion table",  flush=True) #Debug

                    query = """
                    SELECT DISTINCT cname FROM champion WHERE cname = %s
                    """
                    champname = LL_CRUD.run_query(query,cn,True)[0]['cname']
                    print(champname,flush=True)

                    buildquery ="""
                                SELECT item1, item2, item3,skill1, skill2, skill3, slot1, slot2, slot3, slot4, slot5, slot6 
                                FROM champion 
                                LEFT JOIN build ON champion.recommend_build_id = build.id
                                LEFT JOIN skill_order ON champion.recommended_skillorder_id = skill_order.id
                                LEFT JOIN rune_page ON champion.recommended_runepage_id = rune_page.id 
                                WHERE champion.cname = %s
                                """
                    build = LL_CRUD.run_query(buildquery,cn,True)
            else:
                return render_template("index.html") #Provide an error message of some sort
        return render_template('champbuilds.html', champname = champname, build = build)
        
    else:
        return render_template("index.html")
    
@app.route('/champion', methods = ['GET', 'POST'])
def champsearch():
    if request.method =='POST':
        cn = request.form['champname']

        #Checking if champion is a valid champ at all (exist in build table)
        validchampquery = """
                    SELECT EXISTS (SELECT cname FROM build WHERE cname = %s) AS result
                    """
        validchamp = LL_CRUD.run_query(validchampquery,cn,True)[0]['result']
        print(validchamp, flush=True) #Debug
        
        #If champion is valid, check if its in the champion table, if not in champion table then add it along with it's recs
        if validchamp:
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
            champname = LL_CRUD.run_query(query,cn,True)[0]['cname']
            print(champname,flush=True)

            buildquery ="""
                        SELECT item1, item2, item3,skill1, skill2, skill3, slot1, slot2, slot3, slot4, slot5, slot6 
                        FROM champion 
                        LEFT JOIN build ON champion.recommend_build_id = build.id
                        LEFT JOIN skill_order ON champion.recommended_skillorder_id = skill_order.id
                        LEFT JOIN rune_page ON champion.recommended_runepage_id = rune_page.id 
                        WHERE champion.cname = %s
                        """
            build = LL_CRUD.run_query(buildquery,cn,True)

            return render_template('champbuilds.html', champname = champname, build = build)
        
        else:
            return render_template("index.html") #Provide an error message of some sort
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)