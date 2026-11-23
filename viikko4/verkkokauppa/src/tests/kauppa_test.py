import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_added_product_that_in_storage__buy_with_right_values(self):
        varasto_mock= Mock()
        varasto_mock.saldo.return_value = 1
        varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")
        pankki_mock.tilisiirto.assert_called_once_with("pekka", ANY, "12345", ANY, 5)

    def test_added_two_products_that_in_storage__buy_with_right_values(self):
            varasto_mock= Mock()
            def saldo(tuote_id):
                if tuote_id == 1:
                    return 1
                if tuote_id == 2:
                    return 2

            def hae_tuote(tuote_id):
                if tuote_id == 1:
                    return Tuote(1, "maito", 5)
                if tuote_id == 2:
                    return Tuote(2, "suklaa", 10)
                
            varasto_mock.saldo.side_effect = saldo
            varasto_mock.hae_tuote.side_effect = hae_tuote
            pankki_mock = Mock()
            viitegeneraattori_mock = Mock()
        
            kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
            kauppa.aloita_asiointi()
            kauppa.lisaa_koriin(1)
            kauppa.lisaa_koriin(2)
            kauppa.tilimaksu("jenna", "123456")
            pankki_mock.tilisiirto.assert_called_once_with("jenna", ANY, "123456", ANY, 15)


    def test_added_two_same_products_that_in_storage__buy_with_right_values(self):
                varasto_mock= Mock()
                def saldo(tuote_id):
                    if tuote_id == 1:
                        saldo.count = saldo.count - 1
                        return saldo.count + 1
                saldo.count = 2
    
                def hae_tuote(tuote_id):
                    if tuote_id == 1:
                        return Tuote(1, "maito", 5)

                varasto_mock.saldo.side_effect = saldo
                varasto_mock.hae_tuote.side_effect = hae_tuote
                pankki_mock = Mock()
                viitegeneraattori_mock = Mock()
            
                kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
                kauppa.aloita_asiointi()
                kauppa.lisaa_koriin(1)
                kauppa.lisaa_koriin(1)
                kauppa.tilimaksu("jenna", "123456")
                pankki_mock.tilisiirto.assert_called_once_with("jenna", ANY, "123456", ANY, 10)
    
    def test_added_two_products_but_second_not_in_storage__buy_with_right_values(self):
                varasto_mock= Mock()
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

                varasto_mock.saldo.side_effect = saldo
                varasto_mock.hae_tuote.side_effect = hae_tuote
                pankki_mock = Mock()
                viitegeneraattori_mock = Mock()
            
                kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
                kauppa.aloita_asiointi()
                kauppa.lisaa_koriin(1)
                kauppa.lisaa_koriin(2)
                kauppa.tilimaksu("jenna", "123456")
                pankki_mock.tilisiirto.assert_called_once_with("jenna", ANY, "123456", ANY, 5)
    
        