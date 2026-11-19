import unittest
from datetime import date, timedelta

from prenotazioni import (
    ORIZZONTE_GIORNI,
    DataNonAmmessa,
    Flotta,
    Noleggio,
    NoleggioNonTrovato,
    Veicolo,
    VeicoloNonTrovato,
)


class TestFlotta(unittest.TestCase):
    def setUp(self):
        self.flotta = Flotta()
        self.veicolo_a = Veicolo("A1", "Auto A", 4)
        self.veicolo_b = Veicolo("B1", "Auto B", 4)
        self.flotta.aggiungi_veicolo(self.veicolo_a)
        self.flotta.aggiungi_veicolo(self.veicolo_b)
        self.oggi = date(2026, 11, 16)  # lunedì

    def test_aggiungi_veicolo_duplicato_e_veicolo_inesistente(self):
        with self.assertRaises(ValueError):
            self.flotta.aggiungi_veicolo(Veicolo("A1", "Duplicato", 2))

        with self.assertRaises(VeicoloNonTrovato):
            self.flotta.veicolo("INESISTENTE")

    def test_prenota_controlli_data_e_limiti_orizzonte(self):
        noleggio_passato = Noleggio(
            "A1", self.oggi - timedelta(days=1), "08:00", "09:00", "Mario", 2
        )
        noleggio_oltre = Noleggio(
            "A1",
            self.oggi + timedelta(days=ORIZZONTE_GIORNI + 1),
            "08:00",
            "09:00",
            "Mario",
            2,
        )
        noleggio_oggi = Noleggio("A1", self.oggi, "08:00", "09:00", "Mario", 2)
        noleggio_limite = Noleggio(
            "A1",
            self.oggi + timedelta(days=ORIZZONTE_GIORNI),
            "08:00",
            "09:00",
            "Mario",
            2,
        )

        with self.assertRaises(DataNonAmmessa):
            self.flotta.prenota(noleggio_passato, oggi=self.oggi)
        with self.assertRaises(DataNonAmmessa):
            self.flotta.prenota(noleggio_oltre, oggi=self.oggi)

        id_oggi = self.flotta.prenota(noleggio_oggi, oggi=self.oggi)
        id_limite = self.flotta.prenota(noleggio_limite, oggi=self.oggi)
        self.assertEqual(id_oggi, 1)
        self.assertEqual(id_limite, 2)

    def test_id_progressivi_non_riutilizzati_dopo_cancellazione(self):
        n1 = Noleggio("A1", self.oggi, "08:00", "09:00", "Mario", 2)
        n2 = Noleggio("A1", self.oggi, "09:00", "10:00", "Luigi", 2)
        id1 = self.flotta.prenota(n1, oggi=self.oggi)
        self.flotta.prenota(n2, oggi=self.oggi)
        self.flotta.cancella(id1)
        n3 = Noleggio("A1", self.oggi, "10:00", "11:00", "Anna", 2)

        id3 = self.flotta.prenota(n3, oggi=self.oggi)

        self.assertEqual(id1, 1)
        self.assertEqual(id3, 3)

    def test_cancella_e_noleggio_id_inesistente_sollevano_noleggio_non_trovato(self):
        with self.assertRaises(NoleggioNonTrovato):
            self.flotta.cancella(999)

        with self.assertRaises(NoleggioNonTrovato):
            self.flotta.noleggio(999)

    def test_noleggi_del_giorno_ordinati_per_inizio_e_filtro_veicolo(self):
        # Ordine per codice: A1 (11:00), B1 (08:00), A1 (09:00)
        # Ordine per orario inizio: B1 (08:00), A1 (09:00), A1 (11:00)
        n_b_mattina = Noleggio("B1", self.oggi, "08:00", "09:00", "Mario", 2)
        n_a_tardi = Noleggio("A1", self.oggi, "11:00", "12:00", "Luigi", 2)
        n_a_meta = Noleggio("A1", self.oggi, "09:00", "10:00", "Anna", 2)
        self.flotta.prenota(n_a_tardi, oggi=self.oggi)
        self.flotta.prenota(n_b_mattina, oggi=self.oggi)
        self.flotta.prenota(n_a_meta, oggi=self.oggi)

        tutti = self.flotta.noleggi_del_giorno(self.oggi)
        solo_a1 = self.flotta.noleggi_del_giorno(self.oggi, veicolo_codice="A1")

        self.assertEqual([n.inizio for n in tutti], ["08:00", "09:00", "11:00"])
        self.assertEqual(
            [(n.veicolo_codice, n.inizio) for n in solo_a1],
            [("A1", "09:00"), ("A1", "11:00")],
        )


if __name__ == "__main__":
    unittest.main()
