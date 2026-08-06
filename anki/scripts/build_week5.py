#!/usr/bin/env python3
"""Build Week 5 Anki TSV/apkg files (Deck 1 Vocabulary, Deck 2 Grammar & Usage).

Follows specs/anki-tsv-generation-process.md, specs/anki-note-type-vocabulary.md,
specs/anki-note-type-grammar-and-usage.md. Run from repo root:

    .venv/bin/python anki/scripts/build_week5.py
"""
import genanki
import hashlib
import re

def stable_id(name):
    h = hashlib.sha256(name.encode('utf-8')).hexdigest()
    return int(h[:9], 16) % 1_000_000_000 + 1_000_000_000

DECK1_ID = 1265466646   # Japanese N2 Vocabulary
MODEL1_ID = 1074616827  # Japanese vocabulary
DECK2_ID = 1226860726   # Japanese N2 Grammar & Usage
MODEL2_ID = 1742781826  # Japanese grammar and usage

assert stable_id("Japanese N2 Vocabulary") == DECK1_ID
assert stable_id("Japanese vocabulary") == MODEL1_ID
assert stable_id("Japanese N2 Grammar & Usage") == DECK2_ID
assert stable_id("Japanese grammar and usage") == MODEL2_ID

vocab_cards = []   # list of dict(word, reading, meaning, sentence, sreading, strans, tags)
grammar_cards = [] # list of dict(front_main, reading, meaning_class, meaning, sentences=[(jp,reading,en),...], tags)


def V(word, reading, meaning, sentence, sreading, strans, tags):
    vocab_cards.append(dict(word=word, reading=reading, meaning=meaning,
                             sentence=sentence, sreading=sreading, strans=strans, tags=tags))


def G(front_main, reading, meaning_class, meaning, sentences, tags):
    """meaning_class: 'english' or 'explanation' -> back-main-english vs back-main-english-explanation"""
    grammar_cards.append(dict(front_main=front_main, reading=reading, meaning_class=meaning_class,
                               meaning=meaning, sentences=sentences, tags=tags))


# =====================================================================
# VOCAB_DATA_MARKER
# =====================================================================

# --- Kanji Day 1: 家庭用品(ポット・ヒーター) ---
K5D1 = "kanji::w5 kanji::w5d1 jlpt::n2"
V("傾向", "けいこう", "Trend/tendency", "最近、若者の間で健康志向の傾向が強まっている。", "さいきん、わかもののあいだでけんこうしこうのけいこうがつよまっている。", "There's a growing health-conscious trend among young people recently.", K5D1)
V("傾く", "かたむく", "Tilt/incline", "地震で家が傾いた。", "じしんでいえがかたむいた。", "The house tilted due to the earthquake.", K5D1)
V("傾ける", "かたむける", "Make something tilt/incline", "彼は私の話に耳を傾けてくれた。", "かれはわたしのはなしにみみをかたむけてくれた。", "He lent an ear to what I said.", K5D1)
V("横転", "おうてん", "Overturn", "トラックが横転して道路をふさいだ。", "トラックがおうてんしてどうろをふさいだ。", "The truck overturned and blocked the road.", K5D1)
V("横断歩道", "おうだんほどう", "Pedestrian crossing", "横断歩道を渡るときは車に気をつけて。", "おうだんほどうをわたるときはくるまにきをつけて。", "Watch out for cars when crossing the crosswalk.", K5D1)
V("横", "よこ", "Side", "本を横に倒して置いた。", "ほんをよこにたおしておいた。", "I laid the book on its side.", K5D1)
V("熱湯", "ねっとう", "Boiling water", "カップ麺に熱湯を注いだ。", "カップめんにねっとうをそそいだ。", "I poured boiling water into the cup noodles.", K5D1)
V("湯飲み", "ゆのみ", "Teacup", "お客さんに湯飲みでお茶を出した。", "おきゃくさんにゆのみでおちゃをだした。", "I served tea to the guest in a teacup.", K5D1)
V("湯", "ゆ", "Hot water", "お湯を沸かしてコーヒーを入れた。", "おゆをわかしてコーヒーをいれた。", "I boiled water and made coffee.", K5D1)
V("湯気", "ゆげ", "Steam", "なべから湯気が立っている。", "なべからゆげがたっている。", "Steam is rising from the pot.", K5D1)
V("恐怖", "きょうふ", "Fear", "暗い道を一人で歩くのは恐怖を感じる。", "くらいみちをひとりであるくのはきょうふをかんじる。", "Walking alone on a dark road feels frightening.", K5D1)
V("恐ろしい", "おそろしい", "Fearful/terrible", "あの事故は本当に恐ろしかった。", "あのじこはほんとうにおそろしかった。", "That accident was truly terrifying.", K5D1)
V("恐れ", "おそれ", "Fear/risk", "台風の影響で大雨になる恐れがある。", "たいふうのえいきょうでおおあめになるおそれがある。", "There is a risk of heavy rain due to the typhoon.", K5D1)
V("恐れ入ります", "おそれいります", "I beg your pardon/Excuse me", "恐れ入りますが、少々お待ちください。", "おそれいりますが、しょうしょうおまちください。", "Excuse me, but please wait a moment.", K5D1)
V("原料", "げんりょう", "Raw material", "このパンの原料は小麦粉です。", "このパンのげんりょうはこむぎこです。", "The raw material of this bread is wheat flour.", K5D1)
V("原産", "げんさん", "Origin/native", "このお茶はインド原産です。", "このおちゃはインドげんさんです。", "This tea is native to India.", K5D1)
V("野原", "のはら", "Field", "子どもたちは野原を走り回った。", "こどもたちはのはらをはしりまわった。", "The children ran around the field.", K5D1)
V("原因", "げんいん", "Cause", "事故の原因を調査している。", "じこのげんいんをちょうさしている。", "They are investigating the cause of the accident.", K5D1)
V("要因", "よういん", "Factor", "物価上昇の要因はいくつかある。", "ぶっかじょうしょうのよういんはいくつかある。", "There are several factors behind the price increase.", K5D1)
V("位置", "いち", "Location", "地図で現在の位置を確認した。", "ちずでげんざいのいちをかくにんした。", "I checked my current location on the map.", K5D1)
V("装置", "そうち", "Device", "この工場には最新の安全装置がある。", "このこうじょうにはさいしんのあんぜんそうちがある。", "This factory has the latest safety device.", K5D1)
V("置く", "おく", "Put", "かばんを椅子の上に置いた。", "かばんをいすのうえにおいた。", "I put my bag on the chair.", K5D1)
V("物置", "ものおき", "Closet/storeroom", "使わない道具を物置にしまった。", "つかわないどうぐをものおきにしまった。", "I put the tools I don't use in the storeroom.", K5D1)
V("寝室", "しんしつ", "Bedroom", "寝室にベッドを二つ置いた。", "しんしつにベッドをふたつおいた。", "I put two beds in the bedroom.", K5D1)
V("寝坊", "ねぼう", "Late riser/getting up late", "今朝は寝坊して遅刻した。", "けさはねぼうしてちこくした。", "I overslept and was late this morning.", K5D1)
V("昼寝", "ひるね", "Nap", "週末は昼寝をすることが多い。", "しゅうまつはひるねをすることがおおい。", "I often take a nap on weekends.", K5D1)
V("寝る", "ねる", "Sleep", "毎晩11時に寝る。", "まいばん11じにねる。", "I go to sleep at 11 every night.", K5D1)
V("熱", "ねつ", "Heat/fever", "子どもが熱を出して学校を休んだ。", "こどもがねつをだしてがっこうをやすんだ。", "My child had a fever and stayed home from school.", K5D1)
V("熱中", "ねっちゅう", "Mania/passion/enthusiasm", "息子はサッカーに熱中している。", "むすこはサッカーにねっちゅうしている。", "My son is really into soccer.", K5D1)
V("熱心", "ねっしんな", "Enthusiastic/zealous", "彼は仕事に熱心に取り組んでいる。", "かれはしごとにねっしんにとりくんでいる。", "He works enthusiastically at his job.", K5D1)
V("熱い", "あつい", "Hot", "熱いお茶をどうぞ。", "あついおちゃをどうぞ。", "Please have some hot tea.", K5D1)
V("燃焼", "ねんしょう", "Combustion", "このエンジンは燃焼効率がいい。", "このエンジンはねんしょうこうりつがいい。", "This engine has good combustion efficiency.", K5D1)
V("焼く", "やく", "Roast/grill", "週末は庭で肉を焼いた。", "しゅうまつはにわでにくをやいた。", "We grilled meat in the garden on the weekend.", K5D1)
V("焼ける", "やける", "Be burnt/baked", "パンがきれいに焼けた。", "パンがきれいにやけた。", "The bread baked nicely.", K5D1)
V("接触", "せっしょく", "Contact", "車が電柱に接触した。", "くるまがでんちゅうにせっしょくした。", "The car made contact with the utility pole.", K5D1)
V("感触", "かんしょく", "Sense of touch", "この布は柔らかい感触だ。", "このぬのはやわらかいかんしょくだ。", "This cloth has a soft texture.", K5D1)
V("触れる", "ふれる", "Touch/mention", "そのニュースについて記事の最後で触れている。", "そのニュースについてきじのさいごでふれている。", "The article touches on that news at the end.", K5D1)
V("触る", "さわる", "Touch", "展示品には触らないでください。", "てんじひんにはさわらないでください。", "Please do not touch the exhibits.", K5D1)
V("灯油", "とうゆ", "Kerosene", "冬に備えて灯油を買っておいた。", "ふゆにそなえてとうゆをかっておいた。", "I bought kerosene in preparation for winter.", K5D1)
V("蛍光灯", "けいこうとう", "Fluorescent light", "台所の蛍光灯が切れた。", "だいどころのけいこうとうがきれた。", "The fluorescent light in the kitchen burned out.", K5D1)
V("電灯", "でんとう", "Electric light", "部屋の電灯をつけた。", "へやのでんとうをつけた。", "I turned on the room's electric light.", K5D1)
V("灯台", "とうだい", "Lighthouse", "岬の先に灯台が見える。", "みさきのさきにとうだいがみえる。", "You can see a lighthouse at the tip of the cape.", K5D1)
V("石油", "せきゆ", "Oil/petroleum", "この国は石油の輸出で栄えている。", "このくにはせきゆのゆしゅつでさかえている。", "This country prospers from petroleum exports.", K5D1)
V("原油", "げんゆ", "Crude oil", "原油の価格が値上がりしている。", "げんゆのかかくがねあがりしている。", "Crude oil prices are rising.", K5D1)
V("油断", "ゆだん", "Negligence/inattention", "簡単な問題でも油断しないほうがいい。", "かんたんなもんだいでもゆだんしないほうがいい。", "You shouldn't let your guard down even for easy problems.", K5D1)
V("油", "あぶら", "Oil", "この料理には油をたくさん使う。", "このりょうりにはあぶらをたくさんつかう。", "This dish uses a lot of oil.", K5D1)
V("余分", "よぶんな", "Excessive", "余分な荷物は家に置いてきた。", "よぶんなにもつはいえにおいてきた。", "I left the extra luggage at home.", K5D1)
V("余計", "よけいな", "Excessive/needless", "余計なことを言ってしまった。", "よけいなことをいってしまった。", "I said something unnecessary.", K5D1)
V("余裕", "よゆう", "Leeway/time to spare", "時間に余裕を持って出発した。", "じかんによゆうをもってしゅっぱつした。", "I left with plenty of time to spare.", K5D1)
V("余る", "あまる", "Be left over", "料理が余ったので冷凍しておいた。", "りょうりがあまったのでれいとうしておいた。", "Since the food was left over, I froze it.", K5D1)

# --- Kanji Day 2: 家庭用品(洗剤①) ---
K5D2 = "kanji::w5 kanji::w5d2 jlpt::n2"
V("羊毛", "ようもう", "Wool", "このセーターは羊毛で作られている。", "このセーターはようもうでつくられている。", "This sweater is made of wool.", K5D2)
V("毛", "け", "Fur/hair/wool", "猫の毛がソファについている。", "ねこのけがソファについている。", "There's cat fur on the sofa.", K5D2)
V("毛皮", "けがわ", "Fur", "母は毛皮のコートを持っている。", "はははけがわのコートをもっている。", "My mother has a fur coat.", K5D2)
V("毛糸", "けいと", "Woollen yarn", "毛糸でマフラーを編んだ。", "けいとでマフラーをあんだ。", "I knitted a scarf with woollen yarn.", K5D2)
V("糸", "いと", "Thread", "針に糸を通した。", "はりにいとをとおした。", "I threaded the needle.", K5D2)
V("肌", "はだ", "Skin", "冬は肌が乾燥する。", "ふゆははだがかんそうする。", "My skin gets dry in winter.", K5D2)
V("肌着", "はだぎ", "Undershirt", "寒いので肌着を着た。", "さむいのではだぎをきた。", "I wore an undershirt because it's cold.", K5D2)
V("柔軟", "じゅうなんな", "Flexible", "柔軟な考え方が大切だ。", "じゅうなんなかんがえかたがたいせつだ。", "A flexible mindset is important.", K5D2)
V("柔道", "じゅうどう", "Judo", "弟は柔道を習っている。", "おとうとはじゅうどうをならっている。", "My younger brother is learning judo.", K5D2)
V("柔らかい", "やわらかい", "Soft/tender", "このパンはとても柔らかい。", "このパンはとてもやわらかい。", "This bread is very soft.", K5D2)
V("香水", "こうすい", "Perfume", "出かける前に香水をつけた。", "でかけるまえにこうすいをつけた。", "I put on perfume before going out.", K5D2)
V("無香料", "むこうりょう", "No scent", "肌の弱い人には無香料の石けんがいい。", "はだのよわいひとにはむこうりょうのせっけんがいい。", "Unscented soap is good for people with sensitive skin.", K5D2)
V("香辛料", "こうしんりょう", "Spice", "この料理にはたくさんの香辛料が使われている。", "このりょうりにはたくさんのこうしんりょうがつかわれている。", "Lots of spices are used in this dish.", K5D2)
V("香り", "かおり", "Scent/smell", "コーヒーのいい香りがする。", "コーヒーのいいかおりがする。", "There's a nice smell of coffee.", K5D2)
V("軟弱", "なんじゃくな", "Weak", "彼は軟弱な性格だとよく言われる。", "かれはなんじゃくなせいかくだとよくいわれる。", "He's often said to have a weak character.", K5D2)
V("柔軟体操", "じゅうなんたいそう", "Warm-up exercises", "運動の前に柔軟体操をする。", "うんどうのまえにじゅうなんたいそうをする。", "I do warm-up exercises before exercising.", K5D2)
V("軟らかい", "やわらかい", "Soft", "この肉は軟らかくておいしい。", "このにくはやわらかくておいしい。", "This meat is tender and delicious.", K5D2)
V("溶岩", "ようがん", "Lava", "火山から溶岩が流れ出た。", "かざんからようがんがながれでた。", "Lava flowed out of the volcano.", K5D2)
V("溶ける", "とける", "Dissolve/melt/thaw", "氷が溶けて水になった。", "こおりがとけてみずになった。", "The ice melted into water.", K5D2)
V("溶かす", "とかす", "Dissolve/melt", "砂糖をお湯に溶かした。", "さとうをおゆにとかした。", "I dissolved sugar in hot water.", K5D2)
V("洗濯", "せんたく", "Washing", "週末にまとめて洗濯をする。", "しゅうまつにまとめてせんたくをする。", "I do all my laundry at once on the weekend.", K5D2)
V("洗濯機", "せんたくき", "Washing machine", "新しい洗濯機を買った。", "あたらしいせんたくきをかった。", "I bought a new washing machine.", K5D2)
V("直接", "ちょくせつ", "Direct", "直接本人に聞いたほうがいい。", "ちょくせつほんにんにきいたほうがいい。", "It's better to ask the person directly.", K5D2)
V("間接", "かんせつ", "Indirect", "間接的な言い方をした。", "かんせつてきないいかたをした。", "I spoke in an indirect way.", K5D2)
V("面接", "めんせつ", "Interview", "明日、会社の面接がある。", "あした、かいしゃのめんせつがある。", "I have a job interview at a company tomorrow.", K5D2)
V("接近", "せっきん", "Proximity", "台風が本州に接近している。", "たいふうがほんしゅうにせっきんしている。", "The typhoon is approaching the mainland.", K5D2)
V("塗る", "ぬる", "Paint/spread", "壁に白いペンキを塗った。", "かべにしろいペンキをぬった。", "I painted the wall white.", K5D2)
V("一緒", "いっしょ", "Together", "友達と一緒に映画を見た。", "ともだちといっしょにえいがをみた。", "I watched a movie with a friend.", K5D2)
V("泥", "どろ", "Mud", "雨で道が泥だらけになった。", "あめでみちがどろだらけになった。", "The road became muddy from the rain.", K5D2)
V("泥棒", "どろぼう", "Thief", "昨夜、隣の家に泥棒が入った。", "さくや、となりのいえにどろぼうがはいった。", "A thief broke into the house next door last night.", K5D2)
V("卵黄", "らんおう", "Yolk", "このケーキには卵黄をたくさん使う。", "このケーキにはらんおうをたくさんつかう。", "This cake uses a lot of egg yolk.", K5D2)
V("黄色", "きいろ", "Yellow", "娘は黄色い帽子をかぶっている。", "むすめはきいろいぼうしをかぶっている。", "My daughter is wearing a yellow hat.", K5D2)

