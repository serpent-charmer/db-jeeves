START TRANSACTION;
        CREATE DATABASE db_jeeves;
        CREATE TABLE db_jeeves.USER (
            login VARCHAR(255),
            password VARCHAR(255),
            nickname VARCHAR(255),
            identity VARCHAR(255),
            PRIMARY KEY(login)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

        CREATE TABLE db_jeeves.PROJECT (
            ref_identity VARCHAR(255),
            lang VARCHAR(255),
            db_vendor VARCHAR(255),
            last_port INT(11),
            PRIMARY KEY(ref_identity)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
COMMIT;