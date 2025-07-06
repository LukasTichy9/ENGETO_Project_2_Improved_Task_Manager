import mysql.connector
from mysql.connector import Error
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bi35T88N',
    'database': 'task_manager'
}

def pripojeni_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None

def vytvoreni_tabulky():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

def pridat_ukol(nazev, popis):
    if not nazev or not popis:
        print("Název i popis jsou povinné!")
        return False
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
            (nazev, popis)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Úkol byl přidán.")
        return True

def zobrazit_ukoly():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nazev, popis, stav, datum_vytvoreni FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')"
        )
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Seznam úkolů je prázdný.")
        else:
            for u in ukoly:
                print(f"{u['id']}: {u['nazev']} | {u['popis']} | {u['stav']} | {u['datum_vytvoreni']}")
        cursor.close()
        conn.close()

def aktualizovat_ukol(ukol_id, novy_stav):
    if novy_stav not in ("Probíhá", "Hotovo"):
        print("Neplatný stav!")
        return False
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id=%s", (ukol_id,))
        if not cursor.fetchone():
            print("Úkol s tímto ID neexistuje.")
            cursor.close()
            conn.close()
            return False
        cursor.execute(
            "UPDATE ukoly SET stav=%s WHERE id=%s",
            (novy_stav, ukol_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Stav úkolu byl změněn.")
        return True

def odstranit_ukol(ukol_id):
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id=%s", (ukol_id,))
        if not cursor.fetchone():
            print("Úkol s tímto ID neexistuje.")
            cursor.close()
            conn.close()
            return False
        cursor.execute("DELETE FROM ukoly WHERE id=%s", (ukol_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Úkol byl odstraněn.")
        return True

def hlavni_menu():
    vytvoreni_tabulky()
    while True:
        print("\n--- Hlavní nabídka ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyber možnost (1-5): ").strip()
        if volba == "1":
            nazev = input("Zadej název úkolu: ").strip()
            popis = input("Zadej popis úkolu: ").strip()
            pridat_ukol(nazev, popis)
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            zobrazit_ukoly()
            try:
                ukol_id = int(input("Zadej ID úkolu pro aktualizaci: ").strip())
                novy_stav = input("Zadej nový stav (Probíhá/Hotovo): ").strip()
                aktualizovat_ukol(ukol_id, novy_stav)
            except ValueError:
                print("Neplatné ID! Zkus to znovu.")
        elif volba == "4":
            zobrazit_ukoly()
            try:
                ukol_id = int(input("Zadej ID úkolu pro odstranění: ").strip())
                odstranit_ukol(ukol_id)
            except ValueError:
                print("Neplatné ID! Zkus to znovu.")
        elif volba == "5":
            print("Program ukončen. Přejeme pěkný den!")
            break
        else:
            print("Neplatná volba! Zadej číslo od 1 do 5.")

if __name__ == "__main__":
    hlavni_menu()

