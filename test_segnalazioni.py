import unittest
from datetime import date

from prenotazioni import Noleggio


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


if __name__ == "__main__":
    unittest.main()