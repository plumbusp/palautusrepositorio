import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()
        self.kauppa = Kauppa(
            self.varasto_mock,
            self.pankki_mock,
            self.viitegeneraattori_mock
        )
        def hae_tuote(tuote_id):
                if tuote_id == 1:
                    return Tuote(1, "maito", 5)
                if tuote_id == 2:
                    return Tuote(2, "suklaa", 10)
                
        self.varasto_mock.hae_tuote.side_effect = hae_tuote

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo


        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_added_product_that_in_storage__buy_with_right_values(self):
        self.varasto_mock.saldo.return_value = 1
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_once_with("pekka", ANY, "12345", ANY, 5)

    def test_added_two_products_that_in_storage__buy_with_right_values(self):
            def saldo(tuote_id):
                if tuote_id == 1:
                    return 1
                if tuote_id == 2:
                    return 2
                
            self.varasto_mock.saldo.side_effect = saldo
        
            self.kauppa.aloita_asiointi()
            self.kauppa.lisaa_koriin(1)
            self.kauppa.lisaa_koriin(2)
            self.kauppa.tilimaksu("jenna", "123456")
            self.pankki_mock.tilisiirto.assert_called_once_with("jenna", ANY, "123456", ANY, 15)


    def test_added_two_same_products_that_in_storage__buy_with_right_values(self):
                def saldo(tuote_id):
                    if tuote_id == 1:
                        saldo.count = saldo.count - 1
                        return saldo.count + 1
                saldo.count = 2

                self.varasto_mock.saldo.side_effect = saldo
            
                self.kauppa.aloita_asiointi()
                self.kauppa.lisaa_koriin(1)
                self.kauppa.lisaa_koriin(1)
                self.kauppa.tilimaksu("jenna", "123456")
                self.pankki_mock.tilisiirto.assert_called_once_with("jenna", ANY, "123456", ANY, 10)
    
    def test_added_two_products_but_second_not_in_storage__buy_with_right_values(self):
                def saldo(tuote_id):
                    if tuote_id == 1:
                        return 1
                    elif tuote_id == 2:
                        return 0
                    
                def hae_tuote(tuote_id):
                    if tuote_id == 1:
                        return Tuote(1, "maito", 5)
                    if tuote_id == 2:
                        return Tuote(2, "suklaa", 10)

                self.varasto_mock.saldo.side_effect = saldo
                self.varasto_mock.hae_tuote.side_effect = hae_tuote
            
                self.kauppa.aloita_asiointi()
                self.kauppa.lisaa_koriin(1)
                self.kauppa.lisaa_koriin(2)
                self.kauppa.tilimaksu("jenna", "123456")
                self.pankki_mock.tilisiirto.assert_called_once_with("jenna", ANY, "123456", ANY, 5)
    def test_aloita_asiointi_resets_data_on_buying(self):
        self.varasto_mock.saldo.return_value = 1
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.aloita_asiointi()
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_once_with("pekka", ANY, "12345", ANY, 0)

    def test_store_asks_for_new_reference_for_each_new_payment(self):
        def uusi():
            uusi.count +=1
            return uusi.count
        uusi.count = 0
        
        def saldo(tuote_id):
            if tuote_id == 1:
                return 1

        self.viitegeneraattori_mock.uusi.side_effect = uusi
        self.varasto_mock.saldo.side_effect = saldo

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 2, "12345", ANY, ANY)

    def test_product_can_be_removed(self):
        def saldo(tuote_id):
            if tuote_id == 1:
                return 1
        tuote = Tuote(1, "maito", 5)
        self.varasto_mock.palauta_varastoon.return_value = tuote
        self.varasto_mock.saldo.side_effect = saldo
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)
        self.varasto_mock.palauta_varastoon.assert_called_once_with(tuote)
        


        