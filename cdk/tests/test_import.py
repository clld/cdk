# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from cdk.scripts.util import Headword


class HeadwordTests(TestCase):
    def test_Headword(self):
        w = Headword('ambel <rus.>')
        self.assertEqual(w.donor, 'rus')
        w = Headword('anát-qodes (nket., sket. anát-qɔrεs, cket. anát-qɔdεs)')
        self.assertEqual(w.form, 'anát-qodes')
        self.assertEqual(w.dialects[0], 'nket')
        self.assertIn('sket', w.variants)
        w = Headword('aduŋu I (nket. aruŋ, cket. aduŋu, sket. aruŋu)')
        self.assertEqual(w.disambiguation, 'I')
        w = Headword('albed1 (cket. alʲəbɛt) III')
        self.assertEqual(w.dialects, [])
        self.assertIn('cket', w.variants)
        self.assertEqual(w.disambiguation, '1 III')
        w = Headword('albed also something also else (cket. alʲəbɛt)')
        self.assertEqual(len(w.variants[None]), 2)
