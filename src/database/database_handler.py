import sqlite3 as sqlite

class AppDatabase():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite.connect(db_name)
        self.cursor = self.conn.cursor()

        self.create_products_table()
        self.create_category_table()
        self.create_brand_table()
        
        self.conn.commit()

    
    def create_products_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS products (
                product_id                  INTEGER               PRIMARY KEY AUTOINCREMENT,
                product_name                VARCHAR(24)           NOT NULL,
                product_category            INTEGER               NOT NULL,
                product_price               FLOAT                 NOT NULL,
                product_brand               INTEGER               NOT NULL,
                product_description         VARCHAR(255)          NULL,

                FOREIGN KEY (product_category) REFERENCES categories(category_id),
                FOREIGN KEY (product_brand) REFERENCES brands(brand_id)
            )
            """
        )

    def create_category_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS category (
                category_id     INTEGER      PRIMARY KEY  AUTOINCREMENT,
                category_name   VARCHAR(24)  NOT NULL     UNIQUE
            )
            """
        )

    def create_brand_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS brand (
                brand_id     INTEGER      PRIMARY KEY  AUTOINCREMENT,
                brand_name   VARCHAR(24)  NOT NULL     UNIQUE
            )
            """
        )

    def close(self):
        self.conn.close()
        
    def __del__(self):
        self.conn.close()

inventory_db = AppDatabase("src/database/inventory.db")

if __name__ == "__main__":

    inventory_db.close()