# --- Kanji Day 3: 家庭用品(洗剤②・薬) ---
K5D3 = "kanji::w5 kanji::w5d3 jlpt::n2"
V("用途", "ようと", "Use", "この道具にはさまざまな用途がある。", "このどうぐにはさまざまなようとがある。", "This tool has various uses.", K5D3)
V("中途", "ちゅうと", "Midway/unfinished", "仕事を中途で辞めるのは良くない。", "しごとをちゅうとでやめるのはよくない。", "It's not good to quit a job halfway through.", K5D3)
V("途中", "とちゅう", "On the way/part way", "帰る途中でコンビニに寄った。", "かえるとちゅうでコンビニによった。", "I stopped by the convenience store on my way home.", K5D3)
V("途端", "とたん", "Just as something happened", "ドアを開けた途端、猫が飛び出した。", "ドアをあけたとたん、ねこがとびだした。", "The moment I opened the door, the cat jumped out.", K5D3)
V("道具", "どうぐ", "Tool", "料理に必要な道具をそろえた。", "りょうりにひつようなどうぐをそろえた。", "I gathered the tools needed for cooking.", K5D3)
V("家具", "かぐ", "Furniture", "新しい家に家具を運んだ。", "あたらしいいえにかぐをはこんだ。", "I moved the furniture to the new house.", K5D3)
V("雨具", "あまぐ", "Rain gear", "山登りには雨具が必要だ。", "やまのぼりにはあまぐがひつようだ。", "You need rain gear for mountain climbing.", K5D3)
V("具合", "ぐあい", "Condition", "今日は体の具合が悪い。", "きょうはからだのぐあいがわるい。", "I'm not feeling well today.", K5D3)
V("起床", "きしょう", "Getting up", "毎朝6時に起床する。", "まいあさ6じにきしょうする。", "I get up at 6 every morning.", K5D3)
V("床屋", "とこや", "Barbershop", "床屋で髪を切ってもらった。", "とこやでかみをきってもらった。", "I got my hair cut at the barbershop.", K5D3)
V("床", "ゆか", "Floor", "床にカーペットを敷いた。", "ゆかにカーペットをしいた。", "I laid a carpet on the floor.", K5D3)
V("床の間", "とこのま", "Alcove", "床の間に花を飾った。", "とこのまにはなをかざった。", "I decorated the alcove with flowers.", K5D3)
V("壁", "かべ", "Wall", "壁に絵をかけた。", "かべにえをかけた。", "I hung a picture on the wall.", K5D3)
V("乾電池", "かんでんち", "Dry cell battery", "リモコンの乾電池を交換した。", "リモコンのかんでんちをこうかんした。", "I replaced the batteries in the remote control.", K5D3)
V("乾く", "かわく", "Dry", "洗濯物がよく乾いた。", "せんたくものがよくかわいた。", "The laundry dried well.", K5D3)
V("乾かす", "かわかす", "Dry something", "ドライヤーで髪を乾かした。", "ドライヤーでかみをかわかした。", "I dried my hair with a hairdryer.", K5D3)
V("毛布", "もうふ", "Blanket", "寒い夜は毛布を二枚使う。", "さむいよるはもうふをにまいつかう。", "I use two blankets on cold nights.", K5D3)
V("分布", "ぶんぷ", "Distribution", "この植物は世界中に分布している。", "このしょくぶつはせかいじゅうにぶんぷしている。", "This plant is distributed throughout the world.", K5D3)
V("座布団", "ざぶとん", "Zabuton/square cushion", "畳の部屋で座布団に座った。", "たたみのへやでざぶとんにすわった。", "I sat on a zabuton cushion in the tatami room.", K5D3)
V("布", "ぬの", "Cloth", "この布はとても丈夫だ。", "このぬのはとてもじょうぶだ。", "This cloth is very durable.", K5D3)
V("電柱", "でんちゅう", "Telegraph pole", "車が電柱にぶつかった。", "くるまがでんちゅうにぶつかった。", "The car crashed into a utility pole.", K5D3)
V("柱", "はしら", "Pillar/post", "この家は木の柱で支えられている。", "このいえはきのはしらでささえられている。", "This house is supported by wooden pillars.", K5D3)
V("防虫剤", "ぼうちゅうざい", "Insect repellant", "セーターを防虫剤と一緒にしまった。", "セーターをぼうちゅうざいといっしょにしまった。", "I stored the sweater with insect repellant.", K5D3)
V("殺虫剤", "さっちゅうざい", "Insecticide", "蚊に殺虫剤をかけた。", "かにさっちゅうざいをかけた。", "I sprayed insecticide on the mosquito.", K5D3)
V("虫", "むし", "Insect", "庭でいろいろな虫を見つけた。", "にわでいろいろなむしをみつけた。", "I found various insects in the garden.", K5D3)
V("虫歯", "むしば", "Decayed tooth", "甘い物を食べすぎて虫歯になった。", "あまいものをたべすぎてむしばになった。", "I ate too many sweets and got a cavity.", K5D3)
V("歯科", "しか", "Dentistry", "歯科で歯の検査を受けた。", "しかではのけんさをうけた。", "I had a dental checkup at the dentist.", K5D3)
V("歯医者", "はいしゃ", "Dentist", "歯が痛いので歯医者に行った。", "はがいたいのではいしゃにいった。", "My tooth hurt, so I went to the dentist.", K5D3)
V("歯周病", "ししゅうびょう", "Periodontal disease", "歯周病を予防するために毎日歯を磨く。", "ししゅうびょうをよぼうするためにまいにちはをみがく。", "I brush my teeth every day to prevent periodontal disease.", K5D3)
V("歯車", "はぐるま", "Toothed wheel", "時計の中には小さな歯車がたくさんある。", "とけいのなかにはちいさなはぐるまがたくさんある。", "There are many small gears inside a watch.", K5D3)
V("予防", "よぼう", "Prevention", "風邪の予防に手を洗う。", "かぜのよぼうにてをあらう。", "I wash my hands to prevent colds.", K5D3)
V("防止", "ぼうし", "Prevention", "事故防止のために注意する。", "じこぼうしのためにちゅういする。", "Be careful to prevent accidents.", K5D3)
V("消防", "しょうぼう", "Firefighting", "消防の車が急いで走っていった。", "しょうぼうのくるまがいそいではしっていった。", "A fire engine sped past.", K5D3)
V("防ぐ", "ふせぐ", "Prevent", "マスクで風邪を防ぐ。", "マスクでかぜをふせぐ。", "I prevent colds by wearing a mask.", K5D3)
V("磨く", "みがく", "Polish/brush", "寝る前に歯を磨く。", "ねるまえにはをみがく。", "I brush my teeth before going to bed.", K5D3)
V("歯磨き", "はみがき", "Tooth brushing", "食後の歯磨きを忘れないでください。", "しょくごのはみがきをわすれないでください。", "Don't forget to brush your teeth after meals.", K5D3)
V("抜群", "ばつぐん", "Outstanding/unrivaled", "彼女の成績は抜群だ。", "かのじょのせいせきはばつぐんだ。", "Her grades are outstanding.", K5D3)
V("抜く", "ぬく", "Remove/extract/omit", "虫歯を抜いてもらった。", "むしばをぬいてもらった。", "I had the decayed tooth extracted.", K5D3)
V("抜ける", "ぬける", "Fall out/be missing", "最近、髪の毛が抜けやすい。", "さいきん、かみのけがぬけやすい。", "My hair has been falling out easily lately.", K5D3)
V("追い抜く", "おいぬく", "Leave behind/overtake", "マラソンで前の選手を追い抜いた。", "マラソンでまえのせんしゅをおいぬいた。", "I overtook the runner ahead of me in the marathon.", K5D3)
V("悩む", "なやむ", "Worry", "進路について悩んでいる。", "しんろについてなやんでいる。", "I'm worrying about my career path.", K5D3)
V("悩み", "なやみ", "A worry/distress", "友達に悩みを相談した。", "ともだちになやみをそうだんした。", "I consulted a friend about my worries.", K5D3)
V("髪", "かみ", "Hair", "彼女は髪を短く切った。", "かのじょはかみをみじかくきった。", "She cut her hair short.", K5D3)
V("白髪", "しらが", "White/gray hair", "最近、白髪が増えてきた。", "さいきん、しらががふえてきた。", "My gray hair has been increasing recently.", K5D3)
V("髪の毛", "かみのけ", "A hair", "服に髪の毛が一本ついていた。", "ふくにかみのけがいっぽんついていた。", "There was a single hair stuck to my clothes.", K5D3)

# --- Kanji Day 4: 家庭用品(薬) ---
K5D4 = "kanji::w5 kanji::w5d4 jlpt::n2"
V("名刺", "めいし", "Name card", "初対面の人と名刺を交換した。", "しょたいめんのひととめいしをこうかんした。", "I exchanged business cards with someone I met for the first time.", K5D4)
V("刺激", "しげき", "Stimulus", "新しい環境はいい刺激になる。", "あたらしいかんきょうはいいしげきになる。", "A new environment provides good stimulation.", K5D4)
V("刺す", "さす", "Stab", "蜂に刺された。", "はちにさされた。", "I was stung by a bee.", K5D4)
V("刺さる", "ささる", "Be pierced", "指にとげが刺さった。", "ゆびにとげがささった。", "A splinter got stuck in my finger.", K5D4)
V("肩", "かた", "Shoulder", "長時間座っていて肩がこった。", "ちょうじかんすわっていてかたがこった。", "My shoulders got stiff from sitting for a long time.", K5D4)
V("肩書き", "かたがき", "Title", "名刺に肩書きを書いた。", "めいしにかたがきをかいた。", "I wrote my title on the business card.", K5D4)
V("腰痛", "ようつう", "Lower backache", "腰痛がひどくて病院に行った。", "ようつうがひどくてびょういんにいった。", "My lower back pain was so bad I went to the hospital.", K5D4)
V("腰", "こし", "Waist/hip", "重い荷物を持って腰を痛めた。", "おもいにもつをもってこしをいためた。", "I hurt my back carrying a heavy load.", K5D4)
V("腰掛ける", "こしかける", "Sit", "ベンチに腰掛けて休んだ。", "ベンチにこしかけてやすんだ。", "I sat on the bench and rested.", K5D4)
V("腰掛け", "こしかけ", "Chair/seat", "公園に木の腰掛けがある。", "こうえんにきのこしかけがある。", "There's a wooden seat in the park.", K5D4)
V("関節", "かんせつ", "Joint", "年をとると関節が痛くなる。", "としをとるとかんせつがいたくなる。", "Joints hurt more as you get older.", K5D4)
V("調節", "ちょうせつ", "Adjustment", "エアコンの温度を調節した。", "エアコンのおんどをちょうせつした。", "I adjusted the air conditioner's temperature.", K5D4)
V("節約", "せつやく", "Thrift", "電気代を節約するようにしている。", "でんきだいをせつやくするようにしている。", "I try to save on electricity costs.", K5D4)
V("節", "ふし", "Knot in wood/joint", "この木の板には節が多い。", "このきのいたにはふしがおおい。", "This wooden board has many knots.", K5D4)
V("神話", "しんわ", "Myth", "ギリシャ神話を読むのが好きだ。", "ギリシャしんわをよむのがすきだ。", "I like reading Greek mythology.", K5D4)
V("神道", "しんとう", "Shintoism", "神道は日本の伝統的な宗教だ。", "しんとうはにほんのでんとうてきなしゅうきょうだ。", "Shinto is a traditional religion of Japan.", K5D4)
V("神経", "しんけい", "Nerve", "彼は神経が細やかな人だ。", "かれはしんけいがこまやかなひとだ。", "He is a person with delicate nerves.", K5D4)
V("神社", "じんじゃ", "Shrine", "お正月に神社にお参りした。", "おしょうがつにじんじゃにおまいりした。", "I visited a shrine on New Year's Day.", K5D4)
V("神様", "かみさま", "God", "神様にお願いごとをした。", "かみさまにおねがいごとをした。", "I made a wish to the gods.", K5D4)
V("頭痛", "ずつう", "Headache", "頭痛がひどいので薬を飲んだ。", "ずつうがひどいのでくすりをのんだ。", "I had a bad headache, so I took medicine.", K5D4)
V("苦痛", "くつう", "Pain/suffering", "長時間の会議は苦痛だった。", "ちょうじかんのかいぎはくつうだった。", "The long meeting was painful.", K5D4)
V("痛い", "いたい", "Sore/painful", "歯が痛くて眠れなかった。", "はがいたくてねむれなかった。", "My tooth hurt so much I couldn't sleep.", K5D4)
V("痛む", "いたむ", "Ache/hurt", "けがをしたところがまだ痛む。", "けがをしたところがまだいたむ。", "The injured spot still hurts.", K5D4)
V("入浴", "にゅうよく", "Bathing", "毎晩入浴してから寝る。", "まいばんにゅうよくしてからねる。", "I take a bath every night before sleeping.", K5D4)
V("浴室", "よくしつ", "Bathroom", "浴室を掃除した。", "よくしつをそうじした。", "I cleaned the bathroom.", K5D4)
V("海水浴", "かいすいよく", "Sea bathing", "夏休みに海水浴に行った。", "なつやすみにかいすいよくにいった。", "I went sea bathing during summer vacation.", K5D4)
V("浴衣", "ゆかた", "Summer kimono", "お祭りに浴衣を着て行った。", "おまつりにゆかたをきていった。", "I went to the festival wearing a yukata.", K5D4)
V("浴びる", "あびる", "Pour water over oneself/soak up", "朝シャワーを浴びる。", "あさシャワーをあびる。", "I take a shower in the morning.", K5D4)
V("目的", "もくてき", "Aim/purpose", "留学の目的は語学の向上だ。", "りゅうがくのもくてきはごがくのこうじょうだ。", "The purpose of studying abroad is to improve language skills.", K5D4)
V("具体的", "ぐたいてきな", "Concrete/specific", "もっと具体的な例を挙げてください。", "もっとぐたいてきなれいをあげてください。", "Please give a more concrete example.", K5D4)
V("的確", "てきかくな", "Accurate/exact", "彼は的確な判断をする人だ。", "かれはてきかくなはんだんをするひとだ。", "He is a person who makes accurate judgments.", K5D4)
V("汗", "あせ", "Perspiration/sweat", "運動をして汗をかいた。", "うんどうをしてあせをかいた。", "I exercised and worked up a sweat.", K5D4)
V("医師", "いし", "Doctor", "彼は大学病院の医師だ。", "かれはだいがくびょういんのいしだ。", "He is a doctor at a university hospital.", K5D4)
V("教師", "きょうし", "Teacher", "姉は中学校の教師をしている。", "あねはちゅうがっこうのきょうしをしている。", "My older sister is a junior high school teacher.", K5D4)
V("技師", "ぎし", "Engineer", "兄はソフトウェアの技師だ。", "あにはソフトウェアのぎしだ。", "My older brother is a software engineer.", K5D4)
V("相談", "そうだん", "Consultation", "進路について先生に相談した。", "しんろについてせんせいにそうだんした。", "I consulted my teacher about my career path.", K5D4)
V("冗談", "じょうだん", "Joke", "彼はいつも冗談を言って笑わせる。", "かれはいつもじょうだんをいってわらわせる。", "He always makes jokes and makes people laugh.", K5D4)
V("会談", "かいだん", "Conference/talks", "両国の首脳が会談を行った。", "りょうこくのしゅのうがかいだんをおこなった。", "The leaders of the two countries held talks.", K5D4)
V("乾燥", "かんそう", "Dryness", "冬は空気が乾燥する。", "ふゆはくうきがかんそうする。", "The air is dry in winter.", K5D4)
V("骨折", "こっせつ", "Bone fracture", "スキーで足を骨折した。", "スキーであしをこっせつした。", "I fractured my leg while skiing.", K5D4)
V("折れる", "おれる", "Break", "強い風で木の枝が折れた。", "つよいかぜできのえだがおれた。", "A tree branch broke in the strong wind.", K5D4)
V("折る", "おる", "Break/fold something", "紙を半分に折った。", "かみをはんぶんにおった。", "I folded the paper in half.", K5D4)

