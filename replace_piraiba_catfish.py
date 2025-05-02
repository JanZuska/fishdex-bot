import mysql.connector
from multiprocessing import Pool, freeze_support

# Funkce pro aktualizaci řádku
def update_row(table):
    try:
        connection = mysql.connector.connect(
            host="gameslim1.bisecthosting.com",
            user="u49705_7xoTAVCKTL",
            password="pz.4@kuZHqaIzZdt^H^nRc!E",
            database="s49705_fishdex")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {table} SET fish_name = 'Piraiba Catfish' WHERE id = 445")
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Chyba při aktualizaci řádku v tabulce {table}: {str(e)}")
        return False

# Získání seznamu tabulek z databáze
def get_table_list():
    try:
        connection = mysql.connector.connect(
            host="gameslim1.bisecthosting.com",
            user="u49705_7xoTAVCKTL",
            password="pz.4@kuZHqaIzZdt^H^nRc!E",
            database="s49705_fishdex")
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        connection.close()
        return tables
    except Exception as e:
        print(f"Chyba při získávání seznamu tabulek: {str(e)}")
        return []

# Zpracování tabulek ve více vláknech
def process_tables(table):
    result = update_row(table)
    if result:
        print(f"Aktualizace tabulky {table} dokončena.")

if __name__ == '__main__':
    # Zajištění podpory pro spuštění vícevláknového zpracování na Windows
    freeze_support()

    # Získání seznamu tabulek
    tables = get_table_list()

    # Zpracování tabulek ve více vláknech
    with Pool(processes=4) as pool:
        pool.map(process_tables, tables)