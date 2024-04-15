CREATE DATABASE IF NOT EXISTS LL_database;
USE LL_database;

-- Create the CHAMPION table
CREATE TABLE IF NOT EXISTS CHAMPION (
    cname TEXT NOT NULL PRIMARY KEY,
    recommend_build_id INTEGER,
    recommended_skillorder_id INTEGER,
    recommended_runepage_id INTEGER,
    FOREIGN KEY (recommend_build_id) REFERENCES BUILD(id),
    FOREIGN KEY (recommended_skillorder_id) REFERENCES SKILL_ORDER(id),
    FOREIGN KEY (recommended_runepage_id) REFERENCES RUNE_PAGE(id)
);

-- Create the BUILD table
CREATE TABLE IF NOT EXISTS BUILD (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_count INTEGER,
    win_count INTEGER,
    item1 TEXT,
    item2 TEXT,
    item3 TEXT,
    cname TEXT,
    FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
);

-- Create the SKILL_ORDER table
CREATE TABLE IF NOT EXISTS SKILL_ORDER (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_count INTEGER,
    win_count INTEGER,
    skill1 TEXT,
    skill2 TEXT,
    skill3 TEXT,
    cname TEXT,
    FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
);

-- Create the RUNE_PAGE table
CREATE TABLE IF NOT EXISTS RUNE_PAGE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_count INTEGER,
    win_count INTEGER,
    slot1 TEXT,
    slot2 TEXT,
    slot3 TEXT,
    slot4 TEXT,
    slot5 TEXT,
    slot6 TEXT,
    cname TEXT,
    FOREIGN KEY (cname) REFERENCES CHAMPION(cname) ON DELETE CASCADE
);

-- Create the MATCHES table
CREATE TABLE IF NOT EXISTS MATCHES (
    id TEXT PRIMARY KEY
);