# --- Kanji Day 5: 食品 ---
K5D5 = "kanji::w5 kanji::w5d5 jlpt::n2"
V("賞", "しょう", "Prize", "作文コンクールで賞をもらった。", "さくぶんコンクールでしょうをもらった。", "I received a prize in the essay contest.", K5D5)
V("賞金", "しょうきん", "Prize money", "マラソン大会の優勝者には賞金が出る。", "マラソンたいかいのゆうしょうしゃにはしょうきんがでる。", "Prize money is given to the marathon race winner.", K5D5)
V("賞品", "しょうひん", "Prize goods", "抽選で豪華な賞品が当たった。", "ちゅうせんでごうかなしょうひんがあたった。", "I won a luxurious prize in the drawing.", K5D5)
V("賞味期限", "しょうみきげん", "Best-before date", "牛乳の賞味期限を確認した。", "ぎゅうにゅうのしょうみきげんをかくにんした。", "I checked the best-before date on the milk.", K5D5)
V("金庫", "きんこ", "Safe", "大切な書類を金庫にしまった。", "たいせつなしょるいをきんこにしまった。", "I put important documents in the safe.", K5D5)
V("車庫", "しゃこ", "Garage", "車庫に車を入れた。", "しゃこにくるまをいれた。", "I parked the car in the garage.", K5D5)
V("冷蔵庫", "れいぞうこ", "Refrigerator", "冷蔵庫に野菜を入れた。", "れいぞうこにやさいをいれた。", "I put the vegetables in the refrigerator.", K5D5)
V("製造", "せいぞう", "Manufacture", "この工場では自動車の部品を製造している。", "このこうじょうではじどうしゃのぶひんをせいぞうしている。", "This factory manufactures car parts.", K5D5)
V("改造", "かいぞう", "Conversion/adaptation", "古い家を改造してカフェにした。", "ふるいいえをかいぞうしてカフェにした。", "I converted the old house into a café.", K5D5)
V("造る", "つくる", "Make", "職人が手作業で船を造った。", "しょくにんがてさぎょうでふねをつくった。", "An artisan built the boat by hand.", K5D5)
V("費用", "ひよう", "Expense/cost", "旅行の費用を計算した。", "りょこうのひようをけいさんした。", "I calculated the cost of the trip.", K5D5)
V("消費", "しょうひ", "Consumption", "エネルギーの消費を減らす努力をしている。", "エネルギーのしょうひをへらすどりょくをしている。", "I'm making efforts to reduce energy consumption.", K5D5)
V("可", "か", "Acceptable/possible", "この用紙は鉛筆書きでも可です。", "このようしはえんぴつがきでもかです。", "This form is acceptable even in pencil.", K5D5)
V("不可", "ふか", "Unacceptable", "会場内での飲食は不可です。", "かいじょうないでのいんしょくはふかです。", "Eating and drinking are not allowed in the venue.", K5D5)
V("可能", "かのうな", "Possible", "早めの予約なら可能です。", "はやめのよやくならかのうです。", "An early reservation is possible.", K5D5)
V("可決", "かけつ", "Approval", "新しい法案が国会で可決された。", "あたらしいほうあんがこっかいでかけつされた。", "The new bill was passed in the Diet.", K5D5)
V("秒", "びょう", "Second", "あと10秒で終わります。", "あと10びょうでおわります。", "It will end in 10 more seconds.", K5D5)
V("自身", "じしん", "Oneself", "自分自身を信じることが大切だ。", "じぶんじしんをしんじることがたいせつだ。", "It's important to believe in yourself.", K5D5)
V("身体", "しんたい", "Body", "身体検査を受けた。", "しんたいけんさをうけた。", "I had a physical examination.", K5D5)
V("身長", "しんちょう", "Height", "息子の身長がずいぶん伸びた。", "むすこのしんちょうがずいぶんのびた。", "My son's height has grown quite a lot.", K5D5)
V("出身", "しゅっしん", "Coming from", "彼女は大阪出身だ。", "かのじょはおおさかしゅっしんだ。", "She is from Osaka.", K5D5)
V("中身", "なかみ", "Content", "箱の中身を確認した。", "はこのなかみをかくにんした。", "I checked the contents of the box.", K5D5)
V("刺身", "さしみ", "Sliced raw fish", "新鮮な刺身を食べた。", "しんせんなさしみをたべた。", "I ate fresh sashimi.", K5D5)
V("召し上がる", "めしあがる", "Eat (polite form)", "どうぞ温かいうちに召し上がってください。", "どうぞあたたかいうちにめしあがってください。", "Please eat it while it's still warm.", K5D5)
V("乾杯", "かんぱい", "Cheers!", "みんなでグラスを上げて乾杯した。", "みんなでグラスをあげてかんぱいした。", "Everyone raised their glasses and toasted.", K5D5)
V("杯", "さかずき", "Sake cup", "祖父から古い杯をもらった。", "そふからふるいさかずきをもらった。", "I received an old sake cup from my grandfather.", K5D5)
V("沸騰", "ふっとう", "Boiling", "お湯が沸騰したら麺を入れる。", "おゆがふっとうしたらめんをいれる。", "Once the water boils, add the noodles.", K5D5)
V("沸く", "わく", "Boil", "やかんのお湯が沸いた。", "やかんのおゆがわいた。", "The water in the kettle boiled.", K5D5)
V("沸かす", "わかす", "Boil something", "お風呂を沸かした。", "おふろをわかした。", "I heated the bath water.", K5D5)
V("粉末", "ふんまつ", "Powder", "この薬は粉末になっている。", "このくすりはふんまつになっている。", "This medicine is in powder form.", K5D5)
V("花粉", "かふん", "Pollen", "春は花粉がたくさん飛ぶ。", "はるはかふんがたくさんとぶ。", "A lot of pollen flies around in spring.", K5D5)
V("小麦粉", "こむぎこ", "Wheat flour", "パンは小麦粉から作られる。", "パンはこむぎこからつくられる。", "Bread is made from wheat flour.", K5D5)
V("粉", "こな", "Powder/flour", "粉をふるいにかけた。", "こなをふるいにかけた。", "I sifted the flour.", K5D5)
V("月末", "げつまつ", "End of the month", "月末に家賃を払う。", "げつまつにやちんをはらう。", "I pay the rent at the end of the month.", K5D5)
V("結末", "けつまつ", "End/conclusion", "その映画の結末に驚いた。", "そのえいがのけつまつにおどろいた。", "I was surprised by the ending of that movie.", K5D5)
V("末", "すえ", "End", "悩んだ末に決心した。", "なやんだすえにけっしんした。", "After much worrying, I made up my mind.", K5D5)
V("末っ子", "すえっこ", "Youngest child", "私は三人兄弟の末っ子だ。", "わたしはさんにんきょうだいのすえっこだ。", "I am the youngest of three siblings.", K5D5)
V("栄養", "えいよう", "Nutrition", "バランスのいい栄養を取ることが大切だ。", "バランスのいいえいようをとることがたいせつだ。", "It's important to get well-balanced nutrition.", K5D5)
V("繁栄", "はんえい", "Prosperity", "この町は貿易で繁栄した。", "このまちはぼうえきではんえいした。", "This town prospered through trade.", K5D5)
V("栄える", "さかえる", "Flourish/prosper", "昔、この地域は商業で栄えた。", "むかし、このちいきはしょうぎょうでさかえた。", "Long ago, this area flourished through commerce.", K5D5)

# --- Kanji Day 6: インターホン・パソコン ---
K5D6 = "kanji::w5 kanji::w5d6 jlpt::n2"
V("鳴る", "なる", "Ring/chime", "電話が鳴った。", "でんわがなった。", "The phone rang.", K5D6)
V("鳴らす", "ならす", "Ring a bell", "ドアのベルを鳴らした。", "ドアのベルをならした。", "I rang the doorbell.", K5D6)
V("鳴く", "なく", "Chirp/croak", "庭で鳥が鳴いている。", "にわでとりがないている。", "A bird is chirping in the garden.", K5D6)
V("怒鳴る", "どなる", "Shout", "父は怒って大きな声で怒鳴った。", "ちちはおこっておおきなこえでどなった。", "My father got angry and shouted loudly.", K5D6)
V("訪問", "ほうもん", "Visit", "来週、取引先を訪問する予定だ。", "らいしゅう、とりひきさきをほうもんするよていだ。", "I plan to visit the client next week.", K5D6)
V("訪れる", "おとずれる", "Visit/come", "秋が訪れた。", "あきがおとずれた。", "Autumn has arrived.", K5D6)
V("訪ねる", "たずねる", "Visit", "友人の家を訪ねた。", "ゆうじんのいえをたずねた。", "I visited a friend's house.", K5D6)
V("呼吸", "こきゅう", "Respiration", "深呼吸をして落ち着いた。", "しんこきゅうをしておちついた。", "I took a deep breath and calmed down.", K5D6)
V("呼ぶ", "よぶ", "Call", "名前を呼ばれて振り向いた。", "なまえをよばれてふりむいた。", "I turned around when my name was called.", K5D6)
V("呼び出す", "よびだす", "Call/summon", "校長室に呼び出された。", "こうちょうしつによびだされた。", "I was summoned to the principal's office.", K5D6)
V("警官", "けいかん", "Police officer", "警官に道を尋ねた。", "けいかんにみちをたずねた。", "I asked a police officer for directions.", K5D6)
V("警備", "けいび", "Security", "会場の警備が厳しかった。", "かいじょうのけいびがきびしかった。", "Security at the venue was strict.", K5D6)
V("警察", "けいさつ", "Police", "事故を警察に通報した。", "じこをけいさつにつうほうした。", "I reported the accident to the police.", K5D6)
V("警報", "けいほう", "Warning/alarm", "大雨警報が発表された。", "おおあめけいほうがはっぴょうされた。", "A heavy rain warning was issued.", K5D6)
V("予報", "よほう", "Forecast", "天気予報によると明日は晴れるらしい。", "てんきよほうによるとあしたははれるらしい。", "According to the weather forecast, it will be sunny tomorrow.", K5D6)
V("情報", "じょうほう", "Information", "インターネットでいろいろな情報を調べた。", "インターネットでいろいろなじょうほうをしらべた。", "I looked up various information on the internet.", K5D6)
V("電報", "でんぽう", "Telegram", "結婚式に電報を送った。", "けっこんしきにでんぽうをおくった。", "I sent a telegram to the wedding.", K5D6)
V("裏", "うら", "Reverse/back", "紙の裏に名前を書いた。", "かみのうらになまえをかいた。", "I wrote my name on the back of the paper.", K5D6)
V("裏口", "うらぐち", "Back door", "裏口から入ってください。", "うらぐちからはいってください。", "Please enter through the back door.", K5D6)
V("裏切る", "うらぎる", "Betray", "友人に裏切られた。", "ゆうじんにうらぎられた。", "I was betrayed by a friend.", K5D6)
V("裏表", "うらおもて", "Both sides", "このシャツは裏表どちらでも着られる。", "このシャツはうらおもてどちらでもきられる。", "This shirt can be worn either way, inside out or not.", K5D6)
V("交差点", "こうさてん", "Intersection", "交差点で信号を待った。", "こうさてんでしんごうをまった。", "I waited for the signal at the intersection.", K5D6)
V("差", "さ", "Difference", "二人の意見に差がある。", "ふたりのいけんにさがある。", "There is a difference between the two people's opinions.", K5D6)
V("差出人", "さしだしにん", "Sender", "手紙の差出人を確認した。", "てがみのさしだしにんをかくにんした。", "I checked the sender of the letter.", K5D6)
V("差別", "さべつ", "Discrimination", "どんな差別も許されない。", "どんなさべつもゆるされない。", "No kind of discrimination is acceptable.", K5D6)
V("人差し指", "ひとさしゆび", "Index finger", "人差し指でボタンを押した。", "ひとさしゆびでボタンをおした。", "I pressed the button with my index finger.", K5D6)
V("接続", "せつぞく", "Connection", "パソコンをインターネットに接続した。", "パソコンをインターネットにせつぞくした。", "I connected the computer to the internet.", K5D6)
V("継続", "けいぞく", "Continuity", "プロジェクトの継続を決めた。", "プロジェクトのけいぞくをきめた。", "We decided to continue the project.", K5D6)
V("手続き", "てつづき", "Procedure", "入学の手続きを済ませた。", "にゅうがくのてつづきをすませた。", "I completed the enrollment procedures.", K5D6)
V("続く", "つづく", "Continue", "雨が一週間続いている。", "あめがいっしゅうかんつづいている。", "The rain has continued for a week.", K5D6)
V("続ける", "つづける", "Continue something", "毎日練習を続けている。", "まいにちれんしゅうをつづけている。", "I keep practicing every day.", K5D6)
V("辞書", "じしょ", "Dictionary", "わからない単語を辞書で調べた。", "わからないたんごをじしょでしらべた。", "I looked up the word I didn't know in the dictionary.", K5D6)
V("辞典", "じてん", "Dictionary", "国語辞典を買った。", "こくごじてんをかった。", "I bought a Japanese dictionary.", K5D6)
V("辞表", "じひょう", "Resignation", "上司に辞表を出した。", "じょうしにじひょうをだした。", "I submitted my resignation to my boss.", K5D6)
V("辞める", "やめる", "Resign/retire", "来月、会社を辞めることにした。", "らいげつ、かいしゃをやめることにした。", "I decided to quit my job next month.", K5D6)
V("画面", "がめん", "Screen", "パソコンの画面が急に暗くなった。", "パソコンのがめんがきゅうにくらくなった。", "The computer screen suddenly went dark.", K5D6)
V("正面", "しょうめん", "Front", "正面玄関で待っています。", "しょうめんげんかんでまっています。", "I'll be waiting at the front entrance.", K5D6)
V("方面", "ほうめん", "Direction", "新宿方面の電車に乗った。", "しんじゅくほうめんのでんしゃにのった。", "I took a train heading toward Shinjuku.", K5D6)
V("面積", "めんせき", "Surface area", "この部屋の面積は20平方メートルだ。", "このへやのめんせきは20へいほうメートルだ。", "The area of this room is 20 square meters.", K5D6)
V("操作", "そうさ", "Operation/manipulation", "機械の操作を覚えた。", "きかいのそうさをおぼえた。", "I learned how to operate the machine.", K5D6)
V("体操", "たいそう", "Exercise/gymnastics", "毎朝ラジオ体操をしている。", "まいあさラジオたいそうをしている。", "I do radio calisthenics every morning.", K5D6)
V("実行", "じっこう", "Practice/action", "計画を実行に移した。", "けいかくをじっこうにうつした。", "I put the plan into action.", K5D6)
V("事実", "じじつ", "Fact", "それは事実ではない。", "それはじじつではない。", "That's not a fact.", K5D6)
V("実験", "じっけん", "Experiment", "理科の授業で実験をした。", "りかのじゅぎょうでじっけんをした。", "We did an experiment in science class.", K5D6)
V("実", "み", "Fruit/nut", "この木には秋に実がなる。", "このきにはあきにみがなる。", "This tree bears fruit in autumn.", K5D6)
V("実る", "みのる", "Bear fruit", "長年の努力が実った。", "ながねんのどりょくがみのった。", "Years of effort bore fruit.", K5D6)
V("列", "れつ", "Line/queue", "店の前に列ができている。", "みせのまえにれつができている。", "There's a line forming in front of the store.", K5D6)
V("列車", "れっしゃ", "Train", "夜行列車で旅行した。", "やこうれっしゃでりょこうした。", "I traveled by overnight train.", K5D6)
V("行列", "ぎょうれつ", "Procession", "人気の店には行列ができている。", "にんきのみせにはぎょうれつができている。", "There's a line at the popular store.", K5D6)
V("列島", "れっとう", "Archipelago", "日本列島は南北に長い。", "にほんれっとうはなんぼくにながい。", "The Japanese archipelago is long from north to south.", K5D6)

