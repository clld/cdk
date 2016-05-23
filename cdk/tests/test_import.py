# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from cdk.scripts.util import Headword, yield_variants, yield_examples


class HeadwordTests(TestCase):
    def test_Headword(self):
        w = Headword('ambel <rus.>')
        self.assertEqual(w.donor, 'rus')
        w = Headword('anát-qodes (nket., sket. anát-qɔrεs, cket. anát-qɔdεs)')
        self.assertEqual(w.form, 'anát-qodes')
        self.assertEqual(w.dialects, [])
        self.assertIn('sket', w.variants)
        w = Headword('aduŋu I (nket. aruŋ, cket. aduŋu, sket. aruŋu)')
        self.assertEqual(w.disambiguation, 'I')
        w = Headword('albed1 (cket. alʲəbɛt) III')
        self.assertEqual(w.dialects, [])
        self.assertIn('cket', w.variants)
        self.assertEqual(w.disambiguation, '1 III')
        w = Headword('albed also something also else (cket. alʲəbɛt)')
        self.assertEqual(len(w.variants[None]), 2)

        w = Headword('estij (cket. ε(j)štij) I')
        self.assertEqual(w.variants['cket'], ['ε(j)štij'])

    def test_examples(self):
        s = "kel. kinij aqta ā  сегодня сильная жара, kel. sʲīlʲɛ ā  летом жара, kel. " \
            "ugbinut adiŋalʲ  потеряла сознание от жары, bak. ā baŋga dɨnlitdiŋta ɛnam" \
            "  во время жары в еловом лесу прохладно  kinij qɔŋa qà ā, kεˀt bǝ̄nʲ " \
            "dilsivɛt  cегодня невыносимая жара и духота, человек не вздохнёт (КФТ: 82) "
        l = list(yield_examples(s))
        self.assertEqual(set(o[0] for o in l if o[0] is not None), {'kel', 'bak'})
        self.assertEqual(l[-1][3], 'КФТ')
        self.assertEqual(l[-1][4], '82')
        self.assertEqual(l[-1][2], 'cегодня невыносимая жара и духота, человек не вздохнёт')

        s = "sur. bāt aːtɔʁɔn, dēsʲ ā rʲa-haqtɔlʲaŋ  лоб вспотел, глаза пот ослепил," \
            " sul. adiŋta kʌma hʌˀq tabdaq  в поту (их шерсть) преет [выпадает], kel." \
            " bū ā aːtɔʁɔn-qɔn (t)lɔvεrɔlʲbεt  он до пота [пока пот не пошёл] работал" \
            "  tɨvak bʌjbulʲ āt indaq, āt ā kʌma dabbεt  пучок [косичку] стружки дай" \
            " мне, я пот вытру (СНСС76: 11), sur. ā atpadaq batatdiŋɛl  пот льёт с" \
            " лица (ЛЯНС11: 456) "
        l = list(yield_examples(s))
        self.assertEqual(set(o[3] for o in l if o[3] is not None), {'СНСС76', 'ЛЯНС11'})

        s = "sur. kinij ā iˀ  сегодня жаркий день, sul. εnqɔŋ iˀ atusʲ  сегодня день " \
            "жаркий  qasέŋ aqtam, ʌtnnaŋta qasέŋ aɣam, ūlʲ aːŋam  там хорошо, у нас " \
            "там жарко, вода тёплая (СНСС81: 52)"
        l = list(yield_examples(s))

        s = "kel. abεskij dɛˀŋ ɔna diːmεsin  блуждающие [заблудившиеся] люди только " \
            "пришли, kel. āt abεskij sɛ̀lʲ dɔːnbʌk  я заблудившегося оленя нашёл  " \
            "sul. abɛskij kʲεˀt  заблудившийся человек (АК1: 12б)"
        l = list(yield_examples(s))
        self.assertEqual(set(o[0] for o in l if o[0] is not None), {'kel', 'sul'})
        self.assertEqual(set(o[3] for o in l if o[3] is not None), {'АК1'})

        s = "kel. āt utpaɣan  я слепая, " \
            "kel. āt dassanɔɣavεt  я охочусь, " \
            "kel. abaŋa ɨ̄nʲ qimdɨlʲgat  у меня двое девочек, " \
            "kel. ukuŋa aslɛnaŋ usʲaŋ? – abaŋa usʲaŋ, aqta aslɛnaŋ  у тебя лодка есть? – у меня есть, хорошая лодка, " \
            "bak. abaŋa aqtam, ǝ̄k kiːnbεsʲin  мне хорошо, (что) вы пришли, " \
            "kur. ūlʲ abaŋa bǝ̄nʲ (k)qʌtsʲigɛt?  воды мне не дашь? " \
            "kur. āb bisʲɛp abaŋa qānʲ durɔq  мой брат ко мне пусть прилетит, " \
            "kel. abaŋa ana nara?  мне кто нужен? pak. idiŋ abaŋa bʌnʲsʲaŋ daŋal  писем мне нет от него, " \
            "kur. abaŋta kʌˀt usʲaŋ  у меня дети есть, " \
            "kur. abaŋta dɔˀŋ hunʲaŋ ovɨlda  у меня три дочери было, " \
            "kur. āt (t)kajnam hɔlaq, patrɔ́naŋ abaŋta usʲaŋ  я взял порох, патроны у меня есть, " \
            "bak. lɔbɛt abaŋta baˀt ɔnʲaŋ  работы у меня, правда, много, " \
            "bak. abaŋta tʌˀ kɔbda-qɔ  у меня соли пригоршня, " \
            "pak. abaŋta ɔbɨlʲda qīp  у меня был дед, " \
            "kel. abaŋta qɔˀk huˀnʲ  у меня одна дочь, " \
            "pak. tīp abaŋta diːmbεsʲ  собака ко мне пришла, " \
            "kur. abaŋal dɔˀŋ dɨlʲgat  от меня трое детей, " \
            "sul. āb bisʲɛp abaŋal aqtarʲa  моя сестра меня лучше, " \
            "bak. ə̄k abat (k)sʲaŋsiɣɛtin?  вы меня ищете? " \
            "kur. hissɛj abat iʁusʲ  лес для меня дом, " \
            "sur. diːmbεsʲ adas  он пришёл со мной"
        l = list(yield_examples(s))

        s = "sul. āb arʲεŋ  мои кости, " \
            "pak. qūsʲ aˀt  одна кость, " \
            "kel. aˀt qusʲam  кость одна, " \
            "pak. qāk adεŋ  пять костей, " \
            "kel. qà aˀt  большая кость, " \
            "kel. aˀt qàsʲ  кость большая, " \
            "kel. ilʲiŋ aˀt  обглоданная кость, " \
            "leb. aˀt ilʲ  кость грызи, " \
            "kur. qɔbɛt aˀt  спинной хребет [кость], " \
            "kur. bɔŋda arεŋ  мертвеца скелет [кости], " \
            "kel. hʌŋnd aˀt  плечевой сустав [плеча кость], " \
            "kel. ɨlʲgat(d) aˀt  ключица, " \
            "sul. ɔkdaŋtan arʲεŋ bʌnsʲa  у стерляди костей нет, " \
            "kel. āt ulʲbaɣɔlʲta, barεŋ binʲtʌːlʲ  я промок под дождем, промёрз до костей [кости мои замерзли], " \
            "sur. būŋ tusʲaŋ dʌʁaŋgɔʁɔn buŋna dεŋna adεŋdiŋta  они там жить стали, где кости их людей  " \
            "sʲī haj aɣa ɔɣɔn, daɔbda adεŋdiŋa haj (t)tɔlatn  ночью он снова на гору [вверх на берег в лес] ушёл, на кладбище [к костям] своего отца, снова лёг (КСД: 35)"
        l = list(yield_examples(s))

        s = "аl. buda aˀt  его рост, " \
            "pak. báàt bǝ̄nʲ qà aˀt  старик небольшого роста, " \
            "mad. tur báàt tɨŋalʲ aˀt  этот старик высокого роста, " \
            "kur. tur báàt bǝ̄nʲ ugda aˀt  этот старик небольшого [не длинного] роста, " \
            "kur. bū sʲutn aˀt  он среднего роста, " \
            "kur. bū hʌna aˀt  он маленького роста, " \
            "sur. εjɣε bɔŋsʲúːlʲ (t)biːlεbεt bind atdas  он железный гроб [мертвячью нарту] сделал в свой рост"
        l = list(yield_examples(s))

        s = "dɔlʲdin vasʲka qimas àl sɛnnusʲdiŋta  жили Васька с женой в лесу в оленьем сарае (КФТ: 29) " \
            "dɔlʲdin vasʲka qimas àl sɛnnusʲdiŋta  жили Васька с женой в лесу в оленьем сарае (КФТ: 29),  " \
            "sur. lɛska àl tam ana qɛ̀ dɛːsij, dɛˀŋ aŋgábdǝ  в лесу кто-то громким голосом кричит, люди услыхали (ЛЯНС11: 154)"
        l = list(yield_examples(s))
        self.assertEqual(set(o[0] for o in l if o[0] is not None), {'sur'})
        self.assertEqual(set(o[3] for o in l if o[3] is not None), {'КФТ', 'ЛЯНС11'})

        s = "kel. tɨˀn àl usʲna  котёл прочь сними (с огня), " \
            "kel. àl εsʲandaq  подальше положи, " \
            "kel. àl εsʲandaq, qɨ̄nʲ aqán da-bugbiʁus  положи подальше, течение чтобы не унесло [пусть не унесет] " \
            "imb. àl da-quska da-qimn sɛtɔŋna  а там в чуме его жены узнали (КСб: 181)"
        l = list(yield_examples(s))

    def test_variants(self):
        l = list(yield_variants('sket.'))
        self.assertEqual(l, [('sket', None)])

        l = list(yield_variants('sket., nket.'))
        self.assertEqual(l, [('sket', None), ('nket', None)])

        l = list(yield_variants('sket. abc, nket. def'))
        self.assertEqual(l, [('sket', 'abc'), ('nket', 'def')])

        l = list(yield_variants('sket., nket. abc, cket. def'))
        self.assertEqual(l, [('sket', 'abc'), ('nket', 'abc'), ('cket', 'def')])

        l = list(yield_variants('nket. a, cket. b, c'))
        self.assertEqual(l, [('nket', 'a'), ('cket', 'b'), ('cket', 'c')])

        l = list(yield_variants('nket. a, sket., cket. b, c'))
        self.assertEqual(l, [('nket', 'a'), ('sket', 'b'), ('cket', 'b'), ('sket', 'c'), ('cket', 'c')])
