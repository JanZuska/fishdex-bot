import mysql.connector
import json

with open("assets/json/database-table.json", "r") as file:
    db_data = json.load(file)
    file.close()

class Database:
    def __init__(self, user_id: str) -> None:
        self.user = user_id
        self.table = f"{self.user}_fish"
        self.db = mysql.connector.connect(
            host="161.97.78.70",
            user="u20308_biZS5fqQ4I",
            password="D4XINz=55uky4GJ=VxX^k0Pt",
            database="s20308_fishdex")
        self.cursor = self.db.cursor()
        self.__Table()
        
    def __Table(self) -> None:
        show_tables_query = "SHOW TABLES LIKE %s"
        self.cursor.execute(show_tables_query, [self.table])
        result = self.cursor.fetchone()
        if not result:
            self.__CreateTable()   
        

    def __CreateTable(self) -> None:
        create_table_query = f"""
            CREATE TABLE {self.table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fish_name VARCHAR(255),
                locations VARCHAR(255),
                caught BOOLEAN DEFAULT FALSE,
                shiny BOOLEAN DEFAULT FALSE)"""
        insert_query = f"""
            INSERT INTO {self.table} (fish_name, locations)
            VALUES (%s, %s)"""
        self.cursor.execute(create_table_query)
        self.db.commit()
        self.cursor.executemany(insert_query, db_data)
        self.db.commit()

    def Caught(self, location_id: int = None) -> str:
        if location_id:
            if location_id == "1":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                AND caught = True
                OR FIND_IN_SET('101', REPLACE(locations, ', ', ',')) > 0
                AND caught = True"""
            elif location_id == "5":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                AND caught = True
                OR FIND_IN_SET('104', REPLACE(locations, ', ', ',')) > 0
                AND caught = True"""
            else:
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                AND caught = True"""
        else:
            select_where_query = f"""
              SELECT * FROM {self.table} 
              WHERE caught = True"""
        self.cursor.execute(select_where_query)
        result = self.cursor.fetchall()
        caught = len(result)

        if location_id:
            if location_id == "1":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                OR FIND_IN_SET('101', REPLACE(locations, ', ', ',')) > 0"""
            elif location_id == "5":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                OR FIND_IN_SET('104', REPLACE(locations, ', ', ',')) > 0"""
            else:
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0"""
        else:
            select_where_query = f"""
              SELECT * FROM {self.table}"""
        self.cursor.execute(select_where_query)
        result = self.cursor.fetchall()
        maximum = len(result)

        return f"{caught}/{maximum}"
    
    def Shiny(self, location_id: int = None) -> str:
        if location_id:
            if location_id == "1":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                AND caught = True
                OR FIND_IN_SET('101', REPLACE(locations, ', ', ',')) > 0
                AND shiny = True"""
            elif location_id == "5":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                AND caught = True
                OR FIND_IN_SET('104', REPLACE(locations, ', ', ',')) > 0
                AND shiny = True"""
            else:
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                AND shiny = True"""
        else:
            select_where_query = f"""
              SELECT * FROM {self.table} 
              WHERE shiny = True"""
        self.cursor.execute(select_where_query)
        result = self.cursor.fetchall()
        caught = len(result)

        if location_id:
            if location_id == "1":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                OR FIND_IN_SET('101', REPLACE(locations, ', ', ',')) > 0"""
            elif location_id == "5":
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0
                OR FIND_IN_SET('104', REPLACE(locations, ', ', ',')) > 0"""
            else:
                select_where_query = f"""
                SELECT * FROM {self.table} 
                WHERE FIND_IN_SET('{location_id}', REPLACE(locations, ', ', ',')) > 0"""
        else:
            select_where_query = f"""
              SELECT * FROM {self.table}"""
        self.cursor.execute(select_where_query)
        result = self.cursor.fetchall()
        maximum = len(result)
        
        return f"{caught}/{maximum}"
    
    def isCaught(self, fish_name: str) -> bool:
        select_where_query = f"""
          SELECT caught FROM {self.table} 
          WHERE fish_name = %s"""
        self.cursor.execute(select_where_query, [fish_name])
        result = self.cursor.fetchone()
        return bool(result[0])
    
    def isShiny(self, fish_name: str) -> bool:
        select_where_query = f"""
          SELECT shiny FROM {self.table} 
          WHERE fish_name = %s"""
        self.cursor.execute(select_where_query, [fish_name])
        result = self.cursor.fetchone()
        return bool(result[0])
    
    def SetCaught(self, fish_name: str, true: bool) -> None:
        update_query = f"""
          UPDATE {self.table}
          SET caught = %s
          WHERE fish_name = %s
          """
        self.cursor.execute(update_query, [true, fish_name])
        self.db.commit()

    def SetShiny(self, fish_name: str, true: bool) -> None:
        update_query = f"""
          UPDATE {self.table}
          SET shiny = %s
          WHERE fish_name = %s
          """
        self.cursor.execute(update_query, [true, fish_name])
        self.db.commit()

if __name__ == "__main__":
    x = Database(465456282401243137)
    x.SetCaught("Acanthodes", False)
    print(x.isCaught("Acanthodes"))