# --- Kanji Day 7 Extra: 漢字を使って遊ぼう (bonus puzzle, kanji 453-470) ---
# 棒's only listed word, 泥棒, was already carded under 泥 (Day 2) -- skipped as an exact duplicate.
K5DE = "kanji::w5 kanji::w5dExtra jlpt::n2"
V("枯れる", "かれる", "Wither", "水をやらなかったので花が枯れてしまった。", "みずをやらなかったのではながかれてしまった。", "The flowers withered because I didn't water them.", K5DE)
V("舟", "ふね", "Boat", "小さな舟で川を渡った。", "ちいさなふねでかわをわたった。", "I crossed the river in a small boat.", K5DE)
V("貧しい", "まずしい", "Poor", "若いころは貧しい暮らしをしていた。", "わかいころはまずしいくらしをしていた。", "I lived a poor life when I was young.", K5DE)
V("昔", "むかし", "Old times/long ago", "昔、この辺りは田んぼだった。", "むかし、このあたりはたんぼだった。", "Long ago, this area used to be rice paddies.", K5DE)
V("岩", "いわ", "Rock", "大きな岩の上に座って休んだ。", "おおきないわのうえにすわってやすんだ。", "I sat on a large rock and rested.", K5DE)
V("泣く", "なく", "Cry/weep", "赤ちゃんが大声で泣いている。", "あかちゃんがおおごえでないている。", "The baby is crying loudly.", K5DE)
V("咲く", "さく", "Bloom", "庭にバラの花が咲いた。", "にわにバラのはながさいた。", "Roses bloomed in the garden.", K5DE)
V("司会", "しかい", "Moderating/facilitating a meeting", "結婚式の司会を頼まれた。", "けっこんしきのしかいをたのまれた。", "I was asked to emcee the wedding.", K5DE)
V("残念", "ざんねん", "Regret/disappointment", "試合に負けて残念だった。", "しあいにまけてざんねんだった。", "I was disappointed we lost the match.", K5DE)
V("涼しい", "すずしい", "Cool", "山の上は涼しくて気持ちがいい。", "やまのうえはすずしくてきもちがいい。", "It's cool and pleasant on top of the mountain.", K5DE)
V("散歩", "さんぽ", "Walk/stroll", "毎朝、犬と散歩をする。", "まいあさ、いぬとさんぽをする。", "I take a walk with my dog every morning.", K5DE)
V("吹く", "ふく", "Blow", "強い風が吹いている。", "つよいかぜがふいている。", "A strong wind is blowing.", K5DE)
V("赤ん坊", "あかんぼう", "Baby", "妹に赤ん坊が生まれた。", "いもうとにあかんぼうがうまれた。", "My younger sister gave birth to a baby.", K5DE)
V("怒る", "おこる", "Be angry", "遅刻して先生に怒られた。", "ちこくしてせんせいにおこられた。", "I was scolded by my teacher for being late.", K5DE)
V("家畜", "かちく", "Livestock", "この地域では家畜を育てている。", "このちいきではかちくをそだてている。", "Livestock are raised in this region.", K5DE)
V("才能", "さいのう", "Ability/talent", "彼女には音楽の才能がある。", "かのじょにはおんがくのさいのうがある。", "She has a talent for music.", K5DE)
V("珍しい", "めずらしい", "Rare", "この博物館には珍しい石が展示されている。", "このはくぶつかんにはめずらしいいしがてんじされている。", "Rare stones are on display at this museum.", K5DE)

# --- Vocabulary Day 1: 物事・日中・年月 ---
VOC5D1 = "vocabulary::w5 vocabulary::w5d1 jlpt::n2"
V("物事", "ものごと", "Things", "物事にはすべて原因と結果がある。", "ものごとにはすべてげんいんとけっかがある。", "Everything has a cause and effect.", VOC5D1)
V("人物", "じんぶつ", "A person", "彼は歴史上有名な人物だ。", "かれはれきしじょうゆうめいなじんぶつだ。", "He is a famous historical figure.", VOC5D1)
V("物理", "ぶつり", "Physics", "大学で物理を専攻した。", "だいがくでぶつりをせんこうした。", "I majored in physics at university.", VOC5D1)
V("食物", "しょくもつ", "Food", "高カロリーの食物は控えたほうがいい。", "こうカロリーのしょくもつはひかえたほうがいい。", "You should avoid high-calorie food.", VOC5D1)
V("作物", "さくもつ", "Crop", "この地方の主な作物は米だ。", "このちほうのおもなさくもつはこめだ。", "The main crop of this region is rice.", VOC5D1)
V("書物", "しょもつ", "Books/literature", "図書館には古い書物がたくさんある。", "としょかんにはふるいしょもつがたくさんある。", "There are many old books in the library.", VOC5D1)
V("生き物／生物", "いきもの／せいぶつ", "A living thing/animals/insects", "海の生物について調べる。", "うみのせいぶつについてしらべる。", "I research marine life.", VOC5D1)
V("入れ物", "いれもの", "A container", "つかまえた虫を入れておく入れ物は、何かありますか。", "つかまえたむしをいれておくいれものは、なにかありますか。", "Do you have a container to put the bug I caught in?", VOC5D1)
V("物音", "ものおと", "Sound", "夜中に変な物音がした。", "よなかにへんなものおとがした。", "There was a strange noise in the middle of the night.", VOC5D1)
V("物語", "ものがたり", "A story", "この物語は子どもに人気がある。", "このものがたりはこどもににんきがある。", "This story is popular with children.", VOC5D1)
V("生年月日", "せいねんがっぴ", "Date of birth", "申込書に生年月日を書いた。", "もうしこみしょにせいねんがっぴをかいた。", "I wrote my date of birth on the application form.", VOC5D1)
V("月日", "つきひ", "Time/days and months", "月日が流れて、春から夏になりました。", "つきひがながれて、はるからなつになりました。", "Time passed, and it went from spring to summer.", VOC5D1)
V("元日", "がんじつ", "New Year's Day", "元日は家族と過ごす。", "がんじつはかぞくとすごす。", "I spend New Year's Day with my family.", VOC5D1)
V("後日", "ごじつ", "Later/another day", "後日お伺いしますが、いつがよろしいでしょうか。", "ごじつおうかがいしますが、いつがよろしいでしょうか。", "I will visit another day - when would be convenient?", VOC5D1)
V("日時", "にちじ", "Date and time", "会議の日時を確認した。", "かいぎのにちじをかくにんした。", "I confirmed the date and time of the meeting.", VOC5D1)
V("今日", "こんにち", "Today (nowadays)", "日本の今日の経済は、たいへん不安定な状態だ。", "にほんのこんにちのけいざいは、たいへんふあんていなじょうたいだ。", "Japan's economy today is in a very unstable state.", VOC5D1)
V("日中", "にっちゅう", "During the day/daytime", "日中は暑いが、夜は涼しくなる。", "にっちゅうはあついが、よるはすずしくなる。", "It's hot during the day, but cools down at night.", VOC5D1)
V("日光", "にっこう", "Sunlight/the sun", "植物には日光が必要だ。", "しょくぶつにはにっこうがひつようだ。", "Plants need sunlight.", VOC5D1)
V("日の出", "ひので", "Sunrise", "山の上で日の出を見た。", "やまのうえでひのでをみた。", "I watched the sunrise from the top of the mountain.", VOC5D1)
V("日の入り", "ひのいり", "Sunset", "日の入りの時間が早くなってきた。", "ひのいりのじかんがはやくなってきた。", "Sunset is getting earlier.", VOC5D1)
V("来日", "らいにち", "Come to Japan", "その歌手は来月来日する予定だ。", "そのかしゅはらいげつらいにちするよていだ。", "That singer plans to come to Japan next month.", VOC5D1)
V("年間", "ねんかん", "Year/during the year", "年間スケジュールによると、今月、中間テストがあります。", "ねんかんスケジュールによると、こんげつ、ちゅうかんテストがあります。", "According to the annual schedule, there's a midterm exam this month.", VOC5D1)
V("年月", "ねんげつ", "Years/a long time", "長い年月をかけて完成させた作品だ。", "ながいねんげつをかけてかんせいさせたさくひんだ。", "This is a work completed over many years.", VOC5D1)
V("年中", "ねんじゅう", "All year around", "このプールは年中営業している。", "このプールはねんじゅうえいぎょうしている。", "This pool is open all year round.", VOC5D1)
V("年度", "ねんど", "Fiscal/school year", "新しい年度が4月から始まる。", "あたらしいねんどが4がつからはじまる。", "The new fiscal year begins in April.", VOC5D1)
V("少年／青少年", "しょうねん／せいしょうねん", "Youth/boys/teenagers", "少年サッカーチームに入っている。", "しょうねんサッカーチームにはいっている。", "He's on a boys' soccer team.", VOC5D1)
V("青年", "せいねん", "A young man", "彼は真面目な青年だ。", "かれはまじめなせいねんだ。", "He is a serious young man.", VOC5D1)
V("中年", "ちゅうねん", "Middle-aged", "中年になって体力の衰えを感じる。", "ちゅうねんになってたいりょくのおとろえをかんじる。", "Now that I'm middle-aged, I feel my strength declining.", VOC5D1)
V("年代", "ねんだい", "Generation/era", "同じ年代の人と話し合うのは楽しいです。", "おなじねんだいのひととはなしあうのはたのしいです。", "It's fun to talk with people of the same generation.", VOC5D1)

# --- Vocabulary Day 2: 夜中・世間・作業 ---
VOC5D2 = "vocabulary::w5 vocabulary::w5d2 jlpt::n2"
V("大工", "だいく", "A carpenter", "父は大工として働いている。", "ちちはだいくとしてはたらいている。", "My father works as a carpenter.", VOC5D2)
V("重大", "じゅうだい", "Important/serious", "これは重大な問題だ。", "これはじゅうだいなもんだいだ。", "This is a serious problem.", VOC5D2)
V("大小", "だいしょう", "Large and small/size", "部屋の大小に関わらず掃除は大変だ。", "へやのだいしょうにかかわらずそうじはたいへんだ。", "Regardless of room size, cleaning is hard work.", VOC5D2)
V("大気", "たいき", "The atmosphere/air", "大気の汚染が深刻な問題になっている。", "たいきのおせんがしんこくなもんだいになっている。", "Air pollution has become a serious problem.", VOC5D2)
V("大半", "たいはん", "Majority/mostly", "クラスの大半が自転車で通学している。", "クラスのたいはんがじてんしゃでつうがくしている。", "The majority of the class commutes to school by bicycle.", VOC5D2)
V("大金", "たいきん", "A lot of money", "宝くじで大金を手に入れた。", "たからくじでたいきんをてにいれた。", "I won a large sum of money in the lottery.", VOC5D2)
V("大木", "たいぼく", "A huge tree", "神社の境内に大木がある。", "じんじゃのけいだいにたいぼくがある。", "There's a huge tree in the shrine's grounds.", VOC5D2)
V("中心", "ちゅうしん", "The center/core", "東京は日本の経済の中心です。", "とうきょうはにほんのけいざいのちゅうしんです。", "Tokyo is the center of Japan's economy.", VOC5D2)
V("中世", "ちゅうせい", "Medieval times", "中世ヨーロッパの歴史に興味がある。", "ちゅうせいヨーロッパのれきしにきょうみがある。", "I'm interested in the history of medieval Europe.", VOC5D2)
V("中古", "ちゅうこ", "Used/second-hand", "中古の車を安く買った。", "ちゅうこのくるまをやすくかった。", "I bought a used car cheaply.", VOC5D2)
V("空中", "くうちゅう", "In the air/mid-air", "鳥が空中を飛んでいる。", "とりがくうちゅうをとんでいる。", "Birds are flying in the air.", VOC5D2)
V("集中", "しゅうちゅう", "Concentrate/intensive", "勉強に集中できない。", "べんきょうにしゅうちゅうできない。", "I can't concentrate on studying.", VOC5D2)
V("夜中", "よなか", "Midnight/middle of the night", "昨日、友人と夜中まで電話で話をした。", "きのう、ゆうじんとよなかまででんわではなしをした。", "Yesterday I talked with a friend on the phone until the middle of the night.", VOC5D2)
V("世の中", "よのなか", "The world/society", "世の中には色々な人がいる。", "よのなかにはいろいろなひとがいる。", "There are all kinds of people in the world.", VOC5D2)
V("手間", "てま", "Cumbersome/time and effort", "この作品を作るのには、手間がかかった。", "このさくひんをつくるのには、てまがかかった。", "It took a lot of time and effort to make this work.", VOC5D2)
V("中間", "ちゅうかん", "Mid-term/halfway", "「これとこれの中間のサイズがありますか。」", "「これとこれのちゅうかんのサイズがありますか。」", "\"Do you have a size in between this one and that one?\"", VOC5D2)
V("世間", "せけん", "The public/society", "会社に入って世間のきびしさを知る。", "かいしゃにはいってせけんのきびしさをしる。", "After joining the company, I learned how harsh the world can be.", VOC5D2)
V("人間", "にんげん", "Human/human relations", "人間はだれでも間違える。", "にんげんはだれでもまちがえる。", "Every human makes mistakes.", VOC5D2)
V("昼間", "ひるま", "Daytime", "昼間は仕事で忙しい。", "ひるまはしごとでいそがしい。", "I'm busy with work during the daytime.", VOC5D2)
V("夜間", "やかん", "Night/nighttime", "夜間に工事が行われている。", "やかんにこうじがおこなわれている。", "Construction is being carried out at night.", VOC5D2)
V("週間", "しゅうかん", "Weekly", "週間天気予報を確認した。", "しゅうかんてんきよほうをかくにんした。", "I checked the weekly weather forecast.", VOC5D2)
V("名作", "めいさく", "Masterpiece", "この映画は映画史に残る名作だ。", "このえいがはえいがしにのこるめいさくだ。", "This movie is a masterpiece that will remain in film history.", VOC5D2)
V("作者", "さくしゃ", "Author/creator", "この小説の作者は誰ですか。", "このしょうせつのさくしゃはだれですか。", "Who is the author of this novel?", VOC5D2)
V("作品", "さくひん", "A piece of work", "あまりうまくできなかったが、作品が仕上がった。", "あまりうまくできなかったが、さくひんがしあがった。", "It didn't turn out that well, but I finished the piece.", VOC5D2)
V("作業", "さぎょう", "Work/operation", "この作業が終わったら、次に進みましょう。", "このさぎょうがおわったら、つぎにすすみましょう。", "Once this work is done, let's move on.", VOC5D2)
V("通行", "つうこう", "Pass through/traffic", "この道は工事中で通行できない。", "このみちはこうじちゅうでつうこうできない。", "This road is under construction and impassable.", VOC5D2)
V("一方通行", "いっぽうつうこう", "One way traffic", "この道は一方通行だ。", "このみちはいっぽうつうこうだ。", "This street is one-way.", VOC5D2)
V("通知", "つうち", "Notice/inform", "合格の通知が届いた。", "ごうかくのつうちがとどいた。", "The notice of passing arrived.", VOC5D2)
V("文通", "ぶんつう", "Correspond", "海外の友人と文通している。", "かいがいのゆうじんとぶんつうしている。", "I correspond with a friend overseas.", VOC5D2)
V("一通り", "ひととおり", "Generally/quickly review", "資料に一通り目を通した。", "しりょうにひととおりめをとおした。", "I quickly looked over the materials.", VOC5D2)

