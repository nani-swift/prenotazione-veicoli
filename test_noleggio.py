from datetime import date, timedelta
import unittest

from prenotazioni import Noleggio


class TestNoleggio(unittest.TestCase):
    def setUp(self):
        self.giorno = date(2026, 11, 18)  # mercoledì
        self.noleggio_base = Noleggio(
            "F1",
            self.giorno,
            "08:00",
            "10:00",
            "Mario Rossi",
            2,
            "Ufficio",
        )

    def test_costruttore_orari_non_ammessi_solleva_value_error(self):
        casi_non_validi = [
            ("inizio_non_multiplo_30", "08:15", "09:00"),
            ("fine_non_multiplo_30", "08:00", "09:15"),
            ("inizio_prima_apertura", "06:00", "07:00"),
            ("fine_dopo_chiusura", "21:30", "22:30"),
            ("fine_precedente_inizio", "10:00", "09:00"),
        ]
        for descrizione, inizio, fine in casi_non_validi:
            with self.subTest(caso=descrizione):
                with self.assertRaises(ValueError):
                    Noleggio("F1", self.giorno, inizio, fine, "Mario Rossi", 2)

    def test_costruttore_giorno_non_date_solleva_type_error(self):
        with self.assertRaises(TypeError):
            Noleggio("F1", "2026-11-18", "08:00", "09:00", "Mario Rossi", 2)

    def test_durata_minuti_restituisce_durata_corretta(self):
        durata = self.noleggio_base.durata_minuti()

        self.assertEqual(durata, 120)

    def test_si_sovrappone_veicoli_giorni_diversi_e_intervallo_interno(self):
        altro_veicolo = Noleggio(
            "U1", self.giorno, "08:30", "09:30", "Luigi Verdi", 2
        )
        altro_giorno = Noleggio(
            "F1",
            self.giorno + timedelta(days=1),
            "08:30",
            "09:30",
            "Luigi Verdi",
            2,
        )
        interno = Noleggio("F1", self.giorno, "08:30", "09:30", "Luigi Verdi", 2)

        self.assertFalse(self.noleggio_base.si_sovrappone(altro_veicolo))
        self.assertFalse(self.noleggio_base.si_sovrappone(altro_giorno))
        self.assertTrue(self.noleggio_base.si_sovrappone(interno))

    def test_from_dict_e_to_dict_ricostruiscono_noleggio_con_id(self):
        self.noleggio_base.id = 7
        dati = self.noleggio_base.to_dict()

        ricostruito = Noleggio.from_dict(dati)

        self.assertEqual(ricostruito.id, 7)
        self.assertEqual(ricostruito.veicolo_codice, self.noleggio_base.veicolo_codice)
        self.assertEqual(ricostruito.giorno, self.noleggio_base.giorno)
        self.assertEqual(ricostruito.inizio, self.noleggio_base.inizio)
        self.assertEqual(ricostruito.fine, self.noleggio_base.fine)
        self.assertEqual(ricostruito.conducente, self.noleggio_base.conducente)
        self.assertEqual(ricostruito.persone, self.noleggio_base.persone)
        self.assertEqual(ricostruito.destinazione, self.noleggio_base.destinazione)


if __name__ == "__main__":
    unittest.main()