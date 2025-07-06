import pytest
import uuid
from src.Improved_Task_Manager import pridat_ukol, aktualizovat_ukol, odstranit_ukol, pripojeni_db

@pytest.fixture
def test_ukol():
    # Vytvoří testovací úkol s unikátním názvem
    nazev = f"Testovací úkol {uuid.uuid4()}"
    pridat_ukol(nazev, "Popis testu")
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev=%s", (nazev,))
    ukol_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    yield ukol_id
    # Smaže testovací úkol po testu
    odstranit_ukol(ukol_id)

def test_pridat_ukol_pozitivni():
    nazev = f"Test {uuid.uuid4()}"
    try:
        assert pridat_ukol(nazev, "Popis") is True
        # Najdi ID nově vloženého úkolu
        conn = pripojeni_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE nazev=%s", (nazev,))
        ukol_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    finally:
        # Úklid
        if 'ukol_id' in locals():
            odstranit_ukol(ukol_id)

def test_pridat_ukol_negativni():
    assert pridat_ukol("", "") is False

def test_aktualizovat_ukol_pozitivni(test_ukol):
    assert aktualizovat_ukol(test_ukol, "Hotovo") is True

def test_aktualizovat_ukol_negativni():
    assert aktualizovat_ukol(999999, "Hotovo") is False

def test_odstranit_ukol_pozitivni():
    nazev = f"Smazat {uuid.uuid4()}"
    pridat_ukol(nazev, "Test")
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev=%s", (nazev,))
    ukol_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    assert odstranit_ukol(ukol_id) is True
    # Pokud by test selhal, úkol už je odstraněn

def test_odstranit_ukol_negativni():
    assert odstranit_ukol(999999) is False