# --- Vocabulary Day 3: 一生・用心・見事 ---
VOC5D3 = "vocabulary::w5 vocabulary::w5d3 jlpt::n2"
V("生じる", "しょうじる", "Arise/occur", "この計画には問題が生じる可能性がある。", "このけいかくにはもんだいがしょうじるかのうせいがある。", "There's a possibility that problems will arise with this plan.", VOC5D3)
V("生える", "はえる", "Grow/come up", "あー、こんなところにもカビが生えちゃったよ。", "あー、こんなところにもカビがはえちゃったよ。", "Ugh, mold has grown even in this spot.", VOC5D3)
V("一生", "いっしょう", "A lifetime", "私はあなたを一生愛し続けます。", "わたしはあなたをいっしょうあいしつづけます。", "I will love you for my whole life.", VOC5D3)
V("人生", "じんせい", "One's life", "彼の人生は波乱に満ちていた。", "かれのじんせいははらんにみちていた。", "His life was full of ups and downs.", VOC5D3)
V("生産", "せいさん", "Production", "この工場は自動車を生産している。", "このこうじょうはじどうしゃをせいさんしている。", "This factory produces automobiles.", VOC5D3)
V("生け花", "いけばな", "Flower arrangement", "母は生け花を習っている。", "はははいけばなをならっている。", "My mother is learning flower arrangement.", VOC5D3)
V("生", "なま", "Raw/fresh", "生の魚が苦手な人もいる。", "なまのさかながにがてなひともいる。", "Some people don't like raw fish.", VOC5D3)
V("学力", "がくりょく", "Scholastic ability", "この試験で学力を測る。", "このしけんでがくりょくをはかる。", "This exam measures scholastic ability.", VOC5D3)
V("学習", "がくしゅう", "Study/learning", "毎日少しずつ学習を続けている。", "まいにちすこしずつがくしゅうをつづけている。", "I continue studying little by little every day.", VOC5D3)
V("学者", "がくしゃ", "A scholar", "彼は有名な言語学者だ。", "かれはゆうめいなげんごがくしゃだ。", "He is a famous linguist.", VOC5D3)
V("学問", "がくもん", "Learning/study/academics", "私は学問の道に進みたい。", "わたしはがくもんのみちにすすみたい。", "I want to pursue the path of academics.", VOC5D3)
V("学会", "がっかい", "Academic conference/society", "来月、国際学会に参加する。", "らいげつ、こくさいがっかいにさんかする。", "I will attend an international academic conference next month.", VOC5D3)
V("文学", "ぶんがく", "Literature", "大学で日本文学を学んだ。", "だいがくでにほんぶんがくをまなんだ。", "I studied Japanese literature at university.", VOC5D3)
V("用いる", "もちいる", "Utilize/use", "この実験では新しい方法を用いる。", "このじっけんではあたらしいほうほうをもちいる。", "This experiment uses a new method.", VOC5D3)
V("用語", "ようご", "Terminology/terms", "医学用語を覚えるのは、大変です。", "いがくようごをおぼえるのは、たいへんです。", "Memorizing medical terminology is hard.", VOC5D3)
V("用紙", "ようし", "Form/paper", "申込用紙に記入した。", "もうしこみようしにきにゅうした。", "I filled out the application form.", VOC5D3)
V("用心", "ようじん", "Caution/be aware of", "火の用心を心がける。", "ひのようじんをこころがける。", "I'm careful about fire safety.", VOC5D3)
V("使用", "しよう", "Use/application", "毎日、パソコンを使用している。", "まいにち、パソコンをしようしている。", "I use a computer every day.", VOC5D3)
V("引用", "いんよう", "Quote/citation", "レポートに専門家の言葉を引用した。", "レポートにせんもんかのことばをいんようした。", "I quoted an expert's words in my report.", VOC5D3)
V("通用", "つうよう", "Be generally accepted/pass as", "この切符はどの路線でも通用する。", "このきっぷはどのろせんでもつうようする。", "This ticket is valid on any line.", VOC5D3)
V("急用", "きゅうよう", "Urgent matter", "急用があるので、先に帰ります。", "きゅうようがあるので、さきにかえります。", "I have an urgent matter, so I'll leave early.", VOC5D3)
V("日用品", "にちようひん", "Daily necessities", "スーパーで日用品を買った。", "スーパーでにちようひんをかった。", "I bought daily necessities at the supermarket.", VOC5D3)
V("見学", "けんがく", "Tour/observe/field trip", "工場を見学した。", "こうじょうをけんがくした。", "I toured the factory.", VOC5D3)
V("見事", "みごとな", "Spectacular/excellent", "彼女は見事な演技を見せた。", "かのじょはみごとなえんぎをみせた。", "She gave a spectacular performance.", VOC5D3)
V("見方", "みかた", "Point of view/perspective", "私の父は物の見方が古い。", "わたしのちちはもののみかたがふるい。", "My father's way of looking at things is old-fashioned.", VOC5D3)
V("見出し", "みだし", "Headline", "新聞の見出しを読んだ。", "しんぶんのみだしをよんだ。", "I read the newspaper headline.", VOC5D3)
V("見本", "みほん", "Sample/example", "店で商品の見本を見せてもらった。", "みせでしょうひんのみほんをみせてもらった。", "I was shown a sample of the product at the store.", VOC5D3)
V("見回る", "みまわる", "Patrol/look around", "警備員が夜中に見回っている。", "けいびいんがよなかにみまわっている。", "The security guard patrols in the middle of the night.", VOC5D3)

# --- Vocabulary Day 4: 土地・名字・発売 ---
VOC5D4 = "vocabulary::w5 vocabulary::w5d4 jlpt::n2"
V("地方", "ちほう", "Region/countryside", "東北地方に伝わる昔話を聞いた。", "とうほくちほうにつたわるむかしばなしをきいた。", "I heard an old tale passed down in the Tohoku region.", VOC5D4)
V("地区", "ちく", "District/area", "この地区は静かな住宅街だ。", "このちくはしずかなじゅうたくがいだ。", "This district is a quiet residential area.", VOC5D4)
V("地理", "ちり", "Geography/layout", "このあたりの地理には詳しくないので、道に迷った。", "このあたりのちりにはくわしくないので、みちにまよった。", "I don't know the geography around here well, so I got lost.", VOC5D4)
V("地理学", "ちりがく", "Geology/geography", "大学で地理学を学んでいる。", "だいがくでちりがくをまなんでいる。", "I study geography at university.", VOC5D4)
V("地下", "ちか", "Underground", "地下の駐車場に車を止めた。", "ちかのちゅうしゃじょうにくるまをとめた。", "I parked the car in the underground parking lot.", VOC5D4)
V("地下街", "ちかがい", "Underground mall", "雨の日は地下街を通って駅に行く。", "あめのひはちかがいをとおってえきにいく。", "On rainy days, I go to the station through the underground mall.", VOC5D4)
V("土地", "とち", "Land/lot", "この土地に家を建てる予定だ。", "このとちにいえをたてるよていだ。", "I plan to build a house on this land.", VOC5D4)
V("地元", "じもと", "Local", "私の地元では、この魚は食べない。", "わたしのじもとでは、このさかなはたべない。", "In my hometown, we don't eat this fish.", VOC5D4)
V("地味", "じみな", "Dull/plain/subtle", "彼女はいつも地味な服を着ている。", "かのじょはいつもじみなふくをきている。", "She always wears plain clothes.", VOC5D4)
V("生地", "きじ", "Material/dough", "ピザの生地は小麦粉で作る。", "ピザのきじはこむぎこでつくる。", "Pizza dough is made from flour.", VOC5D4)
V("名所", "めいしょ", "Famous spot/attraction", "京都には観光名所がたくさんある。", "きょうとにはかんこうめいしょがたくさんある。", "Kyoto has many famous tourist spots.", VOC5D4)
V("名人", "めいじん", "Master/expert", "彼は将棋の名人だ。", "かれはしょうぎのめいじんだ。", "He is a master of shogi.", VOC5D4)
V("名物", "めいぶつ", "Local specialty", "納豆は水戸の名物です。", "なっとうはみとのめいぶつです。", "Natto is a local specialty of Mito.", VOC5D4)
V("名字", "みょうじ", "Family name/surname", "結婚して名字が変わった。", "けっこんしてみょうじがかわった。", "My surname changed when I got married.", VOC5D4)
V("本名", "ほんみょう", "Real name", "作家の本名は知らない人が多い。", "さっかのほんみょうはしらないひとがおおい。", "Many people don't know the writer's real name.", VOC5D4)
V("あだ名", "あだな", "Nickname", "学生時代のあだ名で呼ばれた。", "がくせいじだいのあだなでよばれた。", "I was called by my nickname from school days.", VOC5D4)
V("発売", "はつばい", "Sale/release", "新製品が来月発売される。", "しんせいひんがらいげつはつばいされる。", "The new product will be released next month.", VOC5D4)
V("発明", "はつめい", "Invention", "電話の発明者は、一般的にベルだと言われている。", "でんわのはつめいしゃは、いっぱんてきにベルだといわれている。", "The inventor of the telephone is generally said to be Bell.", VOC5D4)
V("発言", "はつげん", "Speech/remark/speak up", "会議で発言する機会がなかった。", "かいぎではつげんするきかいがなかった。", "I didn't have a chance to speak up at the meeting.", VOC5D4)
V("発見", "はっけん", "Discovery", "新しい星が発見された。", "あたらしいほしがはっけんされた。", "A new star was discovered.", VOC5D4)
V("発行", "はっこう", "Issue/publish", "新しい紙幣が発行された。", "あたらしいしへいがはっこうされた。", "New banknotes were issued.", VOC5D4)
V("発生", "はっせい", "Occurrence/outbreak", "事故の発生を防ぐ対策を取る。", "じこのはっせいをふせぐたいさくをとる。", "Measures are taken to prevent accidents from occurring.", VOC5D4)
V("発車", "はっしゃ", "Departure (train/vehicle)", "電車はまもなく発車します。", "でんしゃはまもなくはっしゃします。", "The train will depart shortly.", VOC5D4)
V("会計", "かいけい", "Accounting/bill/checkout", "レストランで会計を済ませた。", "レストランでかいけいをすませた。", "I paid the bill at the restaurant.", VOC5D4)
V("会合", "かいごう", "Meeting/gathering", "町内会の会合に出席した。", "ちょうないかいのかいごうにしゅっせきした。", "I attended the neighborhood association meeting.", VOC5D4)
V("会場", "かいじょう", "Venue/site", "会場までタクシーで行った。", "かいじょうまでタクシーでいった。", "I went to the venue by taxi.", VOC5D4)
V("開会", "かいかい", "Opening of a meeting/event", "大会の開会を宣言した。", "たいかいのかいかいをせんげんした。", "The tournament's opening was declared.", VOC5D4)
V("開会式", "かいかいしき", "Opening ceremony", "オリンピックの開会式を見た。", "オリンピックのかいかいしきをみた。", "I watched the Olympic opening ceremony.", VOC5D4)
V("閉会式", "へいかいしき", "Closing ceremony", "閉会式で選手たちが行進した。", "へいかいしきでせんしゅたちがこうしんした。", "The athletes marched at the closing ceremony.", VOC5D4)
V("大会", "たいかい", "Tournament/assembly", "東京で開かれる大会に出るため上京した。", "とうきょうでひらかれるたいかいにでるためじょうきょうした。", "I went to Tokyo to participate in a tournament held there.", VOC5D4)
V("出会い", "であい", "Encounter/meeting", "あの出会いが人生を変えた。", "あのであいがじんせいをかえた。", "That encounter changed my life.", VOC5D4)

# --- Vocabulary Day 5: 手品・合図・強気 ---
VOC5D5 = "vocabulary::w5 vocabulary::w5d5 jlpt::n2"
V("手当て", "てあて", "Medical treatment/allowance", "けがの手当てをしてもらった。", "けがのてあてをしてもらった。", "I received treatment for my injury.", VOC5D5)
V("手入れ", "ていれ", "Maintenance/care/looking after", "休日に庭の手入れをした。", "きゅうじつににわのていれをした。", "I did yard maintenance on my day off.", VOC5D5)
V("手書き", "てがき", "Handwriting", "パソコンを使わずに手書きであて名を書いた。", "パソコンをつかわずにてがきであてなをかいた。", "I wrote the address by hand without using a computer.", VOC5D5)
V("手作り", "てづくり", "Handmade/home-made", "手作りのケーキをプレゼントした。", "てづくりのケーキをプレゼントした。", "I gave a handmade cake as a present.", VOC5D5)
V("手品", "てじな", "Magic trick", "子どもたちの前で手品を見せた。", "こどもたちのまえでてじなをみせた。", "I showed a magic trick to the children.", VOC5D5)
V("手前", "てまえ", "Before/right in front of", "駅の手前で車を止めた。", "えきのてまえでくるまをとめた。", "I stopped the car just before the station.", VOC5D5)
V("話し手", "はなして", "Speaker", "この授業では話し手の意図を考える。", "このじゅぎょうでははなしてのいとをかんがえる。", "In this class, we consider the speaker's intention.", VOC5D5)
V("聞き手", "ききて", "Listener", "話し方は聞き手によって変える。", "はなしかたはききてによってかえる。", "I change how I speak depending on the listener.", VOC5D5)
V("人手", "ひとで", "Manpower/hands", "忙しくて人手が足りない。", "いそがしくてひとでがたりない。", "We're busy and short-handed.", VOC5D5)
V("手話", "しゅわ", "Sign language", "手話を勉強している。", "しゅわをべんきょうしている。", "I'm studying sign language.", VOC5D5)
V("合計", "ごうけい", "Total/sum", "買い物の合計金額を計算した。", "かいもののごうけいきんがくをけいさんした。", "I calculated the total amount of my shopping.", VOC5D5)
V("合理的", "ごうりてきな", "Rational/logical", "もっと合理的な方法があるはずだ。", "もっとごうりてきなほうほうがあるはずだ。", "There must be a more rational method.", VOC5D5)
V("合同", "ごうどう", "Joint/combined", "二つのチームが合同で練習した。", "ふたつのチームがごうどうでれんしゅうした。", "The two teams practiced jointly.", VOC5D5)
V("集合", "しゅうごう", "Gathering/assembly", "12時にロビーに集合してください。", "12じにロビーにしゅうごうしてください。", "Please gather in the lobby at 12 o'clock.", VOC5D5)
V("都合", "つごう", "Circumstances/convenience", "今週は都合が悪い。", "こんしゅうはつごうがわるい。", "This week doesn't work for me.", VOC5D5)
V("合図", "あいず", "Signal/cue", "合図と同時に走り出した。", "あいずとどうじにはしりだした。", "I started running at the signal.", VOC5D5)
V("合間", "あいま", "Interval/break/spare time", "仕事の合間に家に電話を入れた。", "しごとのあいまにいえにでんわをいれた。", "I called home during a break at work.", VOC5D5)
V("体重", "たいじゅう", "Body weight", "運動を続けているのに体重が増えてしまった。", "うんどうをつづけているのにたいじゅうがふえてしまった。", "Even though I keep exercising, I've gained weight.", VOC5D5)
V("体力", "たいりょく", "Physical strength/stamina", "毎日走って体力をつけている。", "まいにちはしってたいりょくをつけている。", "I run every day to build up my stamina.", VOC5D5)
V("死体", "したい", "Corpse/dead body", "事件現場で死体が発見された。", "じけんげんばでしたいがはっけんされた。", "A body was discovered at the crime scene.", VOC5D5)
V("重体", "じゅうたい", "Serious condition/critical state", "事故で重体になった患者を治療した。", "じこでじゅうたいになったかんじゃをちりょうした。", "I treated a patient who was in critical condition due to an accident.", VOC5D5)
V("強化", "きょうか", "Strengthening/reinforcement", "試合に向けて練習を強化した。", "しあいにむけてれんしゅうをきょうかした。", "I intensified my practice for the match.", VOC5D5)
V("強力", "きょうりょくな", "Powerful/strong", "携帯電話には強力な磁石が使われている。", "けいたいでんわにはきょうりょくなじしゃくがつかわれている。", "A powerful magnet is used in mobile phones.", VOC5D5)
V("強引", "ごういんな", "Pushy/overbearing", "セールスマンに強引に契約させられた。", "セールスマンにごういんにけいやくさせられた。", "I was forced into a contract pushily by the salesman.", VOC5D5)
V("強気", "つよきな", "Aggressive/firm", "彼は交渉で強気な態度を見せた。", "かれはこうしょうでつよきなたいどをみせた。", "He showed an aggressive attitude in the negotiation.", VOC5D5)
V("力強い", "ちからづよい", "Strong/powerful/reassuring", "彼の力強い言葉に勇気づけられた。", "かれのちからづよいことばにゆうきづけられた。", "His powerful words encouraged me.", VOC5D5)

