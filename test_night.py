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
        s = RoleClaim(amelia, r, ORIGINAL)
        self.assertTrue(n.incorporate(s))
        self.assertEqual(n.assignments[ORIGINAL].get(amelia), r)
        self.assertTrue(n.is_consistent(s))
        s2 = RoleClaim(amelia, Role(WEREWOLF), ORIGINAL)
        self.assertFalse(n.is_consistent(s2))

    def test_can_add_multiple_start_roles(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        s1 = RoleClaim(amelia, Role(VILLAGER), ORIGINAL)
        s2 = RoleClaim(bob, Role(WEREWOLF), ORIGINAL)
        s3 = RoleClaim(chad, Role(TROUBLEMAKER), ORIGINAL)
        s4 = RoleClaim(dan, Role(SEER), ORIGINAL)
        s5 = RoleClaim(eno, Role(ROBBER), ORIGINAL)
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))
        self.assertTrue(n.incorporate(s3))
        self.assertTrue(n.incorporate(s4))
        self.assertTrue(n.incorporate(s5))

    def test_can_add_final_role(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(VILLAGER)
        s = RoleClaim(amelia, r, FINAL)
        self.assertTrue(n.incorporate(s))
        self.assertEqual(n.assignments[FINAL].get(amelia), r)

    def test_can_add_start_and_final(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(VILLAGER)
        s1 = RoleClaim(amelia, r, ORIGINAL)
        s2 = RoleClaim(amelia, r, FINAL)
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))

    def test_can_add_different_start_and_final(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        s1 = RoleClaim(amelia, Role(VILLAGER), ORIGINAL)
        s2 = RoleClaim(amelia, Role(WEREWOLF), FINAL)
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))

    def test_more_than_one_role(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(ROBBER)
        s1 = RoleClaim(amelia, r, FINAL)
        s2 = RoleClaim(dan, r, FINAL)
        self.assertTrue(n.incorporate(s1))
        self.assertFalse(n.incorporate(s2))

    def test_too_many_roles(self):
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        r = Role(VILLAGER)
        s1 = RoleClaim(amelia, r, FINAL)
        s2 = RoleClaim(dan, r, FINAL)
        s3 = RoleClaim(bob, r, FINAL)
        self.assertTrue(n.incorporate(s1))
        self.assertTrue(n.incorporate(s2))
        self.assertFalse(n.incorporate(s3))

    def test_swapper_must_exist(self):
        s = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)
        self.assertFalse(n.incorporate(s))

    def test_empty_swap(self):
        t = RoleClaim(dan, Role(TROUBLEMAKER), ORIGINAL)
        s = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(s))

    def test_swap(self):
        t = RoleClaim(dan, Role(TROUBLEMAKER), ORIGINAL)
        v = RoleClaim(amelia, Role(VILLAGER), ORIGINAL)
        w = RoleClaim(bob, Role(WEREWOLF), ORIGINAL)
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(w))
        self.assertTrue(n.incorporate(swap))

    def test_unfinished_swap(self):
        t = RoleClaim(dan, Role(TROUBLEMAKER), ORIGINAL)
        v = RoleClaim(amelia, Role(VILLAGER), ORIGINAL)
        w = RoleClaim(bob, Role(WEREWOLF), FINAL)
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(w))
        self.assertTrue(n.incorporate(swap))

    def test_lying_swap(self):
        t = RoleClaim(dan, Role(TROUBLEMAKER), ORIGINAL)
        v = RoleClaim(amelia, Role(VILLAGER), ORIGINAL)
        w = RoleClaim(bob, Role(WEREWOLF), FINAL)
        c = RoleClaim(c1, Role(ROBBER), ORIGINAL)
        swap = Swap(Role(TROUBLEMAKER), amelia, bob)
        n = night.Night(DEFAULT_ROLES, DEFAULT_PLAYERS)

        self.assertTrue(n.incorporate(c))
        self.assertTrue(n.incorporate(t))
        self.assertTrue(n.incorporate(v))
        self.assertTrue(n.incorporate(w))
        self.assertFalse(n.incorporate(swap))

    def test_verified_swap(self):
        t = RoleClaim(dan, Role(TROUBLEMAKER), ORIGINAL)
        v = RoleClaim(amelia, Role(VILLAGER), ORIGINAL)
        v2 = RoleClaim(amelia, Role(WEREWOLF), FINAL)
        w = RoleClaim(bob, Role(WEREWOLF), ORIGINAL)
        w2 = RoleClaim(bob, Role(VILLAGER), FINAL)
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
