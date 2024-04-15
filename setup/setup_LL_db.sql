CREATE DATABASE IF NOT EXISTS LL_database;
USE LL_database;


CREATE TABLE IF NOT EXISTS CHAMPION (
    cname VARCHAR(255) NOT NULL PRIMARY KEY,
    recommend_build_id INTEGER,
    recommended_skillorder_id INTEGER,
    recommended_runepage_id INTEGER,
    FOREIGN KEY (recommend_build_id) REFERENCES BUILD(id),
    FOREIGN KEY (recommended_skillorder_id) REFERENCES SKILL_ORDER(id),
    FOREIGN KEY (recommended_runepage_id) REFERENCES RUNE_PAGE(id)
);


CREATE TABLE IF NOT EXISTS BUILD (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_count INTEGER,
    win_count INTEGER,
    item1 VARCHAR(255),
    item2 VARCHAR(255),
    item3 VARCHAR(255),
    cname VARCHAR(255),
    FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS SKILL_ORDER (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_count INTEGER,
    win_count INTEGER,
    skill1 VARCHAR(255),
    skill2 VARCHAR(255),
    skill3 VARCHAR(255),
    cname VARCHAR(255),
    FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS RUNE_PAGE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- Create the MATCHES table
CREATE TABLE IF NOT EXISTS MATCHES (
    id TEXT PRIMARY KEY
);