# --- Vocabulary Day 6: 本気・気楽・目安 ---
VOC5D6 = "vocabulary::w5 vocabulary::w5d6 jlpt::n2"
V("本日", "ほんじつ", "Today (formal)", "本日は晴天です。", "ほんじつはせいてんです。", "Today is fine weather.", VOC5D6)
V("本年", "ほんねん", "This year (formal)", "本年もよろしくお願いいたします。", "ほんねんもよろしくおねがいいたします。", "I look forward to working with you again this year.", VOC5D6)
V("本社", "ほんしゃ", "Headquarters/main office", "本社は東京にある。", "ほんしゃはとうきょうにある。", "The headquarters is in Tokyo.", VOC5D6)
V("本店", "ほんてん", "Main store", "このパン屋の本店は京都にある。", "このパンやのほんてんはきょうとにある。", "The main store of this bakery is in Kyoto.", VOC5D6)
V("本人", "ほんにん", "The person themselves", "銀行で本人の確認のため免許証を見せるように言われた。", "ぎんこうでほんにんのかくにんのためめんきょしょうをみせるようにいわれた。", "At the bank, I was asked to show my license to confirm my identity.", VOC5D6)
V("本気", "ほんき", "Serious/earnest", "彼は本気でうそをつくので、信用できない。", "かれはほんきでうそをつくので、しんようできない。", "He lies seriously, so he can't be trusted.", VOC5D6)
V("本来", "ほんらい", "Original/by nature", "彼女が本来の力を出せば、優勝できるでしょう。", "かのじょがほんらいのちからをだせば、ゆうしょうできるでしょう。", "If she shows her true ability, she should be able to win.", VOC5D6)
V("家屋", "かおく", "House/building", "台風で多くの家屋が壊れた。", "たいふうでおおくのかおくがこわれた。", "Many houses were destroyed by the typhoon.", VOC5D6)
V("一家", "いっか", "A family/household", "田中さん一家は、3日前から旅行に出かけたようだ。", "たなかさんいっかは、3にちまえからりょこうにでかけたようだ。", "It seems the Tanaka family went on a trip three days ago.", VOC5D6)
V("芸術家", "げいじゅつか", "An artist", "彼女は有名な芸術家だ。", "かのじょはゆうめいなげいじゅつかだ。", "She is a famous artist.", VOC5D6)
V("読書家", "どくしょか", "A great reader", "祖父はたいへんな読書家だ。", "そふはたいへんなどくしょかだ。", "My grandfather is quite an avid reader.", VOC5D6)
V("作家", "さっか", "A writer/novelist", "彼女は人気の作家だ。", "かのじょはにんきのさっかだ。", "She is a popular writer.", VOC5D6)
V("画家", "がか", "A painter", "彼は有名な画家になった。", "かれはゆうめいながかになった。", "He became a famous painter.", VOC5D6)
V("大家", "おおや", "Landlord", "大家さんに家賃を払った。", "おおやさんにやちんをはらった。", "I paid the rent to the landlord.", VOC5D6)
V("目上", "めうえ", "One's superior/senior", "目上の人には敬語を使う。", "めうえのひとにはけいごをつかう。", "I use polite language with my superiors.", VOC5D6)
V("目下", "めした", "One's junior/subordinate", "彼は目下の人にも丁寧だ。", "かれはめしたのひとにもていねいだ。", "He is polite even to his subordinates.", VOC5D6)
V("目安", "めやす", "Aim/rough estimate/standard", "赤ちゃんの成長の目安は体重の増え方です。", "あかちゃんのせいちょうのめやすはたいじゅうのふえかたです。", "A guideline for a baby's growth is how their weight increases.", VOC5D6)
V("目指す", "めざす", "Aim for", "医者を目指して勉強している。", "いしゃをめざしてべんきょうしている。", "I'm studying with the aim of becoming a doctor.", VOC5D6)
V("目立つ", "めだつ", "Stand out/be conspicuous", "年をとって白髪が目立つようになった。", "としをとってしらががめだつようになった。", "As I've gotten older, my gray hair has become noticeable.", VOC5D6)
V("注目", "ちゅうもく", "Pay attention/focus", "彼のこれからの活躍に注目していこうと思う。", "かれのこれからのかつやくにちゅうもくしていこうとおもう。", "I intend to keep paying attention to his future achievements.", VOC5D6)
V("気体", "きたい", "Gas/vapor", "水は気体、液体、固体に変化する。", "みずはきたい、えきたい、こたいにへんかする。", "Water changes into gas, liquid, and solid.", VOC5D6)
V("気分", "きぶん", "Feeling/mood", "熱が下がってだいぶ気分が良くなった。", "ねつがさがってだいぶきぶんがよくなった。", "My fever went down and I feel much better.", VOC5D6)
V("気味", "きみ", "Sensation/tendency", "最近、疲れ気味だ。", "さいきん、つかれぎみだ。", "I've been feeling somewhat tired lately.", VOC5D6)
V("気楽", "きらくな", "Comfortable/easygoing", "気楽に考えたほうがいい。", "きらくにかんがえたほうがいい。", "It's better to think about it in a relaxed way.", VOC5D6)
V("平気", "へいきな", "Unconcerned/calm/alright", "彼は失敗しても平気な顔をしている。", "かれはしっぱいしてもへいきなかおをしている。", "He looks unbothered even when he fails.", VOC5D6)
V("短気", "たんきな", "Short-tempered", "父は短気な性格だ。", "ちちはたんきなせいかくだ。", "My father has a short temper.", VOC5D6)

# --- Reading extraction (annotated/glossary vocabulary from reading-w5.md) ---
R5D1 = "reading::w5 reading::w5d1 jlpt::n2"
V("足止め", "あしどめ", "Being trapped", "台風で空港に足止めされた。", "たいふうでくうこうにあしどめされた。", "I was stranded at the airport due to the typhoon.", R5D1)
V("損失", "そんしつ", "A loss", "会社は大きな損失を出した。", "かいしゃはおおきなそんしつをだした。", "The company suffered a large loss.", R5D1)
V("火山噴火", "かざんふんか", "A volcanic eruption", "火山噴火のニュースが世界中に伝わった。", "かざんふんかのニュースがせかいじゅうにつたわった。", "News of the volcanic eruption spread around the world.", R5D1)
V("航空輸送網", "こうくうゆそうもう", "An air transportation network", "悪天候で航空輸送網が混乱した。", "あくてんこうでこうくうゆそうもうがこんらんした。", "The air transportation network was thrown into chaos due to bad weather.", R5D1)
V("火山灰", "かざんばい", "Volcanic ashes", "火山灰が街を覆った。", "かざんばいがまちをおおった。", "Volcanic ash covered the town.", R5D1)
V("拡散する", "かくさんする", "To diffuse", "うわさがSNSで拡散した。", "うわさがエスエヌエスでかくさんした。", "The rumor spread through social media.", R5D1)

R5D2 = "reading::w5 reading::w5d2 jlpt::n2"
V("配慮する", "はいりょする", "To give consideration", "環境に配慮した商品を選ぶ。", "かんきょうにはいりょしたしょうひんをえらぶ。", "I choose products that consider the environment.", R5D2)
V("素材", "そざい", "Materials/ingredients", "この服は天然の素材で作られている。", "このふくはてんねんのそざいでつくられている。", "This clothing is made from natural materials.", R5D2)
V("手間をかける", "てまをかける", "To spend more time and effort", "手間をかけてていねいに作った料理だ。", "てまをかけてていねいにつくったりょうりだ。", "This dish was made carefully, with a lot of time and effort.", R5D2)
V("こだわり", "こだわり", "Particular preferences", "このレストランは素材へのこだわりが強い。", "このレストランはそざいへのこだわりがつよい。", "This restaurant has strong particular preferences about ingredients.", R5D2)
V("有機農法", "ゆうきのうほう", "Organic farming", "有機農法で野菜を育てている。", "ゆうきのうほうでやさいをそだてている。", "I grow vegetables using organic farming.", R5D2)
V("栽培する", "さいばいする", "To grow", "この地域ではぶどうを栽培している。", "このちいきではぶどうをさいばいしている。", "Grapes are grown in this region.", R5D2)

R5D3 = "reading::w5 reading::w5d3 jlpt::n2"
V("大麻", "たいま", "Marijuana", "大麻の所持は法律で禁止されている。", "たいまのしょじはほうりつできんしされている。", "Possession of marijuana is prohibited by law.", R5D3)
V("譲渡", "じょうと", "A transfer", "財産の譲渡について弁護士に相談した。", "ざいさんのじょうとについてべんごしにそうだんした。", "I consulted a lawyer about the transfer of assets.", R5D3)
V("所持", "しょじ", "Possession", "銃の所持には許可が必要だ。", "じゅうのしょじにはきょかがひつようだ。", "A permit is required to possess a gun.", R5D3)
V("容疑", "ようぎ", "Suspicion", "男は殺人の容疑で逮捕された。", "おとこはさつじんのようぎでたいほされた。", "The man was arrested on suspicion of murder.", R5D3)
V("逮捕", "たいほ", "An arrest", "警察は容疑者を逮捕した。", "けいさつはようぎしゃをたいほした。", "The police arrested the suspect.", R5D3)
V("認めている", "みとめている", "To admit", "被告は罪を認めている。", "ひこくはつみをみとめている。", "The defendant admits to the crime.", R5D3)
V("違反", "いはん", "Violation of laws", "スピード違反で捕まった。", "スピードいはんでつかまった。", "I was caught for a speeding violation.", R5D3)
V("罰則", "ばっそく", "Penal regulations", "飲酒運転の罰則が厳しくなった。", "いんしゅうんてんのばっそくがきびしくなった。", "Penalties for drunk driving have become stricter.", R5D3)
V("通報", "つうほう", "A report", "火事を見て110番に通報した。", "かじをみて110ばんにつうほうした。", "I saw the fire and reported it to the police.", R5D3)
V("ひき逃げ", "ひきにげ", "A hit and run", "ひき逃げ事件が起きた。", "ひきにげじけんがおきた。", "A hit-and-run incident occurred.", R5D3)
V("飲酒運転", "いんしゅうんてん", "Drunken driving", "飲酒運転は絶対にしてはいけない。", "いんしゅうんてんはぜったいにしてはいけない。", "You must never drive under the influence.", R5D3)
V("うつぶせ", "うつぶせ", "Lying on one's stomach", "男性はうつぶせで倒れていた。", "だんせいはうつぶせでたおれていた。", "The man was lying face-down.", R5D3)
V("血痕", "けっこん", "A bloodstain", "現場に血痕が残っていた。", "げんばにけっこんがのこっていた。", "Bloodstains remained at the scene.", R5D3)
V("身元", "みもと", "One's identity", "遺体の身元はまだわかっていない。", "いたいのみもとはまだわかっていない。", "The identity of the body is still unknown.", R5D3)

R5D4 = "reading::w5 reading::w5d4 jlpt::n2"
V("万歩計", "まんぽけい", "A pedometer", "万歩計をつけて毎日歩いている。", "まんぽけいをつけてまいにちあるいている。", "I wear a pedometer and walk every day.", R5D4)
V("付加機能", "ふかきのう", "An additional feature", "この時計には付加機能がたくさんある。", "このとけいにはふかきのうがたくさんある。", "This watch has many additional features.", R5D4)
V("損なわれる", "そこなわれる", "To be spoiled", "過度な広告で商品のイメージが損なわれた。", "かどなこうこくでしょうひんのイメージがそこなわれた。", "Excessive advertising spoiled the product's image.", R5D4)
V("支持する", "しじする", "To support", "多くの人がその政策を支持している。", "おおくのひとがそのせいさくをしじしている。", "Many people support that policy.", R5D4)
V("手軽な", "てがるな", "Handy and affordable", "手軽な値段で買える商品が人気だ。", "てがるなねだんでかえるしょうひんがにんきだ。", "Products that can be bought at an affordable price are popular.", R5D4)

R5D5 = "reading::w5 reading::w5d5 jlpt::n2"
V("上回る", "うわまわる", "To exceed", "今月の売り上げは予想を上回った。", "こんげつのうりあげはよそうをうわまわった。", "This month's sales exceeded expectations.", R5D5)
V("下回る", "したまわる", "To fall short of", "今年の収穫量は去年を下回った。", "ことしのしゅうかくりょうはきょねんをしたまわった。", "This year's harvest fell short of last year's.", R5D5)
V("割合", "わりあい", "A ratio", "女性の割合が高い職場だ。", "じょせいのわりあいがたかいしょくばだ。", "This is a workplace with a high ratio of women.", R5D5)
V("わずかに／やや", "わずかに／やや", "Slightly/somewhat", "気温は昨日よりわずかに高い。", "きおんはきのうよりわずかにたかい。", "The temperature is slightly higher than yesterday.", R5D5)
V("はるかに／大きく", "はるかに／おおきく", "By far/a lot", "今年の売り上げは去年をはるかに上回った。", "ことしのうりあげはきょねんをはるかにうわまわった。", "This year's sales far exceeded last year's.", R5D5)
V("発火源", "はっかげん", "The cause of the fire", "発火源はたばこの火だとみられている。", "はっかげんはたばこのひだとみられている。", "The cause of the fire is believed to be a cigarette.", R5D5)
V("死傷者", "ししょうしゃ", "Casualties", "事故による死傷者は10人に上った。", "じこによるししょうしゃは10にんにのぼった。", "The number of casualties from the accident reached 10.", R5D5)
V("行為者", "こういしゃ", "A doer", "違反行為者には罰金が科される。", "いはんこういしゃにはばっきんがかされる。", "Fines are imposed on violators.", R5D5)
V("負傷者", "ふしょうしゃ", "An injured person", "事故で負傷者が3人出た。", "じこでふしょうしゃが3にんでた。", "Three people were injured in the accident.", R5D5)

