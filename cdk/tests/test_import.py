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

        w = Headword('boltaq1 (nket.)')
        self.assertEqual(w.dialects, ['nket'])

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

        s = "kur. āb anun  мой ум, " \
            "sul. anunan kʌjga  бестолковая без ума] голова, " \
            "sur. budaŋtan anunaŋ bʌntʲaŋ  у него разума нет, " \
            "pak. abaŋta aqta anun  у меня хороший ум, " \
            "sur. āt (t)bilʲεbεt bindεp anundasʲ  я сделал своим умом, " \
            "kel. anunan kεˀt – dajεŋ kεˀt  безумец [без ума человек] – больной человек, " \
            "kel. ūk kʌjga anun u bʌnsʲaŋ  у тебя в голове ум есть или нет, " \
            "kel. anunan kεtdiŋta dɨlʲgat daʁalεjin  над безумцем потешались смеялись] дети, " \
            "kel. qɔˀk kεdda anundiŋa turʲɛ bǝ̄nʲ da-íksʲibεsʲ  одному человеку это на ум не придёт, " \
            "kur. āb anundasʲ  по моему мнению, " \
            "bak. bǝ̄nʲ āb anundas  не по своей воле  " \
            "ver. anun dʌkájnɛm  она взялась за ум (КФТ: 63), " \
            "asʲka qaɣεt datɔnɔq, anun daŋta bʌnʲsʲa ɔbɨlʲda  когда старым стал, ума у него не стало (КФТ: 29)"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 13)

        s = "kur. būŋ hʌnʲunʲaŋ  они маленькие,  " \
            "buŋnaŋa ɔnʲa sʲɨkŋ?  им сколько лет?  " \
            "būŋ “ʌtna nʲɛmsʲaŋ” ɔvɨlʲdɛn  они «нашими немцами» были (ПМБ: 252), " \
            "sʲulʲtu kàlʲ ēnʲ ɔvɨlʲdɛ  была теперь кровавая война (ПМБ: 254), " \
            "buttɔ būŋ bɛˀk bʌnʲsʲaŋ sʲɛ́ɛ̀ŋ  будто они здесь никогда не были (ПМБ: 261), " \
            "būŋ ɛk lʲʌʁɛsʲaŋ dimbɛsʲin, ʌtna qɔkŋdiŋ dimbɛsʲin tunʲɛ súran-qáŋnʲiŋ-dɛˀŋ  они пришли лишь за пушниной, в бор наш они пришли эти люди полуденных гор (ПМБ: 213), " \
            "qájɛ qálnas qíbdaŋta ʌtna dɛˀŋ dimbɛsʲin qúkdiŋ, járɔmkadiŋ būŋ dimbɛsʲin  потом в месяце сбора налога [июне] наши люди пришли на Енисей, на ярмарку они пришли (ПМБ: 214), " \
            "diˑmbɛsʲin sʲēlʲ dʌqdiŋ būŋ, diˑmbɛsʲin bənʲ áqta qá:nʲdiŋ  пришли к непристойной жизни, пришли к нехорошим словам (ПМБ: 215)"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 8)

        s = "dūɣ dɨ̄lʲ  кричащий ребёнок,  " \
            "dūɣ tʲīpʲ  лающая собака, " \
            "kel. qusʲd hɨjga dūɣ dɛˀŋ duɣan  в чуме шумные [кричащие] люди сидят, " \
            "kel. kirʲ dūɣ kɛˀt ʌɣa t-kaujak  этот шумный [кричащий] человек сюда зашёл, " \
            "kel. tūrʲ asɛsʲ dɨ̄lʲ, dɨ̄lʲ duɣsʲ  это какой ребёнок, это ребёнок шумный"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 5)

        s = "sur. bū tɔˀn d-buŋsɔʁɔ, ɛta qɔrʲa ɨ̄n saːlaŋ dugdɛ bə̄nʲ bīn tɔːlɔʁut  он так выглядит, как будто две ночи подряд не спал,  " \
            "kinij tɔˀn ā ɛta qɔrʲa sʲīl  сегодня такая жара как будто летом, " \
            "mad. bū ra-ɛsʲɔlɛj, ɛta qɔrʲa ə̄t ɔgdɛnan  она кричала, как будто мы глухие [без ушей], " \
            "mad. ū ɛta qɔrʲa bīn bə̄nʲ itkum  ты как будто сам не знаешь, " \
            "mad. ɛta qɔrʲa āt itparɛm turʲɛ bɛsʲa ɔbɨlda  кажется, я знаю это кто был, " \
            "bak. iˀlʲ qɔda kɛtda hū  песня как будто человека сердце, " \
            "bak. tɔˀn aqta dubil, qɔda kɛˀt dahudil da-kásɔnam  так хорошо поёт, как будто человека за его сердце берёт"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 7)

        s = "sul. iŋɔlt qusʲam  шкура одна, " \
            "kur. ulʲtu iŋɔlt  сырая шкура, " \
            "mad. tū iŋɔlʲta  несушёная шкура, " \
            "kur. dàŋ iŋɔlt  выделанная [мятая] шкура, " \
            "kur. hʌlat iŋɔlt  замша [ровдужная шкура], " \
            "kur. saqda iŋɔlʲt  шкура белки-самца, " \
            "mad. ɔ̀nʲ saːnna iŋɔlʲtɛŋ  много шкур белок, " \
            "kur. sεlεda iŋɔlʲt  оленья шкура, " \
            "kur. kusna iŋɔltɛŋ  коровьи шкуры, " \
            "kur. sʲīlʲ ɔllasda iŋɔltə  пыжик [шкура летнего (новорождённого) телёнка], " \
            "kur. sʲεlʲda bulʲaŋd iŋɔlt  камус [шкура с ног оленя], " \
            "sur. kulʲapda iŋɔlt  шкура горностая, " \
            "kel. tiɣda iŋɔlʲt  змеиная шкура, " \
            "pak. āt kunda iŋɔlt dʲεpqɔlʲdɔnʲ  я росомахи шкуру снял, " \
            "sur. aʲvaŋta kiˀ iŋɔltə bʌnʲsʲaŋ  у меня новой пушнины [звериных шкур] нет, " \
            "kel. ēnʲ kə̄t assanɔ kεˀt assεnna iŋɔltaŋ qɔmat diɣunbεsʲ  этой зимой охотник пушнины [звериных шкур] принёс мало " \
            "kel. qima sεlʲda iŋɔlʲt dʌvrʲaŋ  бабушка мнёт оленью шкуру, " \
            "sul. ʌlʲd iŋɔlt irʲiŋuksʲat  у лягушки шкура узорчатая, " \
            "sul. iŋɔlt(d) ʌːta āt ditaʁut  я сплю на шкуре"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 19)

        s = "mad. turʲɛ kɛˀt qɔnɔksʲ dʌqta ra-tasʲiŋavɛt  вот этот человек (женщина) утром рано [быстро] встаёт, " \
            "kel. tūrʲ kɛˀt āb ōp  этот человек мой отец, " \
            "mad. turʲɛ dɨ̄lʲ bə̄nʲ āb hɨˀp  этот ребёнок не мой сын, " \
            "mad. turʲɛ kɛrʲa lə̄q  этого человека пушнина, " \
            "bak. ū baˀt tudɛ bə̄nʲ (k)tɔbinʲgij  ты правда это не говорил, " \
            "mad. turɛdiŋa ōksʲ hʌninsʲa ɔvílda  у этого (капкана) палка маленькая была, " \
            "mad. tūrʲɔ qɔtá najarij  вот он [тот] впереди шевелится, " \
            "kel. turʲɛ bə̄nʲ ʌtna kuˀsʲ  это не наша корова, " \
            "kel. turʲɛ aksʲ tunbisʲ? – qīmd súùlʲ, tū sʲuːʲlʲd ʌ́ʌ̀t qimn (t)tɔlʲaŋɢɔtin  это что такое? – женская нарта, на такой нарте женщины ездят, " \
            "kel. tū bitsʲɛ?  это кто (о мужчине)? " \
            "kel. tū tɔˀn tɨŋalʲam  вот настолько высоко, " \
            "kel. turʲɛ tavut, ūk ɨlʲɣa, bə̄nʲ kutɔŋ  это лежит, возле тебя, не видишь, " \
            "kel. tunɛ dɛˀŋ inʲam dɔlʲdɛɣin  эти люди давно жили, " \
            "kel. tunɛ dɛˀŋ utisʲ dɛˀŋ  эти люди родственники, " \
            "kel. tū kʌnʲdaŋ dεˀŋ dεˀŋ (d)pɔsɔbarɔŋɔbεtin  эти добрые люди людям помогают, " \
            "kel. hɨlʲ turɔ́  вон он! " \
            "kel. hɨlʲ tunɛ dɛˀŋ araŋɔt  эти вот люди болеют  " \
            "sur. tuda īsʲ nado toʁajaŋɢat  эту рыбу сушить надо (ЛЯНС41: 250), " \
            "pak. usʲka diːnbɛs, (d)buŋsɔʁɔ – tudʌ buŋna kaˀt baŋŋusʲ hapta, tudʌ kaˀt sɨˀk  домой (он) пришёл, смотрит – это их старая землянка стоит, это старое корыто (КФТ: 19)"
        l = list(yield_examples(s))
        #for ll in l:
        #    print('%s %s %s %s %s' % tuple(ll))
        self.assertEqual(len(l), 19)

        s = "danʲáptɛt  я строгаю это,  danʲabílʲtɛt  я строгал это "
        l = list(yield_examples(s))
        self.assertEqual(len(l), 2)

        s = "kel. qīp thitlut iʁɔt dahɔ́lɛtɛsʲ  месяц сел, солнце встало  " \
            "sket. qīp thitsut [thitsuʁut]  луна заходит (WER1: 317), " \
            "cket., nket. thɛtsɔʁɔt  он заходит (1b : 28) (WER1: 317), " \
            "sket. ī dahitsut [dahitsuʁut]  солнце заходит (WER1: 317), " \
            "cket., nket. dahɛ́tsɔʁɔt она заходит (WER1: 317), " \
            "diˑmbɛsʲin bīk dɛˀŋ hāj biksʲa, itlʲan baŋdiŋalʲ dimbɛsʲin, ī dahítsut baŋdiŋalʲ  пришли чужие люди снова, из неведомой страны пришли, из страны, в которой солнце заходит (ПМБ: 214)"
        l = list(yield_examples(s))
        self.assertEqual(set(o[0] for o in l if o[0] is not None), {'kel', 'sket', 'cket', 'nket'})

        s = "kel. buŋtɛt kɛˀt sʲēlʲ bilbɛt  глупый человек плохо сделал, " \
            "kel. buŋtɛt hīɣ ʌtna tān dɛjsɔʁɔt  дурной мужик на нас ругается, " \
            "kel. ʌtna kɛˀt buŋtɛtsʲ  наш человек чокнутый [глупый]  " \
            "manʲmaŋ, ə̄tn darʲij dɛˀŋ, buttɔ ə̄tn buŋtɛt dɛˀŋ  говорят, мы дураки, будто мы глупые люди (ПМБ: 261), " \
            "haj at anʲɛŋilʲgɛt tɔˀnʲ, butta bʌˀj kʌˀ-qɔlʲɛpkaru uɣil sʲɛlʲdu, buŋtɛtdu  и не думай так, будто друг там за рекой тебя хуже, глупей (ПМБ: 230)"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 5)

        s = "bū qusʲ-t hìj dujutɔ  он чум ставить собирается,  " \
            "bū quˀsʲ kisʲɛ̀ŋ hij-εsʲaŋ dutabak  он чум здесь ставить собирается,  " \
            "quˀsʲ kisʲɛ́ŋ hij-εsʲaŋ daqɔˀj  он чум здесь ставить хочет  " \
            "hij-ɛsʲaŋ quˀŋ nada qajga  чумы надо ставить на яру (ПМБ: 203)"
        l = list(yield_examples(s))
        self.assertEqual(len(l), 4)

        s = "bak. qūsʲ ē  одно железо, " \
            "kur. tarɛ ē  кованое [битое] железо, " \
            "sul. áàŋ ē  горячее железо, " \
            "sul. ē aːŋam  железо горячее, " \
            "kel. turʲə ē aːŋsʲ  это железо горячее, " \
            "sul. kɨlʲtɛt ē  кованое железо, " \
            "sul. ē kɨltɛts  железо кованное, " \
            "bak. kɔlɛtdiŋta tʌŋdiŋal, ēdiŋal ɛŋŋuŋ dεˀŋ dubbɛtin  в городе из камня, из железа дома люди делают  " \
            "hʌtnuraŋdiŋt ē dusʲqimnʲan  в плавильнях железо выплавляли (ПМБ: 243), " \
            "āt huːlasʲ (t)kɨlʲdavintɛt aʁatld ʌʁat ē  я железо молотком кую [бью] на наковальне (СНСС72: 126), " \
            "pak. ɛd dūɣ  стрельба [крик железа] "
        l = list(yield_examples(s))
        #for ll in l:
        #    print('%s | %s | %s | %s | %s' % tuple(ll))
        self.assertEqual(len(l), 11)

        s = "sul. qūsʲ asʲpulʲ  одно облако, " \
            "sul. asʲvulʲ qusʲam  облако одно, " \
            "sur. ulʲεsʲ aspulʲ  дождевое облако, " \
            "el. tum aspulʲ  чёрная туча, " \
            "kur. quŋtεt aspulʲ  грозовая туча, " \
            "kur. ēkŋ asʲpul εsavut  грозовая туча поднимается, " \
            "kel. āt asʲbulʲ ditɔŋ  я тучу вижу, " \
            "sul. aspulaŋ bʌnsʲaŋ  туч нет, " \
            "sul. asʲpulʲdiŋalʲ ulʲata  из тучи дождь идёт, " \
            "kel. ulʲɛsʲ aspulʲ arʲɛn tɔsa qɔlʲapka aŋapta  дождевое облако над лесом висит, " \
            "bak. hʌlatbεsʲ aspulaŋ ɔŋɔt  по небу облака идут, " \
            "kel. asʲpulʲ bēj da-bugbit  облако ветром несёт, " \
            "kel. qimdɨlʲ aspul da-kɔlʲdɔ  девочка на облако смотрела, " \
            "kel. tum asʲpulʲ ʌɣa bēj da-bugbiʁɔs  чёрное облако ветер сюда несёт  " \
            "ēkŋ qām duɣaŋgɔʁan, qat qarʲuːn, aspulʲaŋ utal ēsʲ (t)kajnamin  гроза скоро начнется, посмотрите, тучи обложили всё небо (СНСС72: 147), " \
            "quŋlɔɣin ʌla, aksʲ ǝ̄k bǝ̄nʲ kutɔɣin ulεstu aspulʲ?  посмотрите наружу, разве вы не видите грозовую тучу? (СНСС72: 151)"
        l = list(yield_examples(s))
        #for ll in l:
        #    print('%s | %s | %s | %s | %s' % tuple(ll))
        self.assertEqual(len(l), 16)

        s = "sur. ūk inεŋ  твои ногти, " \
            "kel. qūsʲ ìn  один ноготь, " \
            "kel. ìn qusʲam  ноготь один, " \
            "sul. qaɣam inεŋ  пять ногтей, " \
            "sul. ìn sintuɣam  ноготь грязный, " \
            "kur. kεdda ìn  ноготь человека, " \
            "kur. tabna inεŋ  когти собак, " \
            "kur. sutaqd ìn  ноготь среднего пальца, " \
            "kur. qɔjda inεŋ  когти медведя, " \
            "kel. hɨˀj inεŋasʲ ùt (t)tɔɣaulʲtεt  сова схватила мышь когтями,  " \
            "bū kɔˀp (t)kasʲɔnεm, daqɔbεtbεsʲ dεtavinʲtaŋ; kɔbda qɔbεtka qɔjda inεŋdiŋalʲ qāk tumaŋ (s)lεːdaŋ igdɔbɔn  он бурундука взял, по спине погладил; от медвежьих когтей на спине бурундука пять чёрных полос [следов] осталось (СНСС81: 57), " \
            "inεŋ àj  небольшая сумочка из шкурок с лап соболя, выдры, росомахи [когти сумка] (К67: 117)"
        l = list(yield_examples(s))
        #for ll in l:
        #    print('%s | %s | %s | %s | %s' % tuple(ll))
        self.assertEqual(len(l), 12)

        s = "kel. abcd?  efgh? kel. ijkl  mnop"
        l = list(yield_examples(s))
        self.assertEqual(l[0][2], 'efgh?')
        self.assertEqual(l[1][2], 'mnop')

        s = "kel. hīɣ qɔˀk duɣaraq  мужик один живёт, " \
            "kel. bū qɔˀk kɛˀt, ariŋa duɣaraq  он один [один человек], в лесу живёт,  " \
            "qɔˀk huˀn  одна дочь (СНСС72: 83), " \
            "qɔksʲadaŋtɛn ɨ̄n kʌˀt  у одного (человека) двое детей (СНСС72: 83), " \
            "qɔkdadiŋtan dɔˀŋ dɨlʲgat, kunsʲa qimdiŋtan qɔˀk dɨ̄lʲ  у одной было трое детей, у другой женщины один ребёнок (СНСС81: 40), " \
            "qɔˀk qīm qā daigdɔʁɔn  одна баба дома осталась (СНСС72: 139), " \
            "āt qɔˀk kɛˀt digdɔʁɔn  я одна осталась (СНСС72: 107), " \
            "qɔˀk ɔstɨk i qɔˀk hʌmga  один кет и один эвенк (CHCC81ː 44), " \
            "pak. qɔˀk saˀq bīk ɔksʲdaŋa da-ɛtʲditnam  другая [одна] белка соскочила на другое дерево (КФТ: 55)"
        l = list(yield_examples(s))
        #for ll in l:
        #    print('%s | %s | %s | %s | %s' % tuple(ll))
        #
        # FIXME: incorrect parsing of
        # qɔˀk ɔstɨk i qɔˀk hʌmga  один кет и один эвенк (CHCC81ː 44)
        #
        self.assertEqual(len(l), 9)

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
