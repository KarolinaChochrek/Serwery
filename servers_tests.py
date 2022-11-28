import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('PP233', 3), Product('PP234', 2), Product('PP236', 5), Product('PP12', 4)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[1], products[0], products[3], products[2]]), Counter(entries))

    def test_get_entries_raises_exception(self):
        prod = [Product('xd23', 2), Product('xd24', 3), Product('xd27', 3), Product('wo43', 2), Product('he53', 2)]
        for server_type in server_types:
            server = server_type(prod)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)


class ClientTest(unittest.TestCase):

    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_exeption(self):
        prod = [Product('PP234', 2), Product('PP235', 3), Product('PP231', 2), Product('PP243', 2), Product('WO56', 3)]
        for server_type in server_types:
            server = server_type(prod)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_no_prod(self):
        prod = [Product('nie90', 2)]
        for server_type in server_types:
            server = server_type(prod)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()