R5D6 = "reading::w5 reading::w5d6 jlpt::n2"
V("エッセイ", "エッセイ", "An essay", "彼女のエッセイはやさしい文体で書かれている。", "かのじょのエッセイはやさしいぶんたいでかかれている。", "Her essays are written in a gentle style.", R5D6)
V("定義", "ていぎ", "A definition", "「幸せ」の定義は人によって違う。", "「しあわせ」のていぎはひとによってちがう。", "The definition of \"happiness\" differs from person to person.", R5D6)
V("称する", "しょうする", "To claim", "彼は専門家と称する人物だった。", "かれはせんもんかとしょうするじんぶつだった。", "He was a person who claimed to be an expert.", R5D6)
V("論じる", "ろんじる", "To deal with/discuss", "この本は現代社会の問題を論じている。", "このほんはげんだいしゃかいのもんだいをろんじている。", "This book discusses issues in modern society.", R5D6)
V("突拍子もない", "とっぴょうしもない", "Crazy and unrealistic", "突拍子もないアイデアだが、面白い。", "とっぴょうしもないアイデアだが、おもしろい。", "It's a crazy idea, but interesting.", R5D6)
V("お勧め", "おすすめ", "Recommended", "この店のラーメンはお勧めです。", "このみせのラーメンはおすすめです。", "This shop's ramen is recommended.", R5D6)

R5D7 = "reading::w5 reading::w5d7 jlpt::n2"
V("震災", "しんさい", "Disaster caused by earthquake", "震災から10年が経った。", "しんさいから10ねんがたった。", "Ten years have passed since the earthquake disaster.", R5D7)
V("展示する", "てんじする", "To display", "美術館で絵画を展示する。", "びじゅつかんでかいがをてんじする。", "Paintings are displayed at the art museum.", R5D7)
V("復興", "ふっこう", "Reconstruction/recovery", "町の復興が進んでいる。", "まちのふっこうがすすんでいる。", "The town's reconstruction is progressing.", R5D7)
V("町並み", "まちなみ", "Streetscape/townscape", "古い町並みが観光客に人気だ。", "ふるいまちなみがかんこうきゃくににんきだ。", "The old townscape is popular with tourists.", R5D7)
V("開催する", "かいさいする", "To hold (an event)", "来月、展覧会を開催する。", "らいげつ、てんらんかいをかいさいする。", "We will hold an exhibition next month.", R5D7)
V("はねられる", "はねられる", "To be hit (by a vehicle)", "女性が車にはねられた。", "じょせいがくるまにはねられた。", "A woman was hit by a car.", R5D7)
V("被告", "ひこく", "The accused/defendant", "被告は無罪を主張した。", "ひこくはむざいをしゅちょうした。", "The defendant claimed innocence.", R5D7)
V("開廷", "かいてい", "The opening of a court session", "裁判が開廷した。", "さいばんがかいていした。", "The trial began.", R5D7)
V("目撃者", "もくげきしゃ", "A witness", "目撃者の証言を聞いた。", "もくげきしゃのしょうげんをきいた。", "I heard the witness's testimony.", R5D7)
V("遮断棒", "しゃだんぼう", "A railroad crossing barrier", "遮断棒が下りて電車が通過した。", "しゃだんぼうがおりてでんしゃがつうかした。", "The crossing barrier came down and the train passed.", R5D7)
V("外来魚", "がいらいぎょ", "A non-native fish", "川に外来魚が増えている。", "かわにがいらいぎょがふえている。", "Non-native fish are increasing in the river.", R5D7)

# --- Listening extraction (聞き取り 第5章 総まとめ問題 — mock JLPT test with real dialogue) ---
L5_1 = "listening::w5 listening::w5-1 jlpt::n2"
V("下ろす", "おろす", "Withdraw (money)", "銀行でお金を下ろした。", "ぎんこうでおかねをおろした。", "I withdrew money from the bank.", L5_1)

L5_2 = "listening::w5 listening::w5-2 jlpt::n2"
V("表向き", "おもてむき", "The official/ostensible reason", "表向きは辞任だが、実は解雇だった。", "おもてむきはじにんだが、じつはかいこだった。", "Officially it was a resignation, but it was actually a dismissal.", L5_2)
V("継ぐ", "つぐ", "To carry on/take over", "息子が父の店を継いだ。", "むすこがちちのみせをついだ。", "The son took over his father's shop.", L5_2)
V("リストラ", "リストラ", "Company restructuring", "不況でリストラされた。", "ふきょうでリストラされた。", "I was laid off due to the recession.", L5_2)
V("豊作を祈願する", "ほうさくをきがんする", "To pray for a bountiful harvest", "神社で豊作を祈願する祭りが行われた。", "じんじゃでほうさくをきがんするまつりがおこなわれた。", "A festival to pray for a bountiful harvest was held at the shrine.", L5_2)
V("田植え", "たうえ", "Rice-planting", "5月に田植えをする。", "5がつにたうえをする。", "Rice-planting is done in May.", L5_2)
V("おみこし", "おみこし", "Portable shrine", "祭りでおみこしをかついだ。", "まつりでおみこしをかついだ。", "I carried the portable shrine at the festival.", L5_2)
V("買い得", "かいどく", "A bargain/a steal", "このセーターは買い得だった。", "このセーターはかいどくだった。", "This sweater was a great deal.", L5_2)
V("題材", "だいざい", "Subject material/theme", "この小説は実話を題材にしている。", "このしょうせつはじつわをだいざいにしている。", "This novel is based on a true story.", L5_2)

L5_3 = "listening::w5 listening::w5-3 jlpt::n2"
V("車イス", "くるまイス", "Wheelchair", "祖母は車イスで生活している。", "そぼはくるまイスでせいかつしている。", "My grandmother lives using a wheelchair.", L5_3)
V("付き添い", "つきそい", "To accompany, to go with", "入院中は家族が付き添いをした。", "にゅういんちゅうはかぞくがつきそいをした。", "Family members accompanied me during my hospital stay.", L5_3)
V("同伴", "どうはん", "Escort/companion", "子ども同伴でも入店できます。", "こどもどうはんでもにゅうてんできます。", "You can enter even accompanied by children.", L5_3)
V("添乗員", "てんじょういん", "Tour guide", "ツアーには添乗員が同行した。", "ツアーにはてんじょういんがどうこうした。", "A tour guide accompanied the tour.", L5_3)
V("介護人", "かいごにん", "Patient care assistant", "祖父の介護人を雇った。", "そふのかいごにんをやとった。", "We hired a caregiver for my grandfather.", L5_3)
V("フレックス会員", "フレックスかいいん", "Flex membership", "フレックス会員なら好きな時に来られる。", "フレックスかいいんならすきなときにこられる。", "As a flex member, you can come whenever you like.", L5_3)

L5_5 = "listening::w5 listening::w5-5 jlpt::n2"
V("吸い込み", "すいこみ", "Suction/vacuuming capacity", "この掃除機は吸い込みが強い。", "このそうじきはすいこみがつよい。", "This vacuum cleaner has strong suction.", L5_5)
V("紙パック", "かみパック", "Paper dust bag", "紙パック式の掃除機を使っている。", "かみパックしきのそうじきをつかっている。", "I use a paper-bag-type vacuum cleaner.", L5_5)
V("お求めやすいお値段", "おもとめやすいおねだん", "An affordable price", "このセーターはお求めやすいお値段です。", "このセーターはおもとめやすいおねだんです。", "This sweater is at an affordable price.", L5_5)
V("価値観", "かちかん", "Values/sense of values", "世代によって価値観が違う。", "せだいによってかちかんがちがう。", "Values differ by generation.", L5_5)
V("洗面化粧台", "せんめんけしょうだい", "Washstand", "部屋に洗面化粧台がついている。", "へやにせんめんけしょうだいがついている。", "There's a washstand in the room.", L5_5)
V("苦労をかける", "くろうをかける", "To be a burden/to cause trouble", "親に苦労をかけたくない。", "おやにくろうをかけたくない。", "I don't want to burden my parents.", L5_5)
V("ぜいたくを言う", "ぜいたくをいう", "To ask (expect) too much", "これ以上ぜいたくを言うつもりはない。", "これいじょうぜいたくをいうつもりはない。", "I don't intend to ask for anything more.", L5_5)

L5_4 = "listening::w5 listening::w5-4 jlpt::n2"
V("うろうろする", "うろうろする", "To wander aimlessly", "道に迷って駅の周りをうろうろした。", "みちにまよってえきのまわりをうろうろした。", "I got lost and wandered around the station.", L5_4)
V("出直す", "でなおす", "To come back/start over", "今日は無理なので、また出直します。", "きょうはむりなので、またでなおします。", "It's not possible today, so I'll come back again.", L5_4)

# --- Grammar Day 1: 信じがたい ---
G5D1 = "grammar::w5 grammar::w5d1 jlpt::n2 type::grammar"
G("〜っこない", "っこない", "explanation", "impossible to (emphatic)",
  [("一日でこの本の文法全部なんて、覚えられっこない。", "いちにちでこのほんのぶんぽうぜんぶなんて、おぼえられっこない。", "It's impossible to memorize all the grammar in this book in one day.")], G5D1)
G("〜っこない", "っこない", "explanation", "impossible to (emphatic)",
  [("今の実力では、試験に受かりっこない。", "いまのじつりょくでは、しけんにうかりっこない。", "It is impossible to pass the test with my current ability.")], G5D1)
G("〜かねない", "かねない", "explanation", "might happen/could possibly (something bad)",
  [("この問題を解決せずに放っておいたら、国際問題になりかねない。", "このもんだいをかいけつせずにほうっておいたら、こくさいもんだいになりかねない。", "If this problem is left unresolved, it could become an international issue.")], G5D1)
G("〜かねない", "かねない", "explanation", "might happen/could possibly (something bad)",
  [("そんなひどいことも、あの人なら言いかねない。", "そんなひどいことも、あのひとならいいかねない。", "If it's him, he might say something that terrible.")], G5D1)
G("〜かねる", "かねる", "explanation", "hard to/cannot (due to hesitation, formal)",
  [("申し訳ありませんが、私にはわかりかねます。", "もうしわけありませんが、わたしにはわかりかねます。", "I am sorry, but I cannot answer that.")], G5D1)
G("〜かねる", "かねる", "explanation", "hard to/cannot (due to hesitation, formal)",
  [("そのようなご依頼は、お引き受けしかねます。", "そのようなごいらいは、おひきうけしかねます。", "I cannot accept that request.")], G5D1)
G("〜がたい", "がたい", "explanation", "difficult to do/hard to feel",
  [("これは信じがたい話だが、事実である。", "これはしんじがたいはなしだが、じじつである。", "This is hard to believe, but it is true.")], G5D1)
G("〜がたい", "がたい", "explanation", "difficult to do/hard to feel",
  [("人が人の命をうばうなんて、許しがたい。", "ひとがひとのいのちをうばうなんて、ゆるしがたい。", "It is unforgivable that a person would take another's life.")], G5D1)

# --- Grammar Day 2: 富士山が見えることから ---
G5D2 = "grammar::w5 grammar::w5d2 jlpt::n2 type::grammar"
G("〜ことから", "ことから", "explanation", "because/from the fact that",
  [("富士山が見えることから、この町は富士見町という名前がついた。", "ふじさんがみえることから、このまちはふじみちょうというなまえがついた。", "Because Mt. Fuji is visible, this town is named Fujimicho.")], G5D2)
G("〜ことから", "ことから", "explanation", "because/from the fact that",
  [("桜の名所であることから、春には花見客が大勢やってくる。", "さくらのめいしょであることから、はるにははなみきゃくがおおぜいやってくる。", "Because this is a famous place for cherry blossoms, many people visit in spring.")], G5D2)
G("〜ことだから", "ことだから", "explanation", "knowing that/since it is X (person's character)",
  [("いつも遅刻する彼のことだから、もうすぐ現れるだろう。", "いつもちこくするかれのことだから、もうすぐあらわれるだろう。", "Knowing him, since he's always late, he should be here soon.")], G5D2)
G("〜ことだから", "ことだから", "explanation", "knowing that/since it is X (person's character)",
  [("親切な林さんのことだから、頼めば手伝ってくれるよ。", "しんせつなはやしさんのことだから、たのめばてつだってくれるよ。", "Knowing kind Hayashi-san, if you ask, he will help.")], G5D2)
G("〜ことなく", "ことなく", "explanation", "without doing (formal)",
  [("雨は休むことなく降り続いた。", "あめはやすむことなくふりつづいた。", "The rain continued without stopping.")], G5D2)
G("〜ことなく", "ことなく", "explanation", "without doing (formal)",
  [("時は止まることなく流れる。", "ときはとまることなくながれる。", "Time flows without stopping.")], G5D2)
G("〜ないことには", "ないことには", "explanation", "unless (X happens, Y cannot)",
  [("やってみないことには、できるかどうかわからない。", "やってみないことには、できるかどうかわからない。", "I don't know if I can do it unless I try.")], G5D2)
G("〜ないことには", "ないことには", "explanation", "unless (X happens, Y cannot)",
  [("実物を見ないことには、買う気にはなれない。", "じつぶつをみないことには、かうきにはなれない。", "I don't feel like buying it until I see it.")], G5D2)

# --- Grammar Day 3: あるだけましだ ---
G5D3 = "grammar::w5 grammar::w5d3 jlpt::n2 type::grammar"
G("〜(な)ら当然だ／当たり前だ", "(な)らとうぜんだ／あたりまえだ", "explanation", "it is natural that...",
  [("ひどいことばかり言ったので、彼女に嫌われて当然だ。", "ひどいことばかりいったので、かのじょにきらわれてとうぜんだ。", "Since you said so many nasty things, it's natural she hates you.")], G5D3)
G("〜(な)ら当然だ／当たり前だ", "(な)らとうぜんだ／あたりまえだ", "explanation", "it is natural that...",
  [("相手のチームは弱い。勝って当たり前だ。", "あいてのチームはよわい。かってあたりまえだ。", "The other team is weak. It's only natural to win.")], G5D3)
G("〜もの／もっともだ", "もの／もっともだ", "explanation", "it is natural/reasonable",
  [("君が裏切ったのだから、彼女が怒るのももっともだ。", "きみがうらぎったのだから、かのじょがおこるのももっともだ。", "Since you betrayed her, it's natural she is angry.")], G5D3)
G("〜もの／もっともだ", "もの／もっともだ", "explanation", "it is natural/reasonable",
  [("あなたがそう言うのはもっともだ。", "あなたがそういうのはもっともだ。", "It is natural for you to say that.")], G5D3)
G("〜(も)同然だ", "(も)どうぜんだ", "explanation", "virtually the same as",
  [("この車は中古車といっても新品も同然だ。", "このくるまはちゅうこしゃといってもしんぴんもどうぜんだ。", "Although this is a used car, it is virtually new.")], G5D3)
G("〜(も)同然だ", "(も)どうぜんだ", "explanation", "virtually the same as",
  [("彼の財産はないも同然だ。", "かれのざいさんはないもどうぜんだ。", "He virtually has no assets.")], G5D3)
G("〜だけましだ", "だけましだ", "explanation", "better than nothing/at least",
  [("給料が減ったけれど、首にならないだけましだ。", "きゅうりょうがへったけれど、くびにならないだけましだ。", "My salary decreased, but at least I didn't get fired.")], G5D3)
G("〜だけましだ", "だけましだ", "explanation", "better than nothing/at least",
  [("狭くて高いけれど、便利なだけましだ。", "せまくてたかいけれど、べんりなだけましだ。", "It's small and expensive, but at least it's convenient.")], G5D3)

