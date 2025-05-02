import mysql.connector
import asyncio

old_db = mysql.connector.connect(
    host="161.97.78.70",
    user="u20308_biZS5fqQ4I",
    password="D4XINz=55uky4GJ=VxX^k0Pt",
    database="s20308_fishdex"
)

new_db = mysql.connector.connect(
    host="gameslim1.bisecthosting.com",
    user="u49705_7xoTAVCKTL",
    password="pz.4@kuZHqaIzZdt^H^nRc!E",
    database="s49705_fishdex"
)

# Vytvoření kurzorů pro starou a novou databázi
old_cursor = old_db.cursor()
new_cursor = new_db.cursor()


async def transfer_data(table_name):
    # Získání struktury tabulky z staré databáze
    old_cursor.execute(f"SHOW CREATE TABLE {table_name}")
    create_table_query = old_cursor.fetchone()[1]

    # Vytvoření tabulky v nové databázi
    new_cursor.execute(create_table_query)

    # Získání dat z tabulky v staré databázi
    old_cursor.execute(f"SELECT * FROM {table_name}")
    rows = old_cursor.fetchall()

    # Vytvoření dávky pro vložení
    batch_size = 615  # Počet řádků v jedné dávce
    batch_rows = []

    # Vložení dat do tabulky v nové databázi dávkou
    for row in rows:
        batch_rows.append(row)

        # Vložení dávky, pokud dosáhne maximální velikosti
        if len(batch_rows) == batch_size:
            await process_batch(table_name, batch_rows)
            batch_rows = []

    # Vložení případné poslední dávky
    if batch_rows:
        await process_batch(table_name, batch_rows)

    print(f"Tabulka {table_name} byla přenesena.")

async def process_batch(table_name, rows):
    # Připravení SQL dotazu pro vložení dávky řádků do tabulky
    placeholders = ",".join(["%s"] * len(rows[0]))
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    new_cursor.executemany(insert_query, rows)

async def main():
    # Získání seznamu tabulek z staré databáze
    old_cursor.execute("SHOW TABLES")
    tables = [table[0] for table in old_cursor.fetchall()]

    # Paralelní zpracování tabulek
    tasks = []

    for table in tables:
        task = asyncio.create_task(transfer_data(table))
        tasks.append(task)

        # Pokud máte k dispozici více výpočetních jader, můžete spustit více úkolů současně
        # V tomto příkladu spustíme maximálně 5 úkolů najednou
        if len(tasks) == 4:
            await asyncio.gather(*tasks)
            tasks = []

    # Zbývající úkoly
    if tasks:
        await asyncio.gather(*tasks)

    # Potvrzení a ukončení transakce v nové databázi
    new_db.commit()

    # Uzavření kurzorů a připojení k databázím
    old_cursor.close()
    new_cursor.close()
    old_db.close()
    new_db.close()

# Spuštění asynchronního hlavního programu
asyncio.run(main())