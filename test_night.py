import night
import unittest
from statement import *
from player import *
from role import *

amelia = Player('A')
bob = Player('B')
chad = Player('C')
dan = Player('D')
eno = Player('E')
c1 = Center(1)
c2 = Center(2)
c3 = Center(3)

DEFAULT_PLAYERS = [amelia, bob, chad, dan, eno,
                   c1, c2, c3]

DEFAULT_ROLES = [Role(VILLAGER),
                 Role(VILLAGER),
                 Role(WEREWOLF),
                 Role(WEREWOLF),
                 Role(TROUBLEMAKER),
                 Role(ROBBER),
                 Role(SEER)]


class TestNight(unittest.TestCase):
    def test_can_add_start_role(self):
        r = Role(VILLAGER)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        s = Original(amelia, r)
        self.assertTrue(n.incorporate(s))
        self.assertEqual(n.originals.get(amelia), r)
        self.assertTrue(n.is_consistent(s))
        s2 = Original(amelia, Role(WEREWOLF))
        self.assertFalse(n.is_consistent(s2))

    def test_can_add_multiple_start_roles(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        s1 = Original(amelia, Role(VILLAGER))
        s2 = Original(bob, Role(WEREWOLF))
        s3 = Original(chad, Role(TROUBLEMAKER))
        s4 = Original(dan, Role(SEER))
        s5 = Original(eno, Role(ROBBER))
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))
        self.assertTrue(n.incorporate(s3))
        self.assertTrue(n.incorporate(s4))
        self.assertTrue(n.incorporate(s5))

    def test_can_add_final_role(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(VILLAGER)
        s = Final(amelia, r)
        self.assertTrue(n.incorporate(s))
        self.assertEqual(n.finals.get(amelia), r)

    def test_can_add_start_and_final(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(VILLAGER)
        s1 = Original(amelia, r)
        s2 = Final(amelia, r)
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))

    def test_can_add_different_start_and_final(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        s1 = Original(amelia, Role(VILLAGER))
        s2 = Final(amelia, Role(WEREWOLF))
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))

    def test_more_than_one_role(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(ROBBER)
        s1 = Final(amelia, r)
        s2 = Final(dan, r)
        self.assertTrue(n.incorporate(s1))
        self.assertFalse(n.incorporate(s2))

    def test_too_many_roles(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(VILLAGER)
        s1 = Final(amelia, r)
        s2 = Final(dan, r)
        s3 = Final(bob, r)
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))
        self.assertFalse(n.incorporate(s3))

    def test_swapper_must_exist(self):
        s = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        self.assertFalse(n.incorporate(s))

    def test_empty_swap(self):
        t = Original(dan, Role(TROUBLEMAKER))
        s = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(s))

    def test_swap(self):
        t = Original(dan, Role(TROUBLEMAKER))
        v = Original(amelia, Role(VILLAGER))
        w = Original(bob, Role(WEREWOLF))
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(w))
        self.assertTrue(n.incorporate(swap))

    def test_unfinished_swap(self):
        t = Original(dan, Role(TROUBLEMAKER))
        v = Original(amelia, Role(VILLAGER))
        w = Final(bob, Role(WEREWOLF))
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(w))
        self.assertTrue(n.incorporate(swap))

    def test_lying_swap(self):
        t = Original(dan, Role(TROUBLEMAKER))
        v = Original(amelia, Role(VILLAGER))
        w = Final(bob, Role(WEREWOLF))
        c = Original(c1, Role(ROBBER))
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(c))
        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(w))
        self.assertFalse(n.incorporate(swap))

    def test_verified_swap(self):
        t = Original(dan, Role(TROUBLEMAKER))
        v = Original(amelia, Role(VILLAGER))
        v2 = Final(amelia, Role(WEREWOLF))
        w = Original(bob, Role(WEREWOLF))
        w2 = Final(bob, Role(VILLAGER))
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(v2))
        self.assertTrue(n.incorporate(w))
        self.assertTrue(n.incorporate(w2))
        self.assertTrue(n.incorporate(swap))

if __name__ == '__main__':
    unittest.main()