# --- Grammar Day 4: 選手だっただけに ---
G5D4 = "grammar::w5 grammar::w5d4 jlpt::n2 type::grammar"
G("〜だけあって／〜だけに／〜だけのことはある", "だけあって／だけに／だけのことはある", "explanation", "precisely because/just as expected",
  [("一流ホテルだけあって快適だった。", "いちりゅうホテルだけあってかいてきだった。", "As expected of a first-rate hotel, it was comfortable.")], G5D4)
G("〜だけあって／〜だけに／〜だけのことはある", "だけあって／だけに／だけのことはある", "explanation", "precisely because/just as expected",
  [("このバッグは安いだけにすぐに壊れてしまった。", "このバッグはやすいだけにすぐにこわれてしまった。", "Just as you'd expect from a cheap bag, it broke immediately.")], G5D4)
G("〜だけあって／〜だけに／〜だけのことはある", "だけあって／だけに／だけのことはある", "explanation", "precisely because/just as expected",
  [("このいすは丈夫だ。高かっただけのことはある。", "このいすはじょうぶだ。たかかっただけのことはある。", "This chair is sturdy. It was a worthwhile investment even though it was expensive.")], G5D4)
G("〜ばかりか／〜ばかりでなく", "ばかりか／ばかりでなく", "explanation", "not only... but also...",
  [("あの人は学校の成績がいいばかりかスポーツもできる。", "あのひとはがっこうのせいせきがいいばかりかスポーツもできる。", "He is not only good at his school work, but also sports.")], G5D4)
G("〜ばかりか／〜ばかりでなく", "ばかりか／ばかりでなく", "explanation", "not only... but also...",
  [("このあたりは、空気ばかりでなく水も汚染されている。", "このあたりは、くうきばかりでなくみずもおせんされている。", "In this area, not only is the air polluted, but so is the water.")], G5D4)
G("〜ばかりに", "ばかりに", "explanation", "just because of... (negative result)",
  [("あの飛行機に乗ったばかりに、彼は死んだ。", "あのひこうきにのったばかりに、かれはしんだ。", "Just because he took that plane, he died.")], G5D4)
G("〜ばかりに", "ばかりに", "explanation", "just because of... (negative result)",
  [("英語の先生が嫌いなばかりに、英語も嫌いになってしまった。", "えいごのせんせいがきらいなばかりに、えいごもきらいになってしまった。", "Because I disliked the English teacher, I grew to dislike English.")], G5D4)
G("〜のみならず", "のみならず", "explanation", "not only... but also... (formal)",
  [("その映画は日本のみならず、外国でもよく知られている。", "そのえいがはにほんのみならず、がいこくでもよくしられている。", "The film is well known not only in Japan but also overseas.")], G5D4)
G("〜のみならず", "のみならず", "explanation", "not only... but also... (formal)",
  [("料理は味が良いのみならず、見た目も美しい。", "りょうりはあじがよいのみならず、みためもうつくしい。", "The food is not only delicious, but also looks beautiful.")], G5D4)
G("〜のみならず", "のみならず", "explanation", "not only... but also... (formal)",
  [("子どものみか大人もこのゲームにはまっている。", "こどものみかおとなもこのゲームにはまっている。", "Not only children but also adults are into this TV game.")], G5D4)

# --- Grammar Day 5: 飲もうではないか ---
G5D5 = "grammar::w5 grammar::w5d5 jlpt::n2 type::grammar"
G("〜ではないか／〜じゃないか", "ではないか／じゃないか", "explanation", "let's/why don't we (strong invitation/will)",
  [("今日はお祝いだ。みんなで飲もうではないか。", "きょうはおいわいだ。みんなでのもうではないか。", "It's a celebration today. Let's all drink together!")], G5D5)
G("〜ではないか／〜じゃないか", "ではないか／じゃないか", "explanation", "let's/why don't we (strong invitation/will)",
  [("誰もやらないなら、ぼくがやってみようじゃないか。", "だれもやらないなら、ぼくがやってみようじゃないか。", "If no one else will do it, I'll try it!")], G5D5)
G("〜ようがない", "ようがない", "explanation", "no way to do (no method or means)",
  [("何と言ったらいいのか、言いようがない。", "なんといったらいいのか、いいようがない。", "I don't know how to express it (no words for it).")], G5D5)
G("〜ようがない", "ようがない", "explanation", "no way to do (no method or means)",
  [("この作文は日本語がめちゃくちゃで直しようがない。", "このさくぶんはにほんごがめちゃくちゃでなおしようがない。", "This essay's Japanese is such a mess, there is no way to fix it.")], G5D5)
G("〜かのようだ", "かのようだ", "explanation", "as if",
  [("まるで空が泣いているかのようだ。", "まるでそらがないているかのようだ。", "It is as if the sky is crying.")], G5D5)
G("〜かのようだ", "かのようだ", "explanation", "as if",
  [("怖いものでも見たかのように、彼女は震えていた。", "こわいものでもみたかのように、かのじょはふるえていた。", "She was shivering as if she had seen something frightening.")], G5D5)
G("〜そうにない／〜そうもない", "そうにない／そうもない", "explanation", "not likely to (little to no possibility)",
  [("最近仕事がすごく忙しくて、同窓会に行けそうにないよ。", "さいきんしごとがすごくいそがしくて、どうそうかいにいけそうにないよ。", "I'm so busy at work, I don't think I can go to the reunion.")], G5D5)
G("〜そうにない／〜そうもない", "そうにない／そうもない", "explanation", "not likely to (little to no possibility)",
  [("できそうもないことを、できると言ってしまって後悔している。", "できそうもないことを、できるといってしまってこうかいしている。", "I regret saying I could do something that I probably couldn't.")], G5D5)

# --- Grammar Day 6: 事実に基づいて ---
G5D6 = "grammar::w5 grammar::w5d6 jlpt::n2 type::grammar"
G("〜に際して", "にさいして", "explanation", "upon/when (formal)",
  [("お申し込みに際しては、写真が必要となります。", "おもうしこみにさいしては、しゃしんがひつようとなります。", "A photograph is required when applying.")], G5D6)
G("〜に際して", "にさいして", "explanation", "upon/when (formal)",
  [("A氏は日本を訪問するに際し、喜びを語った。", "エーしはにほんをほうもんするにさいし、よろこびをかたった。", "Mr. A expressed his joy upon visiting Japan.")], G5D6)
G("〜に基づいて", "にもとづいて", "explanation", "based on (a rule, plan, or experience)",
  [("この工事は市の計画に基づいて進められます。", "このこうじはしのけいかくにもとづいてすすめられます。", "This construction is proceeding based on the city's plan.")], G5D6)
G("〜に基づいて", "にもとづいて", "explanation", "based on (a rule, plan, or experience)",
  [("長年の経験に基づき新入社員を教育する。", "ながねんのけいけんにもとづきしんにゅうしゃいんをきょういくする。", "I train new employees based on my many years of experience.")], G5D6)
G("〜に応じて", "におうじて", "explanation", "in response to/depending on",
  [("ソフトは、必要に応じてダウンロードしてください。", "ソフトは、ひつようにおうじてダウンロードしてください。", "Please download the software as necessary.")], G5D6)
G("〜に応じて", "におうじて", "explanation", "in response to/depending on",
  [("テスト結果に基づき、能力に応じたクラスに分けられます。", "テストけっかにもとづき、のうりょくにおうじたクラスにわけられます。", "Based on your test results, you will be assigned to a class that matches your ability.")], G5D6)
G("〜の下で", "のもとで", "explanation", "under (influence or guidance of)",
  [("子どもたちが青空の下で元気に遊んでいる。", "こどもたちがあおぞらのもとでげんきにあそんでいる。", "Children are playing cheerfully under the blue sky.")], G5D6)
G("〜の下で", "のもとで", "explanation", "under (influence or guidance of)",
  [("田中先生のご指導の下、研究論文を書いています。", "たなかせんせいのごしどうのもと、けんきゅうろんぶんをかいています。", "I am writing my research paper under the guidance of Mr. Tanaka.")], G5D6)

# --- Grammar Bonus: 敬語 (Keigo) — ほかの人について話す① ---
G5KEIGO = "grammar::w5 grammar::w5dExtra jlpt::n2 type::keigo"
G("お呼びです", "およびです", "explanation", "keigo for 呼んでいる (someone is calling for you, respectful)",
  [("社長がお呼びです。", "しゃちょうがおよびです。", "The president is calling for you."),
   ("社長が呼んでるよ。", "しゃちょうがよんでるよ。", "The president is calling for you.")], G5KEIGO)
G("ご研究です／ご研究なさっています", "ごけんきゅうです／ごけんきゅうなさっています", "explanation", "keigo for 研究している (someone is researching, respectful)",
  [("先生は生物学をご研究なさっています。", "せんせいはせいぶつがくをごけんきゅうなさっています。", "The professor is researching biology."),
   ("先生は生物学を研究しているよ。", "せんせいはせいぶつがくをけんきゅうしているよ。", "The professor is researching biology.")], G5KEIGO)

# =====================================================================
# GRAMMAR_DATA_MARKER
# =====================================================================


def csv_escape(html):
    return html.replace('\t', ' ').replace('\n', ' ').strip()


def build_vocab_tsv():
    lines = [
        "#separator:tab",
        "#html:true",
        "#columns:Front\tBack\tTags",
        "# Week 5 (Sou Matome N2) — Japanese vocabulary: Kanji/Vocabulary/Reading/Listening words",
    ]
    for c in vocab_cards:
        front = f'<div class="front-main">{c["word"]}</div><div class="front-example-sentence-1">{c["sentence"]}</div>'
        back = (f'<div class="back-main-reading">{c["reading"]}</div>'
                f'<div class="back-main-english">{c["meaning"]}</div>'
                f'<div class="back-example-sentence-1-reading">{c["sreading"]}</div>'
                f'<div class="back-example-sentence-1-english">{c["strans"]}</div>')
        lines.append(f'{csv_escape(front)}\t{csv_escape(back)}\t{c["tags"]}')
    return "\n".join(lines) + "\n"


def build_grammar_tsv():
    lines = [
        "#separator:tab",
        "#html:true",
        "#columns:Front\tBack\tTags",
        "# Week 5 (Sou Matome N2) — Japanese grammar and usage: Grammar/Reading/Listening patterns",
    ]
    for c in grammar_cards:
        meaning_cls = "back-main-english" if c["meaning_class"] == "english" else "back-main-english-explanation"
        front = f'<div class="front-main">{c["front_main"]}</div>'
        back = f'<div class="back-main-reading">{c["reading"]}</div><div class="{meaning_cls}">{c["meaning"]}</div>'
        for i, (jp, reading, en) in enumerate(c["sentences"], start=1):
            front += f'<div class="front-example-sentence-{i}">{jp}</div>'
            back += f'<div class="back-example-sentence-{i}-reading">{reading}</div><div class="back-example-sentence-{i}-english">{en}</div>'
        lines.append(f'{csv_escape(front)}\t{csv_escape(back)}\t{c["tags"]}')
    return "\n".join(lines) + "\n"


CSS = """
.card {
    font-family: 'Hiragino Kaku Gothic ProN','Hiragino Sans','Yu Gothic Medium','Yu Gothic','Noto Sans JP','Meiryo',sans-serif;
    text-align: center;
    color: #1f1f1f;
    background-color: #fafafa;
    font-size: 20px;
}

div {
    padding-bottom: 2vh;
}

.front-main {
    font-size: 30px;
}

hr#answer {
    max-width: 92vw;
    margin: 3vh auto;
    border: none;
    border-top: 1px solid #ccc;
}
"""

QFMT = "{{Front}}"
AFMT = '{{FrontSide}}\n<hr id="answer">\n{{Back}}'


def make_model(model_id, name):
    return genanki.Model(
        model_id, name,
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{"name": "Card 1", "qfmt": QFMT, "afmt": AFMT}],
        css=CSS,
    )


def build_apkg(tsv_text, deck_id, deck_name, model, out_path):
    deck = genanki.Deck(deck_id, deck_name)
    lines = [l for l in tsv_text.split("\n") if l and not l.startswith("#")]
    for line in lines:
        parts = line.split("\t")
        assert len(parts) == 3, f"bad row: {line!r}"
        front, back, tags = parts
        note = genanki.Note(model=model, fields=[front, back], tags=tags.split())
        deck.add_note(note)
    genanki.Package(deck).write_to_file(out_path)
    return len(lines)


def validate_vocab():
    errs = []
    seen_fronts = {}
    for i, c in enumerate(vocab_cards):
        word, reading, sentence = c["word"], c["reading"], c["sentence"]
        # leaked-reading bug: word != reading, but reading appears parenthesized inside word
        if word != reading and reading and reading in word and re.search(r'[（(][^（()）]*' + re.escape(reading) + r'[^（()）]*[)）]', word):
            errs.append(f"vocab[{i}] possible leaked reading in front-main: word={word!r} reading={reading!r}")
        if "jlpt::n2" not in c["tags"].split():
            errs.append(f"vocab[{i}] missing jlpt::n2 tag: {c['tags']!r} word={word!r}")
        # kanji-in-word-must-appear-in-sentence check (skip words with no kanji, and skip
        # grouped-synonym words like "A／B" where only one variant needs to appear)
        kanji_chars = [ch for ch in re.sub(r'[（(].*?[)）]', '', word) if '一' <= ch <= '鿿']
        if kanji_chars and '／' not in word and not any(ch in sentence for ch in kanji_chars):
            errs.append(f"vocab[{i}] word's kanji not found in sentence: word={word!r} sentence={sentence!r}")
        key = (c["word"], c["sentence"])
        if key in seen_fronts:
            errs.append(f"vocab[{i}] duplicate front content with vocab[{seen_fronts[key]}]: {key!r}")
        seen_fronts[key] = i
    return errs


def validate_grammar():
    errs = []
    subtypes = {"grammar", "keigo", "contrast", "contraction", "idiom"}
    for i, c in enumerate(grammar_cards):
        tagset = set(c["tags"].split())
        if "jlpt::n2" not in tagset:
            errs.append(f"grammar[{i}] missing jlpt::n2: {c['tags']!r}")
        type_tags = [t for t in tagset if t.startswith("type::")]
        if len(type_tags) != 1:
            errs.append(f"grammar[{i}] needs exactly 1 type:: tag, got {type_tags}: front={c['front_main']!r}")
        elif type_tags[0].split("::")[1] not in subtypes:
            errs.append(f"grammar[{i}] unknown subtype: {type_tags}")
    return errs


if __name__ == "__main__":
    import os
    errs = validate_vocab() + validate_grammar()
    if errs:
        print(f"VALIDATION ERRORS ({len(errs)}):")
        for e in errs[:50]:
            print(" -", e)
        if len(errs) > 50:
            print(f"  ... and {len(errs) - 50} more")
    else:
        print("Validation OK.")

    print(f"vocab_cards: {len(vocab_cards)}")
    print(f"grammar_cards: {len(grammar_cards)}")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../anki
    vocab_tsv = build_vocab_tsv()
    grammar_tsv = build_grammar_tsv()

    with open(os.path.join(base, "week5-v3-vocabulary.tsv"), "w", encoding="utf-8") as f:
        f.write(vocab_tsv)
    with open(os.path.join(base, "week5-v3-grammar-usage.tsv"), "w", encoding="utf-8") as f:
        f.write(grammar_tsv)
    print("Wrote TSVs.")

    if not errs:
        model1 = make_model(MODEL1_ID, "Japanese vocabulary")
        model2 = make_model(MODEL2_ID, "Japanese grammar and usage")
        n1 = build_apkg(vocab_tsv, DECK1_ID, "Japanese N2 Vocabulary", model1,
                         os.path.join(base, "week5-v3-vocabulary.apkg"))
        n2 = build_apkg(grammar_tsv, DECK2_ID, "Japanese N2 Grammar & Usage", model2,
                         os.path.join(base, "week5-v3-grammar-usage.apkg"))
        print(f"Wrote apkg: vocabulary={n1} notes, grammar-usage={n2} notes")
