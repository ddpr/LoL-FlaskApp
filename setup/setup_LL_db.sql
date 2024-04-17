import pymysql

# Establish a connection to the MySQL database
connection = pymysql.connect(host='your_host',
                             user='your_user',
                             password='your_password',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new database
        cursor.execute("CREATE DATABASE IF NOT EXISTS LL_database;")
        cursor.execute("USE LL_database;")

        # Create CHAMPION table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CHAMPION (
            cname VARCHAR(255) NOT NULL PRIMARY KEY,
            recommend_build_id INTEGER,
            recommended_skillorder_id INTEGER,
            recommended_runepage_id INTEGER,
            FOREIGN KEY (recommend_build_id) REFERENCES BUILD(id),
            FOREIGN KEY (recommended_skillorder_id) REFERENCES SKILL_ORDER(id),
            FOREIGN KEY (recommended_runepage_id) REFERENCES RUNE_PAGE(id)
        );
        """)

        # Create BUILD table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS BUILD (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            game_count INTEGER,
            win_count INTEGER,
            item1 VARCHAR(255),
            item2 VARCHAR(255),
            item3 VARCHAR(255),
            cname VARCHAR(255),
            FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
        );
        """)

        # Create SKILL_ORDER table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SKILL_ORDER (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            game_count INTEGER,
            win_count INTEGER,
            skill1 VARCHAR(255),
            skill2 VARCHAR(255),
            skill3 VARCHAR(255),
            cname VARCHAR(255),
            FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
        );
        """)

        # Create RUNE_PAGE table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS RUNE_PAGE (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            game_count INTEGER,
            win_count INTEGER,
            slot1 VARCHAR(255),
            slot2 VARCHAR(255),
            slot3 VARCHAR(255),
            slot4 VARCHAR(255),
            slot5 VARCHAR(255),
            slot6 VARCHAR(255),
            cname VARCHAR(255),
            FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
        );
        """)

        # Create MATCHES table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MATCHES (
            id VARCHAR(255) NOT NULL PRIMARY KEY
        );
        """)

        # Commit the changes to the database
        connection.commit()

finally:
    connection.close()
