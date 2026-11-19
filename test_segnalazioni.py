import unittest
from datetime import date

from prenotazioni import DataNonAmmessa, Flotta, Noleggio, Veicolo


class TestSegnalazioni(unittest.TestCase):
    def test_noleggio_fine_uguale_a_inizio_solleva_value_error(self):
        with self.assertRaises(ValueError):
            Noleggio(
                "F1",
                date(2026, 11, 18),
                "10:00",
                "10:00",
                "Mario Rossi",
                2,
            )

    def test_giorno_chiusura_giovedi_rifiutato_e_mercoledi_ammesso(self):
        flotta = Flotta()
        flotta.aggiungi_veicolo(Veicolo("U1", "Utilitaria", 4))
        oggi = date(2026, 11, 16)  # lunedì

        noleggio_giovedi = Noleggio(
            "U1",
            date(2026, 11, 19),  # giovedì
            "09:00",
            "10:00",
            "Mario Rossi",
            2,
        )
        with self.assertRaises(DataNonAmmessa):
            flotta.prenota(noleggio_giovedi, oggi=oggi)

        noleggio_mercoledi = Noleggio(
            "U1",
            date(2026, 11, 18),  # mercoledì
            "09:00",
            "10:00",
            "Mario Rossi",
            2,
        )
        id_noleggio = flotta.prenota(noleggio_mercoledi, oggi=oggi)
        self.assertEqual(id_noleggio, 1)


if __name__ == "__main__":
    unittest.main()
