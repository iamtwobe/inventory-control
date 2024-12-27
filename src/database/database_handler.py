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
                CREATE TABLE IF NOT EXISTS categories (
                category_id     INTEGER      PRIMARY KEY  AUTOINCREMENT,
                category_name   VARCHAR(24)  NOT NULL     UNIQUE
            )
            """
        )

    def create_brand_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS brands (
                brand_id     INTEGER      PRIMARY KEY  AUTOINCREMENT,
                brand_name   VARCHAR(24)  NOT NULL     UNIQUE
            )
            """
        )

    def insert_product(self, product_name=None, product_category=None, product_price=None, product_brand=None, product_description=None):
        if not all([product_name, product_category, product_price, product_brand]):
            return "Missing required fields"
        
        try:
            self.cursor.execute(
                "SELECT category_id FROM categories WHERE category_name = ?",
                (product_category.lower(),)
            )
            category_id = self.cursor.fetchone()
            if not category_id:
                print("Category does not exist")
                return None
            
            self.cursor.execute(
                "SELECT brand_id FROM brands WHERE brand_name = ?",
                (product_brand.lower(),)
            )
            brand_id = self.cursor.fetchone()
            if not brand_id:
                print("Brand does not exist")
                return None

            self.cursor.execute(
                """
                    INSERT INTO products (product_name, product_category, product_price, product_brand, product_description)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (product_name, product_category.lower(), product_price, product_brand.lower(), product_description)
            )
            self.conn.commit()

            return 1
        except sqlite.IntegrityError:
            print("Product already exists")
            return None
        except Exception as e:
            print(e)
            return None

    def insert_category(self, category_name: str=None) -> None:
        if not category_name:
            print("Missing category_name")
            return None
        
        try:
            self.cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name.lower(),))
            self.conn.commit()
            return 1
        except sqlite.IntegrityError:
            print("Category already exists")
            return None
        
        except Exception as e:
            print(e)
            return None
        
    def insert_brand(self, brand_name: str=None) -> None:
        if not brand_name:
            print("Missing brand_name")
            return None
        try:
            self.cursor.execute("INSERT INTO brands (brand_name) VALUES (?)", (brand_name.lower(),))
            self.conn.commit()
            return 1
        except sqlite.IntegrityError:
            print("Brand already exists")
            return None
        
        except Exception as e:
            print(e)
            return None

    def get_all_table(self, table) -> list:
        table_data = self.cursor.execute(f"SELECT * FROM {table}")
        selection = table_data.fetchall()
        return self.verify_db(selection)
    
    def verify_db(self, selection) -> dict:
        if selection:
            if type(selection) is list:
                results = []
                for i in selection:
                    column_names = [description[0] for description in self.cursor.description]
                    result = dict(zip(column_names, i))
                    results.append(result)
                return results
            column_names = [description[0] for description in self.cursor.description]
            result = dict(zip(column_names, selection))
            return result
        else:
            return None

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    inventory_db = AppDatabase("src/database/inventory.db")


    #inventory_db.insert_category("processor")
    #inventory_db.insert_brand("corsair")
    
    inventory_db.insert_product("Fan BVT400", "fan", 199.90, "britania", "A super fan")
    query = inventory_db.get_all_table('brands')
    print(query)
    inventory_db.close()