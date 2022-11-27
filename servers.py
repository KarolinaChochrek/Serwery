#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from abc import ABC, abstractmethod
from copy import deepcopy
from re import match
from typing import List




class Product:

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def  __init__(self, nazwa_produktu, cena_produktu):
        if not isinstance(nazwa_produktu, str):
            raise ValueError("Typ danych nie jest typu string")
        if type(cena_produktu) not in [float,int]:
            raise ValueError("Nie jest typu float")
        if match("""^[a-zA-Z]+\d+$""", nazwa_produktu) is None:
            raise ValueError("Nazwa w złej postaci")

        self.name = nazwa_produktu
        self.price = cena_produktu

    def __eq__(self, other):
        if self.price == other.price and self.name == other.name:
            return True  # FIXME: zwróć odpowiednią wartość
        else:
            return False

    def __hash__(self):
        return hash((self.name, self.price))

class TooManyProductsFoundError(BaseException):

    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, wiadomosc = None):
        if wiadomosc is None:
            wiadomosc = "Liczba znalezionych produktów wykracza poza max wartość "
        super().__init__(wiadomosc)



# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Serwer(ABC):
    @abstractmethod
    def __init__(self, lista_produktow: List[Product]):
        raise NotImplementedError

    # metoda realizowana przez ListServer i MapServer
    @abstractmethod
    def get_entries(self, n_letters = 1):
        raise NotImplementedError

    # wybrana liczba z przedziału od 3 do 7
    n_max_returned_entries = 4

class ListServer(Serwer):
    def __init__(self, lista_produktow: List[Product]):
        self.products = deepcopy(lista_produktow)

    def get_entries(self, n_letters = 1 ):
        pasujace_produkty = []
        for prod in self.products:
            if match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), prod.name) is not None:
                pasujace_produkty.append(prod)
        if len(pasujace_produkty) > Serwer.n_max_returned_entries:
            raise TooManyProductsFoundError("Za duzo produktów")
        return sorted(pasujace_produkty, key=lambda produkt: produkt.price)

class MapServer(Serwer):
    def __init__(self, lista_produktow: List[Product]):
        self.products = {}
        for prod in lista_produktow:
            self.products[prod.name] = deepcopy(prod)

    def get_entries(self, n_letters=1):
        pasujace_produkty = []
        for prod in self.products.values():
            if match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), prod.name) is not None:
                pasujace_produkty.append(prod)
        if len(pasujace_produkty) > Serwer.n_max_returned_entries:
            raise TooManyProductsFoundError("Za duzo produktów")
        return sorted(pasujace_produkty, key=lambda produkt: produkt.price)


class Client:

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Serwer):
        self.server = server

    def get_total_price(self, n_letters: Optional[int] =1 ) -> Optional[float]:
        try:
            lista_posort = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        else:
            cena = 0
            for i in lista_posort:
                cena += i.price
            if cena == 0:
                return None
            else:
                return cena





