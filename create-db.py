import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'resource_manager'

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(30) NOT NULL,"
    "  `password` varchar(20) NOT NULL,"
    "  `email` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['goods'] = (
    "CREATE TABLE `goods` ("
    "  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY `name` (`name`)"
    ") ENGINE=InnoDB")

TABLES['holds'] = (
    "CREATE TABLE `holds` ("
    "  `user_id` int(11) UNSIGNED NOT NULL,"
    "  `goods_id` int(11) UNSIGNED NOT NULL,"
    "  `value` decimal(5,1) NOT NULL,"
    "  `unit` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`user_id`,`goods_id`),"
    "  KEY `user_id` (`user_id`),"
    "  KEY `goods_id` (`goods_id`),"
    "  CONSTRAINT `user_goods_holds_1` FOREIGN KEY (`user_id`) "
    "     REFERENCES `users` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `user_goods_holds_2` FOREIGN KEY (`goods_id`) "
    "     REFERENCES `goods` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['consumers'] = (
    "CREATE TABLE `consumers` ("
    "  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `user_id` int(11) UNSIGNED NOT NULL,"
    "  `name` varchar(20) NOT NULL,"
    "  `period` char(1) NOT NULL,"
    "  `next_time` bigint(20) UNSIGNED NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `user_id` (`user_id`),"
    "  FOREIGN KEY (`user_id`) "
    "     REFERENCES `users` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['consumer_actions'] = (
    "CREATE TABLE `consumer_actions` ("
    "  `consumer_id` int(11) UNSIGNED NOT NULL,"
    "  `goods_id` int(11) UNSIGNED NOT NULL,"
    "  `value` decimal(5,1) NOT NULL,"
    "  `unit` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`consumer_id`,`goods_id`),"
    "  KEY `consumer_id` (`consumer_id`),"
    "  KEY `goods_id` (`goods_id`),"
    "  CONSTRAINT `consumer_goods_1` FOREIGN KEY (`consumer_id`) "
    "     REFERENCES `consumers` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `consumer_goods_2` FOREIGN KEY (`goods_id`) "
    "     REFERENCES `goods` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")



def init_db(host='localhost'):
    config = {
        'user': 'root',
        'password': 'pw',
        'host': host
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")

    

    cnx.close()
if __name__ == '__main__':
    init_db()