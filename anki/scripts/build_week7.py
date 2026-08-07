#!/usr/bin/env python3
"""Build Week 7 Anki TSV/apkg files (Deck 1 Vocabulary, Deck 2 Grammar & Usage).

Follows specs/anki-tsv-generation-process.md, specs/anki-note-type-vocabulary.md,
specs/anki-note-type-grammar-and-usage.md. Run from repo root:

    .venv/bin/python anki/scripts/build_week7.py

Note: Week 7 has no reading-w7.md or listening-w7.md (both source books stop before
Week 7 -- confirmed, not an oversight; Week 6 already lost listening, this week loses
reading too). This week's decks are built from Kanji + Vocabulary + Grammar only.
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

# --- Kanji Day 1: 求人・募集 ---
# 給与 listed under both 給 and 与 (within-day Kanji-Kanji duplicate) -- kept under 給, skipped under 与.
K7D1 = "kanji::w7 kanji::w7d1 jlpt::n2"
V("求人", "きゅうじん", "Help wanted", "求人広告を見てこの会社に応募した。", "きゅうじんこうこくをみてこのかいしゃにおうぼした。", "I applied to this company after seeing a job ad.", K7D1)
V("要求", "ようきゅう", "Demand/request", "労働組合が賃上げを要求した。", "ろうどうくみあいがちんあげをようきゅうした。", "The labor union demanded a pay raise.", K7D1)
V("求める", "もとめる", "Demand/request", "会社に改善を求める手紙を書いた。", "かいしゃにかいぜんをもとめるてがみをかいた。", "I wrote a letter to the company demanding improvement.", K7D1)
V("簡単", "かんたんな", "Easy/simple", "この料理は簡単に作れる。", "このりょうりはかんたんにつくれる。", "This dish can be made easily.", K7D1)
V("単語", "たんご", "Word", "毎日新しい単語を覚える。", "まいにちあたらしいたんごをおぼえる。", "I learn new words every day.", K7D1)
V("単位", "たんい", "Unit/credit", "卒業に必要な単位を取った。", "そつぎょうにひつようなたんいをとった。", "I earned the credits needed to graduate.", K7D1)
V("単なる", "たんなる", "Mere/simple", "単なるうわさにすぎない。", "たんなるうわさにすぎない。", "It's nothing more than a mere rumor.", K7D1)
V("許可", "きょか", "Permission", "駐車の許可をもらった。", "ちゅうしゃのきょかをもらった。", "I got permission to park.", K7D1)
V("免許", "めんきょ", "Permit/license", "運転免許を取った。", "うんてんめんきょをとった。", "I got a driver's license.", K7D1)
V("給料", "きゅうりょう", "Wage/salary", "毎月25日に給料をもらう。", "まいつき25にちにきゅうりょうをもらう。", "I get paid on the 25th of every month.", K7D1)
V("供給", "きょうきゅう", "Supply/provision", "水の供給が止まった。", "みずのきょうきゅうがとまった。", "The water supply stopped.", K7D1)
V("給与", "きゅうよ", "Allowance", "給与明細を確認した。", "きゅうよめいさいをかくにんした。", "I checked my pay statement.", K7D1)
V("月給", "げっきゅう", "Monthly wage", "月給制の会社で働いている。", "げっきゅうせいのかいしゃではたらいている。", "I work at a company with a monthly salary system.", K7D1)
V("週給", "しゅうきゅう", "Weekly wage", "このアルバイトは週給で支払われる。", "このアルバイトはしゅうきゅうでしはらわれる。", "This part-time job pays weekly.", K7D1)
V("日給", "にっきゅう", "Daily wage", "日給1万円の仕事を見つけた。", "にっきゅう1まんえんのしごとをみつけた。", "I found a job with a daily wage of 10,000 yen.", K7D1)
V("与える", "あたえる", "Give/present", "子どもに影響を与える言葉に気をつける。", "こどもにえいきょうをあたえることばにきをつける。", "Be careful with words that influence children.", K7D1)
V("応用", "おうよう", "Practical use/application", "基礎を応用して問題を解く。", "きそをおうようしてもんだいをとく。", "I apply the basics to solve the problem.", K7D1)
V("応じる", "おうじる", "Respond", "相談に応じます。", "そうだんにおうじます。", "I will respond to consultations.", K7D1)
V("課", "か", "Lesson/section", "総務課に配属された。", "そうむかにはいぞくされた。", "I was assigned to the general affairs section.", K7D1)
V("日課", "にっか", "Daily lesson/task", "散歩が私の日課だ。", "さんぽがわたしのにっかだ。", "Walking is my daily routine.", K7D1)
V("課程", "かてい", "Course/curriculum", "博士課程に進んだ。", "はかせかていにすすんだ。", "I advanced to the doctoral program.", K7D1)
V("過程", "かてい", "Process/course", "成長の過程を見守る。", "せいちょうのかていをみまもる。", "I watch over the process of growth.", K7D1)
V("程度", "ていど", "Degree/amount", "ある程度の知識が必要だ。", "あるていどのちしきがひつようだ。", "A certain degree of knowledge is necessary.", K7D1)
V("日程", "にってい", "Schedule", "旅行の日程を決めた。", "りょこうのにっていをきめた。", "I decided on the trip's schedule.", K7D1)
V("制度", "せいど", "System", "新しい年金制度が始まった。", "あたらしいねんきんせいどがはじまった。", "A new pension system began.", K7D1)
V("制限", "せいげん", "Restriction/limitation", "速度制限を守る。", "そくどせいげんをまもる。", "I obey the speed limit.", K7D1)
V("制作", "せいさく", "Work/production", "映画の制作に携わった。", "えいがのせいさくにたずさわった。", "I was involved in the production of the movie.", K7D1)
V("体制", "たいせい", "System/structure", "会社の体制が変わった。", "かいしゃのたいせいがかわった。", "The company's organizational structure changed.", K7D1)
V("講座", "こうざ", "Class/course", "日本語の講座に通っている。", "にほんごのこうざにかよっている。", "I attend a Japanese language course.", K7D1)
V("講義", "こうぎ", "Lecture", "大学で経済学の講義を受けた。", "だいがくでけいざいがくのこうぎをうけた。", "I took an economics lecture at university.", K7D1)
V("講演", "こうえん", "Lecture", "有名な学者の講演を聞いた。", "ゆうめいながくしゃのこうえんをきいた。", "I listened to a lecture by a famous scholar.", K7D1)
V("講師", "こうし", "Lecturer", "彼女はこの講座の講師だ。", "かのじょはこのこうざのこうしだ。", "She is the lecturer for this course.", K7D1)
V("初級", "しょきゅう", "Beginning level", "初級クラスから始めた。", "しょきゅうクラスからはじめた。", "I started from the beginner class.", K7D1)
V("中級", "ちゅうきゅう", "Intermediate level", "中級レベルの教材を使っている。", "ちゅうきゅうレベルのきょうざいをつかっている。", "I'm using intermediate-level materials.", K7D1)
V("上級", "じょうきゅう", "Advanced level", "上級コースに進んだ。", "じょうきゅうコースにすすんだ。", "I advanced to the upper-level course.", K7D1)
V("高級", "こうきゅう", "High class/grade", "高級レストランで食事をした。", "こうきゅうレストランでしょくじをした。", "I dined at a high-class restaurant.", K7D1)
V("基本", "きほん", "Foundation/basics", "基本をしっかり学ぶ。", "きほんをしっかりまなぶ。", "I firmly learn the basics.", K7D1)
V("基礎", "きそ", "Foundation/groundwork", "家の基礎工事が始まった。", "いえのきそこうじがはじまった。", "The house's foundation work began.", K7D1)
V("基準", "きじゅん", "Standard/criterion", "採用の基準を決めた。", "さいようのきじゅんをきめた。", "We decided on the hiring criteria.", K7D1)
V("基地", "きち", "Base", "軍の基地がこの町にある。", "ぐんのきちがこのまちにある。", "There is a military base in this town.", K7D1)
V("指導", "しどう", "Leadership/guidance", "先生の指導を受ける。", "せんせいのしどうをうける。", "I receive guidance from the teacher.", K7D1)
V("導入", "どうにゅう", "Introduction", "新しいシステムを導入した。", "あたらしいシステムをどうにゅうした。", "We introduced a new system.", K7D1)
V("導く", "みちびく", "Lead", "成功へと導く。", "せいこうへとみちびく。", "Lead to success.", K7D1)

# --- Kanji Day 2: 掲示板・地域新聞 ---
# 公園 (already carded week6 kanji d4) skipped as a cross-week duplicate.
K7D2 = "kanji::w7 kanji::w7d2 jlpt::n2"
V("校庭", "こうてい", "School playground", "校庭でサッカーをした。", "こうていでサッカーをした。", "I played soccer in the schoolyard.", K7D2)
V("家庭", "かてい", "Home/family", "家庭を大切にする。", "かていをたいせつにする。", "I value my family.", K7D2)
V("庭", "にわ", "Garden", "庭に花を植えた。", "にわにはなをうえた。", "I planted flowers in the garden.", K7D2)
V("教育", "きょういく", "Education", "子どもに教育を受けさせる。", "こどもにきょういくをうけさせる。", "I have my child receive an education.", K7D2)
V("体育", "たいいく", "Physical education", "体育の授業でバスケットボールをした。", "たいいくのじゅぎょうでバスケットボールをした。", "We played basketball in P.E. class.", K7D2)
V("育つ", "そだつ", "Grow", "この子は健康に育った。", "このこはけんこうにそだった。", "This child grew up healthy.", K7D2)
V("育てる", "そだてる", "Raise/bring up", "花を大切に育てている。", "はなをたいせつにそだてている。", "I'm carefully raising the flowers.", K7D2)
V("猫", "ねこ", "Cat", "猫を一匹飼っている。", "ねこをいっぴきかっている。", "I keep one cat.", K7D2)
V("探検", "たんけん", "Exploration", "洞窟を探検した。", "どうくつをたんけんした。", "I explored the cave.", K7D2)
V("探す", "さがす", "Search/look for", "なくした鍵を探した。", "なくしたかぎをさがした。", "I searched for my lost key.", K7D2)
V("探る", "さぐる", "Probe into/search", "相手の本音を探る。", "あいてのほんねをさぐる。", "I probe for the other person's true feelings.", K7D2)
V("灰", "はい", "Ash", "たばこの灰が落ちた。", "たばこのはいがおちた。", "Cigarette ash fell.", K7D2)
V("灰色", "はいいろ", "Gray", "空が灰色の雲で覆われた。", "そらがはいいろのくもでおおわれた。", "The sky was covered with gray clouds.", K7D2)
V("灰皿", "はいざら", "Ashtray", "テーブルに灰皿を置いた。", "テーブルにはいざらをおいた。", "I put an ashtray on the table.", K7D2)
V("車輪", "しゃりん", "Wheel", "自転車の車輪が壊れた。", "じてんしゃのしゃりんがこわれた。", "The bicycle's wheel broke.", K7D2)
V("指輪", "ゆびわ", "Ring", "彼女に指輪をプレゼントした。", "かのじょにゆびわをプレゼントした。", "I gave her a ring as a present.", K7D2)
V("首輪", "くびわ", "Collar", "犬に首輪をつけた。", "いぬにくびわをつけた。", "I put a collar on the dog.", K7D2)
V("今晩", "こんばん", "Tonight", "今晩は雨が降るそうだ。", "こんばんはあめがふるそうだ。", "It seems it will rain tonight.", K7D2)
V("毎晩", "まいばん", "Every night", "毎晩、日記を書いている。", "まいばん、にっきをかいている。", "I write in my diary every night.", K7D2)
V("晩御飯", "ばんごはん", "Dinner", "家族で晩御飯を食べた。", "かぞくでばんごはんをたべた。", "I had dinner with my family.", K7D2)
V("劇", "げき", "Drama/play", "学校で劇を発表した。", "がっこうでげきをはっぴょうした。", "We performed a play at school.", K7D2)
V("劇団", "げきだん", "Theatrical company", "有名な劇団の公演を見た。", "ゆうめいなげきだんのこうえんをみた。", "I saw a performance by a famous theater company.", K7D2)
V("劇場", "げきじょう", "Theater", "劇場でミュージカルを見た。", "げきじょうでミュージカルをみた。", "I watched a musical at the theater.", K7D2)
V("演劇", "えんげき", "Theatrical play", "大学で演劇部に入っていた。", "だいがくでえんげきぶにはいっていた。", "I was in the drama club at university.", K7D2)
V("公共", "こうきょう", "Public/communal", "公共の場では静かにする。", "こうきょうのばではしずかにする。", "Be quiet in public places.", K7D2)
V("公務員", "こうむいん", "Civil servant", "兄は公務員として働いている。", "あにはこうむいんとしてはたらいている。", "My older brother works as a civil servant.", K7D2)
V("日本舞踊", "にほんぶよう", "Traditional Japanese dance", "祖母は日本舞踊を習っている。", "そぼはにほんぶようをならっている。", "My grandmother is learning traditional Japanese dance.", K7D2)
V("踊る", "おどる", "Dance", "祭りでみんなで踊った。", "まつりでみんなでおどった。", "Everyone danced together at the festival.", K7D2)
V("踊り", "おどり", "A dance", "伝統的な踊りを見た。", "でんとうてきなおどりをみた。", "I watched a traditional dance.", K7D2)
V("種類", "しゅるい", "Type/kind", "この店ではたくさんの種類の花を売っている。", "このみせではたくさんのしゅるいのはなをうっている。", "This store sells many kinds of flowers.", K7D2)
V("雑種", "ざっしゅ", "Hybrid", "飼っている犬は雑種だ。", "かっているいぬはざっしゅだ。", "The dog I keep is a mixed breed.", K7D2)
V("人種", "じんしゅ", "Race", "人種にかかわらず、みんな平等だ。", "じんしゅにかかわらず、みんなびょうどうだ。", "Everyone is equal, regardless of race.", K7D2)
V("種", "たね", "Seed", "花の種をまいた。", "はなのたねをまいた。", "I planted flower seeds.", K7D2)
V("匹敵する", "ひってきする", "Compare with/rival", "彼の実力はプロに匹敵する。", "かれのじつりょくはプロにひってきする。", "His ability rivals that of a professional.", K7D2)
V("渡米", "とべい", "Going to America", "来月、渡米する予定だ。", "らいげつ、とべいするよていだ。", "I plan to go to America next month.", K7D2)
V("渡る", "わたる", "Cross over", "橋を渡る。", "はしをわたる。", "I cross the bridge.", K7D2)
V("渡す", "わたす", "Hand over", "荷物を彼に渡した。", "にもつをかれにわたした。", "I handed the package to him.", K7D2)
V("乗馬", "じょうば", "Horse riding", "週末に乗馬を体験した。", "しゅうまつにじょうばをたいけんした。", "I experienced horse riding on the weekend.", K7D2)
V("馬", "うま", "Horse", "牧場で馬を見た。", "ぼくじょうでうまをみた。", "I saw horses at the ranch.", K7D2)

# --- Kanji Day 3: メニュー・成分表示 ---
# 卵黄 (already carded week5 kanji d2) and 田植え (already carded week5 listening) skipped as
# cross-week duplicates.
K7D3 = "kanji::w7 kanji::w7d3 jlpt::n2"
V("貝", "かい", "Shell/shellfish", "海辺で貝を拾った。", "うみべでかいをひろった。", "I picked up shells at the beach.", K7D3)
V("貝がら", "かいがら", "Shell", "貝がらでアクセサリーを作った。", "かいがらでアクセサリーをつくった。", "I made accessories from seashells.", K7D3)
V("酒", "さけ", "Alcohol", "父はあまり酒を飲まない。", "ちちはあまりさけをのまない。", "My father doesn't drink much alcohol.", K7D3)
V("酒屋", "さかや", "Liquor store", "酒屋でワインを買った。", "さかやでワインをかった。", "I bought wine at the liquor store.", K7D3)
V("居酒屋", "いざかや", "Japanese pub", "同僚と居酒屋で飲んだ。", "どうりょうといざかやでのんだ。", "I drank with my coworkers at an izakaya.", K7D3)
V("蒸発", "じょうはつ", "Evaporation", "水が蒸発して量が減った。", "みずがじょうはつしてりょうがへった。", "The water evaporated and the amount decreased.", K7D3)
V("水蒸気", "すいじょうき", "Water vapor", "やかんから水蒸気が出ている。", "やかんからすいじょうきがでている。", "Steam is coming out of the kettle.", K7D3)
V("蒸す", "むす", "Steam", "野菜を蒸して食べる。", "やさいをむしてたべる。", "I steam vegetables to eat.", K7D3)
V("蒸し暑い", "むしあつい", "Humid/sultry", "梅雨の時期は蒸し暑い。", "つゆのじきはむしあつい。", "It's humid and hot during the rainy season.", K7D3)
V("干す", "ほす", "Hang/dry", "洗濯物を庭に干した。", "せんたくものをにわにほした。", "I hung the laundry out to dry in the garden.", K7D3)
V("干物", "ひもの", "Dried food", "朝食に干物を食べた。", "ちょうしょくにひものをたべた。", "I ate dried fish for breakfast.", K7D3)
V("竹", "たけ", "Bamboo", "竹でかごを作った。", "たけでかごをつくった。", "I made a basket from bamboo.", K7D3)
V("竹の子", "たけのこ", "Bamboo shoot", "春には竹の子ご飯を食べる。", "はるにはたけのこごはんをたべる。", "I eat bamboo shoot rice in spring.", K7D3)
V("卵", "たまご", "Egg", "朝ごはんに卵を食べた。", "あさごはんにたまごをたべた。", "I ate an egg for breakfast.", K7D3)
V("大根", "だいこん", "White radish", "大根を煮て食べた。", "だいこんをにてたべた。", "I simmered and ate the daikon radish.", K7D3)
V("根", "ね", "Root", "木の根が深く伸びている。", "きのねがふかくのびている。", "The tree's roots extend deep.", K7D3)
V("屋根", "やね", "Roof", "屋根に雪が積もった。", "やねにゆきがつもった。", "Snow piled up on the roof.", K7D3)
V("材料", "ざいりょう", "Ingredients/materials", "料理の材料をそろえた。", "りょうりのざいりょうをそろえた。", "I gathered the ingredients for the dish.", K7D3)
V("材質", "ざいしつ", "Material properties", "この家具の材質は木だ。", "このかぐのざいしつはきだ。", "The material of this furniture is wood.", K7D3)
V("原材料", "げんざいりょう", "Raw materials", "このパンの原材料は小麦粉だ。", "このパンのげんざいりょうはこむぎこだ。", "The raw material of this bread is flour.", K7D3)
V("教材", "きょうざい", "Teaching materials", "新しい教材を使って授業をする。", "あたらしいきょうざいをつかってじゅぎょうをする。", "We teach the class using new teaching materials.", K7D3)
V("植物", "しょくぶつ", "Plant", "この植物は日光を好む。", "このしょくぶつはにっこうをこのむ。", "This plant prefers sunlight.", K7D3)
V("植木", "うえき", "Potted plants", "庭に植木を置いた。", "にわにうえきをおいた。", "I put potted plants in the garden.", K7D3)
V("植える", "うえる", "Plant/grow", "木を庭に植えた。", "きをにわにうえた。", "I planted a tree in the garden.", K7D3)
V("砂糖", "さとう", "Sugar", "コーヒーに砂糖を入れた。", "コーヒーにさとうをいれた。", "I put sugar in the coffee.", K7D3)
V("砂漠", "さばく", "Desert", "砂漠を旅した。", "さばくをたびした。", "I traveled through the desert.", K7D3)
V("砂", "すな", "Sand", "子どもが砂で遊んでいる。", "こどもがすなであそんでいる。", "Children are playing with sand.", K7D3)
V("牛乳", "ぎゅうにゅう", "Milk", "毎朝、牛乳を飲む。", "まいあさ、ぎゅうにゅうをのむ。", "I drink milk every morning.", K7D3)
V("乳児", "にゅうじ", "Baby", "乳児の世話をする。", "にゅうじのせわをする。", "I take care of an infant.", K7D3)
V("乳製品", "にゅうせいひん", "Dairy products", "乳製品をよく食べる。", "にゅうせいひんをよくたべる。", "I often eat dairy products.", K7D3)
V("乳", "ちち", "Milk/breasts", "赤ちゃんは母の乳を飲む。", "あかちゃんははははのちちをのむ。", "The baby drinks its mother's milk.", K7D3)
V("含む", "ふくむ", "Be included", "この価格には税金が含まれている。", "このかかくにはぜいきんがふくまれている。", "This price includes tax.", K7D3)
V("含める", "ふくめる", "Include", "私を含めて5人が参加した。", "わたしをふくめて5にんがさんかした。", "Five people, including myself, participated.", K7D3)
V("炭水化物", "たんすいかぶつ", "Carbohydrate", "炭水化物の取りすぎに注意する。", "たんすいかぶつのとりすぎにちゅういする。", "I'm careful not to eat too many carbohydrates.", K7D3)
V("石炭", "せきたん", "Coal", "昔は石炭で電気を作っていた。", "むかしはせきたんででんきをつくっていた。", "In the past, electricity was made from coal.", K7D3)
V("炭", "すみ", "Charcoal", "炭で肉を焼いた。", "すみでにくをやいた。", "I grilled the meat over charcoal.", K7D3)
V("脂肪", "しぼう", "Fat/grease", "脂肪の少ない肉を選ぶ。", "しぼうのすくないにくをえらぶ。", "I choose meat with less fat.", K7D3)
V("脂質", "ししつ", "Lipids/fats", "食品の脂質を確認する。", "しょくひんのししつをかくにんする。", "I check the lipid content of food.", K7D3)
V("油脂", "ゆし", "Fats and oils", "この製品には植物性の油脂が使われている。", "このせいひんにはしょくぶつせいのゆしがつかわれている。", "This product uses vegetable fats and oils.", K7D3)
V("脂", "あぶら", "Fat/lard", "この肉は脂が多い。", "このにくはあぶらがおおい。", "This meat has a lot of fat.", K7D3)

# --- Kanji Day 4: 受験案内 ---
# 業's only listed word, 業績, is shared with 績 (within-day Kanji-Kanji duplicate) -- kept under
# 績, so 業 contributes no card of its own this week. 前述 (bare form) skipped as a near-duplicate
# of week6's already-carded 前述の.
K7D4 = "kanji::w7 kanji::w7d4 jlpt::n2"
V("封筒", "ふうとう", "Envelope", "手紙を封筒に入れた。", "てがみをふうとうにいれた。", "I put the letter in an envelope.", K7D4)
V("水筒", "すいとう", "Canteen/water bottle", "遠足に水筒を持っていった。", "えんそくにすいとうをもっていった。", "I brought a water bottle on the excursion.", K7D4)
V("筒", "つつ", "Pipe/tube", "紙を筒の形に丸めた。", "かみをつつのかたちにまるめた。", "I rolled the paper into a tube shape.", K7D4)
V("卒業", "そつぎょう", "Graduation", "来年、大学を卒業する。", "らいねん、だいがくをそつぎょうする。", "I will graduate from university next year.", K7D4)
V("卒業証明書", "そつぎょうしょうめいしょ", "Diploma", "就職のために卒業証明書が必要だ。", "しゅうしょくのためにそつぎょうしょうめいしょがひつようだ。", "A diploma is needed for employment.", K7D4)
V("成績", "せいせき", "Results/record", "今学期の成績が良かった。", "こんがっきのせいせきがよかった。", "My grades this semester were good.", K7D4)
V("実績", "じっせき", "Actual results/achievement", "この会社は営業の実績がある。", "このかいしゃはえいぎょうのじっせきがある。", "This company has a track record in sales.", K7D4)
V("業績", "ぎょうせき", "Achievement/business results", "会社の業績が伸びている。", "かいしゃのぎょうせきがのびている。", "The company's business performance is improving.", K7D4)
V("論文", "ろんぶん", "Thesis/treatise", "卒業論文を書いている。", "そつぎょうろんぶんをかいている。", "I'm writing my graduation thesis.", K7D4)
V("結論", "けつろん", "Conclusion", "会議で結論が出た。", "かいぎでけつろんがでた。", "A conclusion was reached at the meeting.", K7D4)
V("議論", "ぎろん", "Argument/discussion", "その問題について議論した。", "そのもんだいについてぎろんした。", "We discussed that issue.", K7D4)
V("志望", "しぼう", "Wish/desire", "第一志望の大学に合格した。", "だいいちしぼうのだいがくにごうかくした。", "I passed the entrance exam for my first-choice university.", K7D4)
V("意志", "いし", "Will/volition", "彼は意志が強い。", "かれはいしがつよい。", "He has a strong will.", K7D4)
V("記述", "きじゅつ", "Description", "試験は記述式だった。", "しけんはきじゅつしきだった。", "The exam was in written-answer format.", K7D4)
V("口述", "こうじゅつ", "Verbal statement", "口述試験を受けた。", "こうじゅつしけんをうけた。", "I took an oral exam.", K7D4)
V("述べる", "のべる", "State/mention", "自分の意見を述べた。", "じぶんのいけんをのべた。", "I stated my own opinion.", K7D4)
V("結構", "けっこう", "Splendid/nice", "この案で結構です。", "このあんでけっこうです。", "This proposal is fine.", K7D4)
V("構成", "こうせい", "Composition", "この論文は構成が良い。", "このろんぶんはこうせいがいい。", "This paper is well-structured.", K7D4)
V("構内", "こうない", "Campus/grounds", "大学の構内を歩いた。", "だいがくのこうないをあるいた。", "I walked around the university campus.", K7D4)
V("構う", "かまう", "Mind/care about", "私に構わず先に行ってください。", "わたしにかまわずさきにいってください。", "Don't worry about me, please go ahead.", K7D4)
V("遅刻", "ちこく", "Tardiness", "電車が遅れて遅刻した。", "でんしゃがおくれてちこくした。", "The train was delayed and I was late.", K7D4)
V("遅い", "おそい", "Slow/late", "今日は帰りが遅い。", "きょうはかえりがおそい。", "I'm coming home late today.", K7D4)
V("遅れる", "おくれる", "Be late", "会議の開始が遅れた。", "かいぎのかいしがおくれた。", "The start of the meeting was delayed.", K7D4)
V("仮名", "かな", "Japanese syllabary", "日本語には漢字と仮名がある。", "にほんごにはかんじとかながある。", "Japanese has kanji and kana.", K7D4)
V("振り仮名", "ふりがな", "Kana over kanji", "難しい漢字に振り仮名をつけた。", "むずかしいかんじにふりがなをつけた。", "I added furigana to the difficult kanji.", K7D4)
V("仮定", "かてい", "Assumption", "もし雨だったらと仮定して計画を立てた。", "もしあめだったらとかていしてけいかくをたてた。", "I made a plan assuming it might rain.", K7D4)
V("仮", "かり", "Temporary", "これは仮の住所です。", "これはかりのじゅうしょです。", "This is a temporary address.", K7D4)
V("机", "つくえ", "Desk", "机の上に本を置いた。", "つくえのうえにほんをおいた。", "I put a book on the desk.", K7D4)
V("冊子", "さっし", "Booklet/pamphlet", "案内の冊子をもらった。", "あんないのさっしをもらった。", "I received an information booklet.", K7D4)
V("採点", "さいてん", "Grading/marking", "先生がテストを採点している。", "せんせいがテストをさいてんしている。", "The teacher is grading the test.", K7D4)
V("採集", "さいしゅう", "Collecting/gathering", "夏休みに昆虫採集をした。", "なつやすみにこんちゅうさいしゅうをした。", "I collected insects during summer vacation.", K7D4)
V("採る", "とる", "Adopt a measure", "この方法を採ることにした。", "このほうほうをとることにした。", "We decided to adopt this method.", K7D4)
V("濃度", "のうど", "Concentration/density", "塩水の濃度を測る。", "しおみずののうどをはかる。", "I measure the concentration of the salt water.", K7D4)
V("濃い", "こい", "Concentrated/dark color", "濃いコーヒーが好きだ。", "こいコーヒーがすきだ。", "I like strong coffee.", K7D4)
V("鉛筆", "えんぴつ", "Pencil", "鉛筆で名前を書いた。", "えんぴつでなまえをかいた。", "I wrote my name with a pencil.", K7D4)
V("筆記", "ひっき", "Taking notes", "筆記試験を受けた。", "ひっきしけんをうけた。", "I took a written exam.", K7D4)
V("筆者", "ひっしゃ", "Writer/author", "この記事の筆者は有名な作家だ。", "このきじのひっしゃはゆうめいなさっかだ。", "The author of this article is a famous writer.", K7D4)
V("筆", "ふで", "Writing brush", "筆で文字を書いた。", "ふででもじをかいた。", "I wrote characters with a brush.", K7D4)

# --- Kanji Day 5: 交通情報 ---
K7D5 = "kanji::w7 kanji::w7d5 jlpt::n2"
V("航空", "こうくう", "Aviation/flying", "航空会社に就職した。", "こうくうがいしゃにしゅうしょくした。", "I got a job at an airline company.", K7D5)
V("運航", "うんこう", "Operation of ships/aircraft", "悪天候でフェリーの運航が中止になった。", "あくてんこうでフェリーのうんこうがちゅうしになった。", "Ferry service was suspended due to bad weather.", K7D5)
V("陸", "りく", "Land/shore", "船が陸に近づいた。", "ふねがりくにちかづいた。", "The ship approached land.", K7D5)
V("大陸", "たいりく", "Continent", "アフリカ大陸を旅した。", "アフリカたいりくをたびした。", "I traveled through the African continent.", K7D5)
V("陸上", "りくじょう", "On the land", "陸上部で走っている。", "りくじょうぶではしっている。", "I run track in the athletics club.", K7D5)
V("損", "そん", "Loss/disadvantage", "このやり方では損だ。", "このやりかたではそんだ。", "This method is a loss.", K7D5)
V("損傷", "そんしょう", "Damage/injury", "台風で建物が損傷した。", "たいふうでたてものがそんしょうした。", "The building was damaged by the typhoon.", K7D5)
V("損害", "そんがい", "Damage/loss", "事故の損害を保険で補った。", "じこのそんがいをほけんでおぎなった。", "The accident damage was covered by insurance.", K7D5)
V("損得", "そんとく", "Loss and gain", "損得を考えずに手伝った。", "そんとくをかんがえずにてつだった。", "I helped without thinking about gain or loss.", K7D5)
V("気候", "きこう", "Climate", "この地域は温暖な気候だ。", "このちいきはおんだんなきこうだ。", "This region has a mild climate.", K7D5)
V("天候", "てんこう", "Weather", "天候が悪くて登山を中止した。", "てんこうがわるくてとざんをちゅうしした。", "We cancelled the climb due to bad weather.", K7D5)
V("風船", "ふうせん", "Balloon", "子どもに風船をあげた。", "こどもにふうせんをあげた。", "I gave a balloon to the child.", K7D5)
V("造船", "ぞうせん", "Shipbuilding", "この町は造船業で栄えた。", "このまちはぞうせんぎょうでさかえた。", "This town flourished through shipbuilding.", K7D5)
V("船", "ふね", "Boat/ship", "船で島に渡った。", "ふねでしまにわたった。", "I crossed to the island by boat.", K7D5)
V("船便", "ふなびん", "Surface/sea mail", "荷物を船便で送った。", "にもつをふなびんでおくった。", "I sent the package by sea mail.", K7D5)
V("丸", "まる", "Circle", "正解には丸をつける。", "せいかいにはまるをつける。", "Mark correct answers with a circle.", K7D5)
V("丸い", "まるい", "Round", "丸いテーブルを買った。", "まるいテーブルをかった。", "I bought a round table.", K7D5)
V("混雑", "こんざつ", "Confusion/congestion", "電車が混雑している。", "でんしゃがこんざつしている。", "The train is crowded.", K7D5)
V("混じる", "まじる", "Be mixed", "雨に雪が混じっている。", "あめにゆきがまじっている。", "Snow is mixed in with the rain.", K7D5)
V("予想", "よそう", "Anticipation/forecast", "試合の結果を予想した。", "しあいのけっかをよそうした。", "I predicted the result of the match.", K7D5)
V("想像", "そうぞう", "Imagination/guess", "将来の自分を想像する。", "しょうらいのじぶんをそうぞうする。", "I imagine my future self.", K7D5)
V("感想", "かんそう", "Impressions/thoughts", "映画の感想を話した。", "えいがのかんそうをはなした。", "I talked about my impressions of the movie.", K7D5)
V("理想", "りそう", "Ideal", "理想の仕事を見つけた。", "りそうのしごとをみつけた。", "I found my ideal job.", K7D5)
V("事故", "じこ", "Accident", "交通事故が起きた。", "こうつうじこがおきた。", "A traffic accident occurred.", K7D5)
V("故障", "こしょう", "Breakdown/failure", "洗濯機が故障した。", "せんたくきがこしょうした。", "The washing machine broke down.", K7D5)
V("故郷", "こきょう", "Hometown/birthplace", "久しぶりに故郷に帰った。", "ひさしぶりにこきょうにかえった。", "I returned to my hometown after a long time.", K7D5)
V("混乱", "こんらん", "Disorder/confusion", "事故でダイヤが混乱した。", "じこでダイヤがこんらんした。", "The train schedule was thrown into confusion by the accident.", K7D5)
V("乱暴", "らんぼうな", "Rude/violent", "彼は乱暴な運転をする。", "かれはらんぼうなうんてんをする。", "He drives roughly.", K7D5)
V("乱れる", "みだれる", "Fall into disorder", "強風で髪が乱れた。", "きょうふうでかみがみだれた。", "My hair was disheveled by the strong wind.", K7D5)
V("運河", "うんが", "Canal/waterway", "運河を船が通っている。", "うんがをふねがとおっている。", "A boat is passing through the canal.", K7D5)
V("河川", "かせん", "Rivers", "大雨で河川が増水した。", "おおあめでかせんがぞうすいした。", "Rivers swelled due to heavy rain.", K7D5)
V("河", "かわ", "River/stream", "河のほとりを歩いた。", "かわのほとりをあるいた。", "I walked along the riverbank.", K7D5)
V("輸出", "ゆしゅつ", "Exportation", "この製品は海外に輸出されている。", "このせいひんはかいがいにゆしゅつされている。", "This product is exported overseas.", K7D5)
V("輸入", "ゆにゅう", "Importation", "輸入品の価格が上がった。", "ゆにゅうひんのかかくがあがった。", "The price of imported goods has risen.", K7D5)
V("輸血", "ゆけつ", "Blood transfusion", "手術で輸血が必要になった。", "しゅじゅつでゆけつがひつようになった。", "A blood transfusion was needed during the surgery.", K7D5)
V("輸送", "ゆそう", "Transportation", "トラックで荷物を輸送する。", "トラックでにもつをゆそうする。", "I transport goods by truck.", K7D5)

# --- Kanji Day 6: 気象情報 ---
# 宇都宮 and 水戸 (city names) skipped as low-value proper nouns.
K7D6 = "kanji::w7 kanji::w7d6 jlpt::n2"
V("率", "りつ", "Rate/ratio", "合格の率は低い。", "ごうかくのりつはひくい。", "The pass rate is low.", K7D6)
V("確率", "かくりつ", "Probability", "雨が降る確率は50%だ。", "あめがふるかくりつは50パーセントだ。", "There's a 50% chance of rain.", K7D6)
V("利率", "りりつ", "Interest rate", "この銀行の利率は低い。", "このぎんこうのりりつはひくい。", "This bank's interest rate is low.", K7D6)
V("率直", "そっちょく", "Frankness/candor", "率直な意見を聞かせてほしい。", "そっちょくないけんをきかせてほしい。", "I want to hear your frank opinion.", K7D6)
V("能率", "のうりつ", "Efficiency", "休憩を取ると能率が上がる。", "きゅうけいをとるとのうりつがあがる。", "Taking breaks improves efficiency.", K7D6)
V("宇宙", "うちゅう", "Universe/outer space", "宇宙旅行が夢ではなくなった。", "うちゅうりょこうがゆめではなくなった。", "Space travel is no longer just a dream.", K7D6)
V("一戸建て", "いっこだて", "Detached house", "郊外に一戸建てを買った。", "こうがいにいっこだてをかった。", "I bought a detached house in the suburbs.", K7D6)
V("戸", "と", "Door", "戸を開けて風を入れた。", "とをあけてかぜをいれた。", "I opened the door to let in the breeze.", K7D6)
V("雨戸", "あまど", "Sliding storm door", "台風に備えて雨戸を閉めた。", "たいふうにそなえてあまどをしめた。", "I closed the storm shutters in preparation for the typhoon.", K7D6)
V("晴天", "せいてん", "Fine weather", "晴天に恵まれた運動会だった。", "せいてんにめぐまれたうんどうかいだった。", "It was a sports day blessed with clear weather.", K7D6)
V("快晴", "かいせい", "Good weather", "今日は快晴だ。", "きょうはかいせいだ。", "Today is perfectly clear.", K7D6)
V("晴れる", "はれる", "Be sunny", "明日は晴れるらしい。", "あしたははれるらしい。", "It seems it will be sunny tomorrow.", K7D6)
V("素晴らしい", "すばらしい", "Wonderful/magnificent", "素晴らしい景色だった。", "すばらしいけしきだった。", "It was a wonderful view.", K7D6)
V("曇り", "くもり", "Cloudy weather", "今日は曇りだ。", "きょうはくもりだ。", "Today is cloudy.", K7D6)
V("曇る", "くもる", "Become cloudy", "眼鏡が曇って見えにくい。", "めがねがくもってみえにくい。", "My glasses fogged up and it's hard to see.", K7D6)
V("積雪", "せきせつ", "Snow accumulation", "積雪で道路が通れなくなった。", "せきせつでどうろがとおれなくなった。", "The road became impassable due to snow accumulation.", K7D6)
V("吹雪", "ふぶき", "Snowstorm", "今夜は吹雪になりそうだ。", "こんやはふぶきになりそうだ。", "It looks like it will be a snowstorm tonight.", K7D6)
V("雪", "ゆき", "Snow", "昨夜、雪が降った。", "さくや、ゆきがふった。", "It snowed last night.", K7D6)
V("大雪", "おおゆき", "Heavy snow", "大雪で電車が止まった。", "おおゆきででんしゃがとまった。", "The trains stopped due to heavy snow.", K7D6)
V("知恵", "ちえ", "Wisdom", "昔の人は知恵を使って生活した。", "むかしのひとはちえをつかってせいかつした。", "People in the past used their wisdom to live.", K7D6)
V("恩恵", "おんけい", "Benefits", "自然の恩恵を受けて暮らす。", "しぜんのおんけいをうけてくらす。", "We live receiving the blessings of nature.", K7D6)
V("恵まれる", "めぐまれる", "Be blessed with", "今日は良い天気に恵まれた。", "きょうはよいてんきにめぐまれた。", "We were blessed with good weather today.", K7D6)
V("太陽", "たいよう", "Sun", "太陽が昇ってきた。", "たいようがのぼってきた。", "The sun has risen.", K7D6)
V("陽気", "ようき", "Weather/cheerfulness", "春らしい陽気になった。", "はるらしいようきになった。", "It became spring-like weather.", K7D6)
V("雲", "くも", "Clouds", "空に白い雲が浮かんでいる。", "そらにしろいくもがうかんでいる。", "White clouds float in the sky.", K7D6)
V("雨雲", "あまぐも", "Rain clouds", "雨雲が近づいている。", "あまぐもがちかづいている。", "Rain clouds are approaching.", K7D6)

# --- Kanji Day 7 Extra: 読みを推測する (bonus puzzle, kanji 642-651) ---
# 彼女 skipped as too basic for an N2 deck.
K7DE = "kanji::w7 kanji::w7dExtra jlpt::n2"
V("漁船", "ぎょせん", "A fishing boat", "漁船が港に戻ってきた。", "ぎょせんがみなとにもどってきた。", "The fishing boat returned to the harbor.", K7DE)
V("漁師", "りょうし", "A fisherman", "祖父は漁師だった。", "そふはりょうしだった。", "My grandfather was a fisherman.", K7DE)
V("海底", "かいてい", "The sea bottom", "海底に沈んだ船を調査する。", "かいていにしずんだふねをちょうさする。", "We investigate the ship that sank to the seabed.", K7DE)
V("鉱山", "こうざん", "A mine", "この町には昔、鉱山があった。", "このまちにはむかし、こうざんがあった。", "There used to be a mine in this town.", K7DE)
V("炭鉱", "たんこう", "A coal mine/coal pit", "祖父は炭鉱で働いていた。", "そふはたんこうではたらいていた。", "My grandfather worked at a coal mine.", K7DE)
V("彼岸", "ひがん", "The week of the equinox", "お彼岸にお墓参りをした。", "おひがんにおはかまいりをした。", "I visited the grave during the equinox week.", K7DE)
V("彼", "かれ", "He/him/boyfriend", "彼は毎朝ジョギングをする。", "かれはまいあさジョギングをする。", "He jogs every morning.", K7DE)
V("水滴", "すいてき", "A waterdrop", "葉に水滴がついている。", "はにすいてきがついている。", "There are water droplets on the leaf.", K7DE)
V("偉大", "いだいな", "Great", "彼は偉大な科学者だ。", "かれはいだいなかがくしゃだ。", "He is a great scientist.", K7DE)
V("規則", "きそく", "A rule/regulation", "学校の規則を守る。", "がっこうのきそくをまもる。", "I follow the school rules.", K7DE)
V("測定", "そくてい", "A measurement", "体重を測定した。", "たいじゅうをそくていした。", "I measured my weight.", K7DE)
V("測る", "はかる", "Measure/weigh", "部屋の広さを測った。", "へやのひろさをはかった。", "I measured the size of the room.", K7DE)
V("授業", "じゅぎょう", "A class/lesson", "今日は数学の授業がある。", "きょうはすうがくのじゅぎょうがある。", "There's a math class today.", K7DE)
V("零下", "れいか", "Being sub-zero", "気温が零下になった。", "きおんがれいかになった。", "The temperature went below zero.", K7DE)

# --- Vocabulary Day 1: 意味がたくさんある言葉① (multi-meaning words) ---
VOC7D1 = "vocabulary::w7 vocabulary::w7d1 jlpt::n2"
V("切れる", "きれる", "Break (a string/cord)", "重い荷物をぶら下げていたら、ひもが切れてしまった。", "おもいにもつをぶらさげていたら、ひもがきれてしまった。", "The string broke because I was carrying a heavy load.", VOC7D1)
V("切る", "きる", "Cut (a string/cord)", "はさみでひもを切った。", "はさみでひもをきった。", "I cut the string with scissors.", VOC7D1)
V("電池が切れる", "でんちがきれる", "Run out of battery", "電池が切れたから、新しいのに換えよう。", "でんちがきれたから、あたらしいのにかえよう。", "The battery died, so let's replace it with a new one.", VOC7D1)
V("タバコが切れる", "タバコがきれる", "Be out of cigarettes", "タバコが切れたので、コンビニへ買いに行った。", "タバコがきれたので、コンビニへかいにいった。", "I was out of cigarettes, so I went to the convenience store to buy some.", VOC7D1)
V("賞味期限が切れる", "しょうみきげんがきれる", "Be past the best-before date", "冷蔵庫の牛乳は賞味期限が切れていた。", "れいぞうこのぎゅうにゅうはしょうみきげんがきれていた。", "The milk in the fridge was past its best-before date.", VOC7D1)
V("しびれが切れる", "しびれがきれる", "Have one's legs go numb", "畳の上に長い間座っていたら、しびれが切れた。", "たたみのうえにながいあいだすわっていたら、しびれがきれた。", "After sitting on the tatami for a long time, my legs went numb.", VOC7D1)
V("電源を切る", "でんげんをきる", "Switch off the power", "寝る前にテレビの電源を切った。", "ねるまえにテレビのでんげんをきった。", "I switched off the TV before going to bed.", VOC7D1)
V("電源が切れる", "でんげんがきれる", "The power goes off", "停電で急に電源が切れた。", "ていでんできゅうにでんげんがきれた。", "The power suddenly went off due to a blackout.", VOC7D1)
V("野菜の水気を切る", "やさいのみずけをきる", "Drain the water from vegetables", "サラダを作る前に野菜の水気を切った。", "サラダをつくるまえにやさいのみずけをきった。", "I drained the water from the vegetables before making the salad.", VOC7D1)
V("スタートを切る", "スタートをきる", "Start off", "新しい仕事で順調なスタートを切った。", "あたらしいしごとでじゅんちょうなスタートをきった。", "I got off to a smooth start at my new job.", VOC7D1)
V("100メートル競走で10秒を切る", "100メートルきょうそうで10びょうをきる", "Run 100 meters in under 10 seconds", "彼は100メートル競走で10秒を切った。", "かれは100メートルきょうそうで10びょうをきった。", "He ran the 100-meter dash in under 10 seconds.", VOC7D1)
V("ハンドルを右に切る", "ハンドルをみぎにきる", "Turn the steering wheel to the right", "カーブに合わせてハンドルを右に切った。", "カーブにあわせてハンドルをみぎにきった。", "I turned the steering wheel to the right to match the curve.", VOC7D1)
V("カードをよく切る", "カードをよくきる", "Shuffle the cards well", "ゲームを始める前にカードをよく切った。", "ゲームをはじめるまえにカードをよくきった。", "I shuffled the cards well before starting the game.", VOC7D1)
V("キレる", "キレる", "Lose one's temper / snap", "彼は些細なことでキレて、大声を出した。", "かれはささいなことでキレて、おおごえをだした。", "He lost his temper over a trivial thing and shouted.", VOC7D1)
V("しみがつく", "しみがつく", "Get a stain on", "白いシャツにコーヒーのしみがついた。", "しろいシャツにコーヒーのしみがついた。", "A coffee stain got on the white shirt.", VOC7D1)
V("しみをつける", "しみをつける", "Put a stain on", "不注意でテーブルクロスにしみをつけてしまった。", "ふちゅういでテーブルクロスにしみをつけてしまった。", "I carelessly put a stain on the tablecloth.", VOC7D1)
V("窓ガラスに水滴がつく", "まどガラスにすいてきがつく", "Condensation forms on the window", "冬の朝は窓ガラスに水滴がつく。", "ふゆのあさはまどガラスにすいてきがつく。", "On winter mornings, condensation forms on the window glass.", VOC7D1)
V("利子がつく", "りしがつく", "Yield interest", "この口座には利子がつく。", "このこうざにはりしがつく。", "Interest accrues on this account.", VOC7D1)
V("身につく", "みにつく", "Master (a skill)", "毎日練習すれば、技術は自然に身につく。", "まいにちれんしゅうすれば、ぎじゅつはしぜんにみにつく。", "If you practice every day, the skill will naturally become second nature.", VOC7D1)
V("身につける", "みにつける", "Acquire (a skill)", "留学して英語力を身につけた。", "りゅうがくしてえいごりょくをみにつけた。", "I studied abroad and acquired English ability.", VOC7D1)
V("力がつく", "ちからがつく", "Gain power/strength", "毎日走っていたら、足に力がついた。", "まいにちはしっていたら、あしにちからがついた。", "After running every day, my legs gained strength.", VOC7D1)
V("力をつける", "ちからをつける", "Build strength", "基礎から力をつけるつもりだ。", "きそからちからをつけるつもりだ。", "I intend to build strength from the basics.", VOC7D1)
V("差がつく", "さがつく", "A gap opens up", "練習量によって実力に差がついた。", "れんしゅうりょうによってじつりょくにさがついた。", "A gap in ability opened up depending on the amount of practice.", VOC7D1)
V("差をつける", "さをつける", "Pull ahead / make a difference", "2位とはずいぶん差をつけて、優勝した。", "にいとはずいぶんさをつけて、ゆうしょうした。", "He won, pulling far ahead of second place.", VOC7D1)
V("見当がつく", "けんとうがつく", "Have an idea / guess", "彼が何を考えているか見当がつかない。", "かれがなにをかんがえているかけんとうがつかない。", "I have no idea what he's thinking.", VOC7D1)
V("見当をつける", "けんとうをつける", "Make a guess", "だいたいの値段に見当をつけてから店に行った。", "だいたいのねだんにけんとうをつけてからみせにいった。", "I made a rough guess at the price before going to the store.", VOC7D1)
V("めどがつく", "めどがつく", "There is hope for / an end in sight", "ようやく工事の完成にめどがついた。", "ようやくこうじのかんせいにめどがついた。", "We finally have an end in sight for the construction's completion.", VOC7D1)
V("めどをつける", "めどをつける", "Set a goal / prospect", "来月までに終わるようめどをつけた。", "らいげつまでにおわるようめどをつけた。", "I set a goal to finish by next month.", VOC7D1)
V("決心がつく", "けっしんがつく", "Make up one's mind", "彼に結婚を申し込まれているが、なかなか決心がつかない。", "かれにけっこんをもうしこまれているが、なかなかけっしんがつかない。", "He proposed marriage to me, but I can't make up my mind.", VOC7D1)
V("服ににおいがつく", "ふくににおいがつく", "Clothes pick up an odor", "焼肉屋に行くと服ににおいがつく。", "やきにくやにいくとふくににおいがつく。", "When I go to a yakiniku restaurant, my clothes pick up the smell.", VOC7D1)
V("折り目がつく", "おりめがつく", "Get a crease", "このズボンはすぐ折り目がつく。", "このズボンはすぐおりめがつく。", "These pants get creases easily.", VOC7D1)
V("折り目をつける", "おりめをつける", "Put a crease in", "アイロンでズボンに折り目をつけよう。", "アイロンでズボンにおりめをつけよう。", "Let's put a crease in the pants with the iron.", VOC7D1)
V("味がつく", "あじがつく", "Become flavored", "煮込むうちに味がついてきた。", "にこむうちにあじがついてきた。", "It became flavorful as it simmered.", VOC7D1)
V("味をつける", "あじをつける", "Flavor (something)", "スープに塩で味をつけた。", "スープにしおであじをつけた。", "I flavored the soup with salt.", VOC7D1)
V("ボールが当たる", "ボールがあたる", "The ball hits", "窓にボールが当たって割れた。", "まどにボールがあたってわれた。", "The ball hit the window and it broke.", VOC7D1)
V("ボールを当てる", "ボールをあてる", "Hit (something) with a ball", "的にボールを当てるゲームをした。", "まとにボールをあてるゲームをした。", "We played a game of hitting the target with a ball.", VOC7D1)
V("答えが当たる", "こたえがあたる", "Get the right answer", "クイズの答えが当たってうれしかった。", "クイズのこたえがあたってうれしかった。", "I was happy that I got the quiz answer right.", VOC7D1)
V("答えを当てる", "こたえをあてる", "Guess the answer", "友達の考えている数字を当てた。", "ともだちのかんがえているすうじをあてた。", "I guessed the number my friend was thinking of.", VOC7D1)
V("宝くじが当たる", "たからくじがあたる", "Win the lottery", "宝くじが当たったら、何を買いますか。", "たからくじがあたったら、なにをかいますか。", "What would you buy if you won the lottery?", VOC7D1)
V("日が当たる", "ひがあたる", "Get sun", "この部屋はよく日が当たる。", "このへやはよくひがあたる。", "This room gets a lot of sun.", VOC7D1)
V("日を当てる", "ひをあてる", "Expose to the sun", "布団に日を当てて干した。", "ふとんにひをあててほした。", "I aired out the futon by exposing it to the sun.", VOC7D1)
V("額に手を当てる", "ひたいにてをあてる", "Put one's hand on one's forehead", "熱を測るために額に手を当てた。", "ねつをはかるためにひたいにてをあてた。", "I put my hand on my forehead to check for a fever.", VOC7D1)

# --- Vocabulary Day 2: 意味がたくさんある言葉② (multi-meaning words) ---
VOC7D2 = "vocabulary::w7 vocabulary::w7d2 jlpt::n2"
V("迷惑がかかる", "めいわくがかかる", "Be an inconvenience/burden (to someone)", "工事の音で近所に迷惑がかかっている。", "こうじのおとできんじょにめいわくがかかっている。", "The construction noise is causing an inconvenience to the neighbors.", VOC7D2)
V("迷惑をかける", "めいわくをかける", "Cause inconvenience (to someone)", "遅刻して皆に迷惑をかけてしまった。", "ちこくしてみんなにめいわくをかけてしまった。", "I was late and caused everyone an inconvenience.", VOC7D2)
V("太陽に雲がかかる", "たいようにくもがかかる", "The sun goes behind a cloud", "太陽に雲がかかって、急に暗くなった。", "たいようにくもがかかって、きゅうにくらくなった。", "The sun went behind a cloud and it suddenly got dark.", VOC7D2)
V("エンジンがかかる", "エンジンがかかる", "The engine starts", "寒い朝はなかなかエンジンがかからない。", "さむいあさはなかなかエンジンがかからない。", "On cold mornings, the engine doesn't start easily.", VOC7D2)
V("エンジンをかける", "エンジンをかける", "Start the engine", "出発前にエンジンをかけておいた。", "しゅっぱつまえにエンジンをかけておいた。", "I started the engine before we left.", VOC7D2)
V("優勝がかかる", "ゆうしょうがかかる", "The championship is at stake", "この試合には優勝がかかっている。", "このしあいにはゆうしょうがかかっている。", "The championship is at stake in this match.", VOC7D2)
V("壁に絵をかける", "かべにえをかける", "Hang a picture on the wall", "リビングの壁に絵をかけた。", "リビングのかべにえをかけた。", "I hung a picture on the living room wall.", VOC7D2)
V("腰をかける", "こしをかける", "Take a seat", "ソファーに腰をかけて話しましょう。", "ソファーにこしをかけてはなしましょう。", "Let's sit on the sofa and talk.", VOC7D2)
V("橋がかかる", "はしがかかる", "A bridge is built", "この川には新しい橋がかかっている。", "このかわにはあたらしいはしがかかっている。", "A new bridge has been built over this river.", VOC7D2)
V("橋をかける", "はしをかける", "Build a bridge", "町は川に新しい橋をかけることにした。", "まちはかわにあたらしいはしをかけることにした。", "The town decided to build a new bridge over the river.", VOC7D2)
V("犬にブラシをかける", "いぬにブラシをかける", "Brush the dog", "毎朝、犬にブラシをかけている。", "まいあさ、いぬにブラシをかけている。", "I brush the dog every morning.", VOC7D2)
V("水がかかる", "みずがかかる", "Get splashed with water", "車が水たまりを通って、服に水がかかった。", "くるまがみずたまりをとおって、ふくにみずがかかった。", "A car drove through a puddle and my clothes got splashed with water.", VOC7D2)
V("植木に水をかける", "うえきにみずをかける", "Water the plant", "毎朝、植木に水をかけている。", "まいあさ、うえきにみずをかけている。", "I water the plants every morning.", VOC7D2)
V("体重をかける", "たいじゅうをかける", "Put one's weight on", "片足に体重をかけて立った。", "かたあしにたいじゅうをかけてたった。", "I stood putting my weight on one leg.", VOC7D2)
V("命をかけて、子どもたちを守る", "いのちをかけて、こどもたちをまもる", "Risk one's life to protect the children", "母親は命をかけて、子どもたちを守った。", "ははおやはいのちをかけて、こどもたちをまもった。", "The mother risked her life to protect her children.", VOC7D2)
V("保険をかける", "ほけんをかける", "Take out insurance", "彼女は高価な楽器に保険をかけた。", "かのじょはこうかながっきにほけんをかけた。", "She insured her expensive instrument.", VOC7D2)
V("火にかける", "ひにかける", "Put a pan on the stove", "スープを火にかけて温めた。", "スープをひにかけてあたためた。", "I put the soup on the stove to heat it up.", VOC7D2)
V("金メダルを取る", "きんメダルをとる", "Win a gold medal", "彼はオリンピックで金メダルを取った。", "かれはオリンピックできんメダルをとった。", "He won a gold medal at the Olympics.", VOC7D2)
V("記録を取る", "きろくをとる", "Keep a record of", "インタビューの記録を取っておく。", "インタビューのきろくをとっておく。", "I'll keep a record of the interview.", VOC7D2)
V("場所を取る", "ばしょをとる", "Take up space", "机が場所を取ってベッドが置けません。", "つくえがばしょをとってベッドがおけません。", "The desk takes up so much space that I can't put a bed in.", VOC7D2)
V("責任を取る", "せきにんをとる", "Take responsibility", "失敗の責任を取って辞任した。", "しっぱいのせきにんをとってじにんした。", "He resigned, taking responsibility for the failure.", VOC7D2)
V("下準備に時間を取る", "したじゅんびにじかんをとる", "Take time to prepare", "下準備には十分な時間を取りましょう。", "したじゅんびにはじゅうぶんなじかんをとりましょう。", "Let's take enough time for preparation.", VOC7D2)
V("親の機嫌を取る", "おやのきげんをとる", "Try to please one's parents", "彼はいつも親の機嫌を取っている。", "かれはいつもおやのきげんをとっている。", "He is always trying to please his parents.", VOC7D2)
V("大事を取って入院する", "だいじをとってにゅういんする", "Get hospitalized just in case (to be safe)", "軽いけがだったが、大事を取って入院した。", "かるいけがだったが、だいじをとってにゅういんした。", "It was a minor injury, but I was hospitalized just to be safe.", VOC7D2)
V("税金を取られる", "ぜいきんをとられる", "Have a tax imposed", "車や家を買うと、消費税とは別の税金を取られる。", "くるまやいえをかうと、しょうひぜいとはべつのぜいきんをとられる。", "When you buy a car or house, a tax separate from consumption tax is imposed.", VOC7D2)
V("ハンドルを取られる", "ハンドルをとられる", "Lose control of the steering wheel", "強風でハンドルを取られそうになった。", "きょうふうでハンドルをとられそうになった。", "I nearly lost control of the steering wheel because of the strong wind.", VOC7D2)
V("疲れが取れる", "つかれがとれる", "Recover from fatigue", "温泉に入ったら、疲れが取れた。", "おんせんにはいったら、つかれがとれた。", "After soaking in the hot spring, my fatigue went away.", VOC7D2)
V("身長が伸びる", "しんちょうがのびる", "Grow taller", "この一年で身長が5センチ伸びた。", "このいちねんでしんちょうが5センチのびた。", "My height grew 5cm this year.", VOC7D2)
V("売り上げが伸びる", "うりあげがのびる", "Sales go up", "新商品のおかげで売り上げが伸びた。", "しんしょうひんのおかげでうりあげがのびた。", "Thanks to the new product, sales went up.", VOC7D2)
V("売り上げを伸ばす", "うりあげをのばす", "Increase sales", "広告を工夫して売り上げを伸ばした。", "こうこくをくふうしてうりあげをのばした。", "We increased sales by improving the advertisements.", VOC7D2)
V("パジャマのズボンのゴムが伸びる", "パジャマのズボンのゴムがのびる", "The elastic of the pajama pants goes slack", "何年も使ってパジャマのズボンのゴムが伸びてしまった。", "なんねんもつかってパジャマのズボンのゴムがのびてしまった。", "After years of use, the elastic of the pajama pants has gone slack.", VOC7D2)
V("そばが伸びて、まずくなる", "そばがのびて、まずくなる", "The soba gets soggy and loses its taste", "時間が経って、そばが伸びてまずくなった。", "じかんがたって、そばがのびてまずくなった。", "Time passed and the soba got soggy and lost its taste.", VOC7D2)
V("髪が伸びる", "かみがのびる", "Hair grows", "ずっと切らなかったので髪が肩まで伸びた。", "ずっときらなかったのでかみがかたまでのびた。", "My hair grew down to my shoulders because I hadn't cut it in a while.", VOC7D2)
V("肩まで髪を伸ばす", "かたまでかみをのばす", "Grow one's hair down to the shoulders", "彼女は肩まで髪を伸ばすことにした。", "かのじょはかたまでかみをのばすことにした。", "She decided to grow her hair down to her shoulders.", VOC7D2)
V("アンテナを伸ばす", "アンテナをのばす", "Extend the antenna", "ラジオのアンテナを伸ばした。", "ラジオのアンテナをのばした。", "I extended the radio's antenna.", VOC7D2)
V("しわが伸びる", "しわがのびる", "Creases are smoothed out", "アイロンをかけたら、しわが伸びた。", "アイロンをかけたら、しわがのびた。", "After ironing, the creases were smoothed out.", VOC7D2)
V("アイロンをかけてしわを伸ばす", "アイロンをかけてしわをのばす", "Iron out the creases", "シャツにアイロンをかけてしわを伸ばした。", "シャツにアイロンをかけてしわをのばした。", "I ironed the shirt to smooth out the creases.", VOC7D2)
V("子どもの才能を伸ばす", "こどものさいのうをのばす", "Develop a child's talent", "子どもの才能を伸ばすような教育をしよう。", "こどものさいのうをのばすようなきょういくをしよう。", "Let's provide education that develops children's talents.", VOC7D2)

# --- Vocabulary Day 3: 意味がたくさんある言葉③ (multi-meaning words) ---
VOC7D3 = "vocabulary::w7 vocabulary::w7d3 jlpt::n2"
V("軽いけが", "かるいけが", "A slight injury", "軽いけがだったので、すぐに帰宅できた。", "かるいけがだったので、すぐにきたくできた。", "It was a slight injury, so I could go home right away.", VOC7D3)
V("重いけが", "おもいけが", "A serious injury", "事故で重いけがを負った。", "じこでおもいけがをおった。", "He sustained a serious injury in the accident.", VOC7D3)
V("台風の被害が軽い", "たいふうのひがいがかるい", "The typhoon damage is minimal", "今年の台風の被害は軽かった。", "ことしのたいふうのひがいはかるかった。", "This year's typhoon damage was minimal.", VOC7D3)
V("軽く運動する", "かるくうんどうする", "Do light exercise", "毎朝、軽く運動するようにしている。", "まいあさ、かるくうんどうするようにしている。", "I try to do light exercise every morning.", VOC7D3)
V("激しく運動する", "はげしくうんどうする", "Exercise intensely", "彼は毎日激しく運動している。", "かれはまいにちはげしくうんどうしている。", "He exercises intensely every day.", VOC7D3)
V("軽い罪", "かるいつみ", "A minor offense", "彼が犯したのは軽い罪だった。", "かれがおかしたのはかるいつみだった。", "What he committed was a minor offense.", VOC7D3)
V("重い罪", "おもいつみ", "A serious crime", "彼は重い罪を犯して逮捕された。", "かれはおもいつみをおかしてたいほされた。", "He committed a serious crime and was arrested.", VOC7D3)
V("気持ちが軽くなる", "きもちがかるくなる", "Feel relieved / lighthearted", "試験が終わって気持ちが軽くなった。", "しけんがおわってきもちがかるくなった。", "I felt relieved after the exam was over.", VOC7D3)
V("気持ちが重くなる", "きもちがおもくなる", "Feel down / heavy-hearted", "悪いニュースを聞いて気持ちが重くなった。", "わるいニュースをきいてきもちがおもくなった。", "I felt heavy-hearted after hearing the bad news.", VOC7D3)
V("親の負担が軽くなる", "おやのふたんがかるくなる", "A parent's burden becomes lighter", "息子が就職して親の負担が軽くなった。", "むすこがしゅうしょくしておやのふたんがかるくなった。", "The parents' burden became lighter after their son got a job.", VOC7D3)
V("親の負担が重くなる", "おやのふたんがおもくなる", "A parent's burden becomes heavier", "子どもが増えて親の負担が重くなった。", "こどもがふえておやのふたんがおもくなった。", "The parents' burden became heavier as they had more children.", VOC7D3)
V("口が軽い", "くちがかるい", "Can't keep a secret / loose-lipped", "彼は口が軽いので、秘密を話さないほうがいい。", "かれはくちがかるいので、ひみつをはなさないほうがいい。", "He can't keep a secret, so it's better not to tell him anything private.", VOC7D3)
V("口がかたい", "くちがかたい", "Tight-lipped / discreet", "彼女は口がかたいから、安心して相談できる。", "かのじょはくちがかたいから、あんしんしてそうだんできる。", "She is discreet, so I can consult her with peace of mind.", VOC7D3)
V("軽い気持ちで引き受ける", "かるいきもちでひきうける", "Accept without much thought", "軽い気持ちで引き受けたが、大変な仕事だった。", "かるいきもちでひきうけたが、たいへんなしごとだった。", "I accepted it without much thought, but it turned out to be a difficult job.", VOC7D3)
V("体が軽くなる", "からだがかるくなる", "Feel refreshed (physically light)", "マッサージを受けたら、体が軽くなった。", "マッサージをうけたら、からだがかるくなった。", "After getting a massage, I felt physically refreshed.", VOC7D3)
V("体が重くなる", "からだがおもくなる", "Feel physically heavy / sluggish", "風邪をひくと体が重くなる。", "かぜをひくとからだがおもくなる。", "When I catch a cold, my body feels heavy.", VOC7D3)
V("暗い夜道を歩く", "くらいよみちをあるく", "Walk a dark road at night", "一人で暗い夜道を歩くのは危険だ。", "ひとりでくらいよみちをあるくのはきけんだ。", "Walking alone on a dark road at night is dangerous.", VOC7D3)
V("暗い色のシャツ", "くらいいろのシャツ", "A dark colored shirt", "彼はいつも暗い色のシャツを着ている。", "かれはいつもくらいいろのシャツをきている。", "He always wears dark colored shirts.", VOC7D3)
V("明るい色のシャツ", "あかるいいろのシャツ", "A bright colored shirt", "夏には明るい色のシャツがよく似合う。", "なつにはあかるいいろのシャツがよくにあう。", "Bright colored shirts suit summer well.", VOC7D3)
V("暗い声で話す", "くらいこえではなす", "Speak in a low, sad voice", "彼は暗い声で話すので、心配になった。", "かれはくらいこえではなすので、しんぱいになった。", "He spoke in such a low, sad voice that I got worried.", VOC7D3)
V("明るい声で話す", "あかるいこえではなす", "Speak in a cheerful voice", "彼女はいつも明るい声で話す。", "かのじょはいつもあかるいこえではなす。", "She always speaks in a cheerful voice.", VOC7D3)
V("将来の見通しが暗い", "しょうらいのみとおしがくらい", "The outlook for the future is dim", "この業界は将来の見通しが暗い。", "このぎょうかいはしょうらいのみとおしがくらい。", "This industry's future outlook is dim.", VOC7D3)
V("将来の見通しが明るい", "しょうらいのみとおしがあかるい", "The outlook for the future is bright", "彼の会社は将来の見通しが明るい。", "かれのかいしゃはしょうらいのみとおしがあかるい。", "His company's future outlook is bright.", VOC7D3)
V("暗い過去がある", "くらいかこがある", "Have a dark (sad) past", "彼女には誰にも言えない暗い過去がある。", "かのじょにはだれにもいえないくらいかこがある。", "She has a dark past that she can't tell anyone about.", VOC7D3)
V("政治に暗い", "せいじにくらい", "Know very little about politics", "最近の学生は政治に暗い。", "さいきんのがくせいはせいじにくらい。", "Students these days know very little about politics.", VOC7D3)
V("政治に明るい", "せいじにあかるい", "Be knowledgeable about politics", "彼は政治に明るいので、よく相談する。", "かれはせいじにあかるいので、よくそうだんする。", "He's knowledgeable about politics, so I often consult him.", VOC7D3)
V("高い技術", "たかいぎじゅつ", "High-level technology/skill", "この会社は高い技術を持っている。", "このかいしゃはたかいぎじゅつをもっている。", "This company has high-level technology.", VOC7D3)
V("芸術への関心が高い", "げいじゅつへのかんしんがたかい", "Be very interested in art", "彼女は芸術への関心が高い。", "かのじょはげいじゅつへのかんしんがたかい。", "She is very interested in art.", VOC7D3)
V("芸術への関心が低い", "げいじゅつへのかんしんがひくい", "Have little interest in art", "最近の若者は芸術への関心が低いと言われる。", "さいきんのわかものはげいじゅつへのかんしんがひくいといわれる。", "It's said that young people these days have little interest in art.", VOC7D3)
V("理想が高い", "りそうがたかい", "Aim high / have high ideals", "彼女は理想が高くて、なかなか結婚相手が見つからない。", "かのじょはりそうがたかくて、なかなかけっこんあいてがみつからない。", "Her ideals are so high that she can't easily find a marriage partner.", VOC7D3)
V("理想が低い", "りそうがひくい", "Have low ideals / not aim high", "理想が低いと、成長する機会を逃してしまう。", "りそうがひくいと、せいちょうするきかいをのがしてしまう。", "If your ideals are low, you'll miss opportunities to grow.", VOC7D3)
V("鼻が高い", "はながたかい", "Be proud of (something)", "息子が試験に合格して、鼻が高い。", "むすこがしけんにごうかくして、はながたかい。", "I'm proud that my son passed the exam.", VOC7D3)
V("格式が高いホテル", "かくしきがたかいホテル", "A high-class hotel", "このホテルはとても格式が高く、宿泊費も相当かかる。", "このホテルはとてもかくしきがたかく、しゅくはくひもそうとうかかる。", "This hotel is very high-class, and the lodging fee is quite high too.", VOC7D3)
V("ベルトがきつい", "ベルトがきつい", "The belt is too tight", "食べ過ぎてベルトがきつくなった。", "たべすぎてベルトがきつくなった。", "I ate too much and now my belt is too tight.", VOC7D3)
V("きついけいこ", "きついけいこ", "Very hard training", "毎日きついけいこを続けている。", "まいにちきついけいこをつづけている。", "I keep up hard training every day.", VOC7D3)
V("早起きはきつい", "はやおきはきつい", "It's hard to get up early", "冬の早起きはきつい。", "ふゆのはやおきはきつい。", "Getting up early in winter is hard.", VOC7D3)
V("きつく注意する", "きつくちゅういする", "Give a severe scolding / strict warning", "何度も遅刻したので、先生にきつく注意された。", "なんどもちこくしたので、せんせいにきつくちゅういされた。", "Because I was late many times, I was given a strict warning by the teacher.", VOC7D3)
V("この旅行の日程はきつい", "このりょこうのにっていはきつい", "The trip itinerary is tight", "この旅行の日程はきつくて、休む暇がない。", "このりょこうのにっていはきつくて、やすむひまがない。", "This trip's itinerary is so tight there's no time to rest.", VOC7D3)
V("余裕がある", "よゆうがある", "Have leeway / room to spare", "今日のスケジュールは余裕がある。", "きょうのスケジュールはよゆうがある。", "Today's schedule has plenty of leeway.", VOC7D3)
V("妻はきつい性格の女性だ", "つまはきついせいかくのじょせいだ", "My wife has a very strong (aggressive) personality", "妻はきつい性格の女性だ。", "つまはきついせいかくのじょせいだ。", "My wife has a very strong (aggressive) personality.", VOC7D3)
V("びんのふたがきつくて開かない", "びんのふたがきつくてあかない", "The lid is too tight to open", "びんのふたがきつくて開かない。", "びんのふたがきつくてあかない。", "The lid is too tight to open.", VOC7D3)
V("今日は日差しがきつい", "きょうはひざしがきつい", "The sun is beaming (very strong) today", "夏の日差しはきつい。", "なつのひざしはきつい。", "The summer sunlight is intense.", VOC7D3)
V("きつい酒", "きついさけ", "Hard liquor / strong alcohol", "彼はきつい酒を好んで飲む。", "かれはきついさけをこのんでのむ。", "He likes to drink hard liquor.", VOC7D3)
V("軽い酒", "かるいさけ", "Light alcohol", "パーティーでは軽い酒を飲んだ。", "パーティーではかるいさけをのんだ。", "I drank light alcohol at the party.", VOC7D3)
V("目つきがきつい", "めつきがきつい", "A stern look / sharp eyes", "彼は目つきがきつくて、少し怖い。", "かれはめつきがきつくて、すこしこわい。", "He has a stern look, which is a little scary.", VOC7D3)

# --- Vocabulary Day 4: 言葉の前につく語 (prefixes) ---
VOC7D4 = "vocabulary::w7 vocabulary::w7d4 jlpt::n2"
V("不可能（な）", "ふかのう（な）", "Impossible", "彼にこの仕事を一人で終わらせるのは不可能だ。", "かれにこのしごとをひとりでおわらせるのはふかのうだ。", "It's impossible for him to finish this job alone.", VOC7D4)
V("不必要（な）", "ふひつよう（な）", "Unnecessary", "この書類には不必要な情報が多い。", "このしょるいにはふひつようなじょうほうがおおい。", "This document has a lot of unnecessary information.", VOC7D4)
V("不愉快（な）", "ふゆかい（な）", "Unpleasant", "彼の態度はとても不愉快だった。", "かれのたいどはとてもふゆかいだった。", "His attitude was very unpleasant.", VOC7D4)
V("不健康（な）", "ふけんこう（な）", "Unhealthy", "毎日ファストフードを食べるのは不健康だ。", "まいにちファストフードをたべるのはふけんこうだ。", "Eating fast food every day is unhealthy.", VOC7D4)
V("無差別", "むさべつ", "Indiscriminate", "無差別なテロ攻撃が起きた。", "むさべつなテロこうげきがおきた。", "An indiscriminate terrorist attack occurred.", VOC7D4)
V("無関心（な）", "むかんしん（な）", "Indifferent", "彼は政治に無関心だ。", "かれはせいじにむかんしんだ。", "He is indifferent to politics.", VOC7D4)
V("無関係（な）", "むかんけい（な）", "Unrelated", "この事件は私とは無関係だ。", "このじけんはわたしとはむかんけいだ。", "This incident is unrelated to me.", VOC7D4)
V("無意識", "むいしき", "Unconscious", "彼は無意識のうちに手を挙げていた。", "かれはむいしきのうちにてをあげていた。", "He raised his hand unconsciously.", VOC7D4)
V("非常識（な）", "ひじょうしき（な）", "Lacking common sense", "夜中に電話をかけるのは非常識だ。", "よなかにでんわをかけるのはひじょうしきだ。", "Calling someone in the middle of the night shows a lack of common sense.", VOC7D4)
V("非科学的（な）", "ひかがくてき（な）", "Unscientific", "その説明は非科学的だ。", "そのせつめいはひかがくてきだ。", "That explanation is unscientific.", VOC7D4)
V("非公開", "ひこうかい", "Closed / not open to the public", "この会議は非公開で行われた。", "このかいぎはひこうかいでおこなわれた。", "This meeting was held behind closed doors.", VOC7D4)
V("非公式", "ひこうしき", "Unofficial", "非公式に発表された情報だ。", "ひこうしきにはっぴょうされたじょうほうだ。", "This information was announced unofficially.", VOC7D4)
V("未完成", "みかんせい", "Incomplete", "この小説はまだ未完成だ。", "このしょうせつはまだみかんせいだ。", "This novel is still incomplete.", VOC7D4)
V("未解決", "みかいけつ", "Unsolved", "その事件はいまだに未解決です。", "そのじけんはいまだにみかいけつです。", "That case is still unsolved.", VOC7D4)
V("再出発（する）", "さいしゅっぱつ（する）", "A new start / starting over", "彼は失敗から立ち直り、再出発した。", "かれはしっぱいからたちなおり、さいしゅっぱつした。", "He recovered from his failure and made a new start.", VOC7D4)
V("再認識（する）", "さいにんしき（する）", "Realize again / new realization", "健康の大切さを再認識した。", "けんこうのたいせつさをさいにんしきした。", "I realized once again the importance of health.", VOC7D4)
V("再生産（する）", "さいせいさん（する）", "Reproduction", "この工場では部品の再生産を行っている。", "このこうじょうではぶひんのさいせいさんをおこなっている。", "This factory carries out the reproduction of parts.", VOC7D4)
V("再開発（する）", "さいかいはつ（する）", "Redevelopment", "駅前の再開発が進んでいる。", "えきまえのさいかいはつがすすんでいる。", "Redevelopment near the station is progressing.", VOC7D4)
V("超満員", "ちょうまんいん", "Extremely full/crowded", "朝のラッシュ時、電車はいつも超満員です。", "あさのラッシュじ、でんしゃはいつもちょうまんいんです。", "During the morning rush, the train is always extremely crowded.", VOC7D4)
V("超特急", "ちょうとっきゅう", "A super express", "新幹線は以前、「夢の超特急」と呼ばれていたことがあった。", "しんかんせんはいぜん、「ゆめのちょうとっきゅう」とよばれていたことがあった。", "The Shinkansen used to be called the 'dream super express.'", VOC7D4)
V("超小型", "ちょうこがた", "Micro / very small", "この会社は超小型のカメラを開発した。", "このかいしゃはちょうこがたのカメラをかいはつした。", "This company developed a micro camera.", VOC7D4)
V("超忙しい", "ちょういそがしい", "Extremely busy", "今週は超忙しくて、休む暇もない。", "こんしゅうはちょういそがしくて、やすむひまもない。", "I'm extremely busy this week, with no time to rest.", VOC7D4)
V("高カロリー", "こうカロリー", "High calorie", "揚げ物は高カロリーな食べ物だ。", "あげものはこうカロリーなたべものだ。", "Fried food is high in calories.", VOC7D4)
V("高収入", "こうしゅうにゅう", "A high income", "彼は高収入の仕事に就いている。", "かれはこうしゅうにゅうのしごとについている。", "He has a high-income job.", VOC7D4)
V("高気圧", "こうきあつ", "High pressure (weather)", "今週末は高気圧に覆われて晴れるでしょう。", "こんしゅうまつはこうきあつにおおわれてはれるでしょう。", "This weekend will be covered by high pressure and clear.", VOC7D4)
V("名場面", "めいばめん", "A famous scene", "あの映画には名場面がたくさんある。", "あのえいがにはめいばめんがたくさんある。", "That movie has many famous scenes.", VOC7D4)
V("名女優", "めいじょゆう", "A famous/great actress", "彼女は日本を代表する名女優だ。", "かのじょはにほんをだいひょうするめいじょゆうだ。", "She is a great actress representing Japan.", VOC7D4)
V("名演奏", "めいえんそう", "A great performance (music)", "観客はフルートの名演奏に耳を傾けた。", "かんきゃくはフルートのめいえんそうにみみをかたむけた。", "The audience listened to the great flute performance.", VOC7D4)
V("全世界", "ぜんせかい", "The whole world", "そのニュースは全世界に伝えられた。", "そのニュースはぜんせかいにつたえられた。", "That news was conveyed to the whole world.", VOC7D4)
V("全日本", "ぜんにほん", "All Japan / national", "全日本大会で優勝した。", "ぜんにほんたいかいでゆうしょうした。", "We won the all-Japan tournament.", VOC7D4)
V("全学生", "ぜんがくせい", "All students", "全学生が試験を受けた。", "ぜんがくせいがしけんをうけた。", "All students took the exam.", VOC7D4)
V("全責任", "ぜんせきにん", "Entire responsibility", "彼がこのプロジェクトの全責任を負っている。", "かれがこのプロジェクトのぜんせきにんをおっている。", "He bears the entire responsibility for this project.", VOC7D4)
V("総人数", "そうにんずう", "The total number of people", "参加者の総人数は100人だった。", "さんかしゃのそうにんずうは100にんだった。", "The total number of participants was 100.", VOC7D4)
V("総収入", "そうしゅうにゅう", "Total income", "彼の家族の総収入は年間800万円だ。", "かれのかぞくのそうしゅうにゅうはねんかん800まんえんだ。", "His family's total income is 8 million yen per year.", VOC7D4)
V("各クラス", "かくクラス", "Each class", "各クラスの代表が集まった。", "かくクラスのだいひょうがあつまった。", "The representative of each class gathered.", VOC7D4)
V("各家庭", "かくかてい", "Each household", "各家庭にお知らせを配布した。", "かくかていにおしらせをはいふした。", "We distributed a notice to each household.", VOC7D4)
V("長持ち（する）", "ながもち（する）", "Long-lasting", "この電池は長持ちする。", "このでんちはながもちする。", "This battery is long-lasting.", VOC7D4)
V("長生き（する）", "ながいき（する）", "Long-living", "祖父は長生きしている。", "そふはながいきしている。", "My grandfather is living a long life.", VOC7D4)
V("長話（する）", "ながばなし（する）", "A long talk", "近所の人と長話をしてしまった。", "きんじょのひととながばなしをしてしまった。", "I ended up having a long talk with my neighbor.", VOC7D4)
V("長電話（する）", "ながでんわ（する）", "A long phone conversation", "友達と長電話をした。", "ともだちとながでんわをした。", "I had a long phone conversation with my friend.", VOC7D4)
V("現社長", "げんしゃちょう", "Current president", "現社長は先月就任したばかりだ。", "げんしゃちょうはせんげつしゅうにんしたばかりだ。", "The current president just took office last month.", VOC7D4)
V("現大臣", "げんだいじん", "Current minister", "現大臣が記者会見を行った。", "げんだいじんがきしゃかいけんをおこなった。", "The current minister held a press conference.", VOC7D4)
V("前社長", "ぜんしゃちょう", "Ex-president (the one immediately prior)", "前社長のアドバイスで会社は成長した。", "ぜんしゃちょうのアドバイスでかいしゃはせいちょうした。", "The company grew thanks to advice from the former president.", VOC7D4)
V("前大臣", "ぜんだいじん", "Ex-minister (the one immediately prior)", "前大臣が今の政策を批判した。", "ぜんだいじんがいまのせいさくをひはんした。", "The former minister criticized the current policy.", VOC7D4)
V("元社長", "もとしゃちょう", "Ex-president (in the past)", "元社長は今も会社の相談役を務めている。", "もとしゃちょうはいまもかいしゃのそうだんやくをつとめている。", "The former president still serves as an advisor to the company.", VOC7D4)
V("元大臣", "もとだいじん", "Ex-minister (in the past)", "元大臣が新しい政党を立ち上げた。", "もとだいじんがあたらしいせいとうをたちあげた。", "A former minister launched a new political party.", VOC7D4)
V("故田中社長", "こたなかしゃちょう", "The late President Tanaka", "故田中社長の功績をたたえた。", "こたなかしゃちょうのこうせきをたたえた。", "We honored the achievements of the late President Tanaka.", VOC7D4)
V("故田中大臣", "こたなかだいじん", "The late Minister Tanaka", "故田中大臣の写真が飾られている。", "こたなかだいじんのしゃしんがかざられている。", "A photo of the late Minister Tanaka is displayed.", VOC7D4)
V("副社長", "ふくしゃちょう", "Vice-president", "急病の社長のかわりに副社長が出席した。", "きゅうびょうのしゃちょうのかわりにふくしゃちょうがしゅっせきした。", "The vice-president attended in place of the sick president.", VOC7D4)
V("副大臣", "ふくだいじん", "Vice-minister", "副大臣が代わりに出席した。", "ふくだいじんがかわりにしゅっせきした。", "The vice-minister attended instead.", VOC7D4)
V("副作用", "ふくさよう", "A side effect", "この薬には副作用がある。", "このくすりにはふくさようがある。", "This medicine has side effects.", VOC7D4)

# --- Vocabulary Day 5: 言葉の後ろにつく語① (suffixes) ---
VOC7D5 = "vocabulary::w7 vocabulary::w7d5 jlpt::n2"
V("入学金", "にゅうがくきん", "An admission fee", "大学の入学金を払い込んだ。", "だいがくのにゅうがくきんをはらいこんだ。", "I paid the university's admission fee.", VOC7D5)
V("奨学金", "しょうがくきん", "A scholarship", "彼は奨学金をもらって大学に通っている。", "かれはしょうがくきんをもらってだいがくにかよっている。", "He attends university on a scholarship.", VOC7D5)
V("売上金", "うりあげきん", "Proceeds / sales revenue", "売上金を銀行に預けた。", "うりあげきんをぎんこうにあずけた。", "I deposited the proceeds at the bank.", VOC7D5)
V("授業料", "じゅぎょうりょう", "A tuition fee", "私立大学の授業料は高い。", "しりつだいがくのじゅぎょうりょうはたかい。", "Private university tuition fees are expensive.", VOC7D5)
V("入場料", "にゅうじょうりょう", "An entrance fee", "美術館の入場料を払った。", "びじゅつかんのにゅうじょうりょうをはらった。", "I paid the museum's entrance fee.", VOC7D5)
V("運送料", "うんそうりょう", "A shipping charge", "アメリカに荷物を送るときの運送料はとても高い。", "アメリカににもつをおくるときのうんそうりょうはとてもたかい。", "The shipping charge for sending luggage to America is very expensive.", VOC7D5)
V("拝観料", "はいかんりょう", "An admission fee (for a temple/shrine)", "この寺の拝観料はいくらですか。", "このてらのはいかんりょうはいくらですか。", "How much is the admission fee for this temple?", VOC7D5)
V("宿泊費", "しゅくはくひ", "Accommodation fees", "出張の宿泊費は会社が負担する。", "しゅっちょうのしゅくはくひはかいしゃがふたんする。", "The company covers the accommodation fees for the business trip.", VOC7D5)
V("生活費", "せいかつひ", "Living expenses", "一人暮らしの生活費は月に10万円ほどだ。", "ひとりぐらしのせいかつひはつきに10まんえんほどだ。", "Living expenses for living alone are about 100,000 yen a month.", VOC7D5)
V("医療費", "いりょうひ", "Medical expenses", "今月は医者に何度も行ったので、医療費が高くついた。", "こんげつはいしゃになんどもいったので、いりょうひがたかくついた。", "I went to the doctor many times this month, so the medical expenses were high.", VOC7D5)
V("本代", "ほんだい", "Book expenses", "毎月、本代に1万円くらい使う。", "まいつき、ほんだいに1まんえんくらいつかう。", "I spend about 10,000 yen a month on books.", VOC7D5)
V("電気代", "でんきだい", "Electricity bill", "8月の電気代はとても高かった。", "8がつのでんきだいはとてもたかかった。", "August's electricity bill was very expensive.", VOC7D5)
V("修理代", "しゅうりだい", "A repair bill", "ぶつけた車の修理代の請求書が来ました。", "ぶつけたくるまのしゅうりだいのせいきゅうしょがきました。", "The bill for the repair of the car I hit arrived.", VOC7D5)
V("バス代", "バスだい", "Bus fare", "バス代が値上がりした。", "バスだいがねあがりした。", "Bus fare went up.", VOC7D5)
V("借り賃", "かりちん", "Rent (for borrowing something)", "この部屋の借り賃は月8万円だ。", "このへやのかりちんはつき8まんえんだ。", "The rent for this room is 80,000 yen a month.", VOC7D5)
V("貸し賃", "かしちん", "Rent (for lending something)", "駐車場の貸し賃を毎月受け取っている。", "ちゅうしゃじょうのかしちんをまいつきうけとっている。", "I receive rent for the parking space every month.", VOC7D5)
V("電車賃", "でんしゃちん", "Train fare", "家は広いが、遠くなったので電車賃が前よりかかる。", "いえはひろいが、とおくなったのででんしゃちんがまえよりかかる。", "The house is spacious, but since it's farther away, the train fare costs more than before.", VOC7D5)
V("手間賃", "てまちん", "Pay for labor", "修理を手伝って、手間賃をもらった。", "しゅうりをてつだって、てまちんをもらった。", "I helped with the repair and got paid for my labor.", VOC7D5)
V("時間内に書き終える", "じかんないにかきおえる", "Finish writing within the time limit", "レポートを時間内に書き終えた。", "レポートをじかんないにかきおえた。", "I finished writing the report within the time limit.", VOC7D5)
V("予算内に収まる", "よさんないにおさまる", "Be within the budget", "工事費用は予算内に収まった。", "こうじひようはよさんないにおさまった。", "The construction costs stayed within the budget.", VOC7D5)
V("期限内に支払う", "きげんないにしはらう", "Pay before the deadline", "電気代は期限内に支払わなければならない。", "でんきだいはきげんないにしはらわなければならない。", "The electricity bill must be paid before the deadline.", VOC7D5)
V("予想外の結果", "よそうがいのけっか", "An unexpected result", "その事件は予想外の結果を迎え、だれもが驚いた。", "そのじけんはよそうがいのけっかをむかえ、だれもがおどろいた。", "The incident led to an unexpected result, and everyone was surprised.", VOC7D5)
V("範囲外の問題", "はんいがいのもんだい", "Unanticipated questions (outside the scope)", "試験には範囲外の問題が出た。", "しけんにははんいがいのもんだいがでた。", "Questions outside the scope appeared on the exam.", VOC7D5)
V("時間外労働", "じかんがいろうどう", "Overtime work", "時間外労働とは、言いかえると「残業」である。", "じかんがいろうどうとは、いいかえると「ざんぎょう」である。", "Overtime work, in other words, is 'zangyo.'", VOC7D5)
V("代表的な映画", "だいひょうてきなえいが", "A typical/representative movie", "『七人の侍』は日本の代表的な映画だ。", "『しちにんのさむらい』はにほんのだいひょうてきなえいがだ。", "'Seven Samurai' is a representative Japanese movie.", VOC7D5)
V("日常的な出来事", "にちじょうてきなできごと", "A daily event", "電車の遅延は日常的な出来事だ。", "でんしゃのちえんはにちじょうてきなできごとだ。", "Train delays are a daily occurrence.", VOC7D5)
V("比較的大きい", "ひかくてきおおきい", "Comparatively big", "この部屋は比較的大きい。", "このへやはひかくてきおおきい。", "This room is comparatively big.", VOC7D5)
V("進歩的な考え", "しんぽてきなかんがえ", "A progressive idea", "彼は進歩的な考えを持っている。", "かれはしんぽてきなかんがえをもっている。", "He has progressive ideas.", VOC7D5)
V("サラリーマン風の男", "サラリーマンふうのおとこ", "A man who looks like a businessman", "駅前でサラリーマン風の男を見かけた。", "えきまえでサラリーマンふうのおとこをみかけた。", "I saw a man who looked like a businessman near the station.", VOC7D5)
V("西洋風の建物", "せいようふうのたてもの", "A western style building", "この街には西洋風の建物が多い。", "このまちにはせいようふうのたてものがおおい。", "There are many western-style buildings in this town.", VOC7D5)
V("関西風の味付け", "かんさいふうのあじつけ", "Kansai style seasoning", "このうどんは関西風の味付けだ。", "このうどんはかんさいふうのあじつけだ。", "This udon has Kansai-style seasoning.", VOC7D5)
V("立体感のある絵", "りったいかんのあるえ", "A painting with a 3D effect", "この絵はとても立体感がある。", "このえはとてもりったいかんがある。", "This painting has a great sense of depth.", VOC7D5)
V("開放感を味わう", "かいほうかんをあじわう", "Enjoy the sense of freedom", "海を見ると開放感を味わえる。", "うみをみるとかいほうかんをあじわえる。", "Looking at the sea gives me a sense of freedom.", VOC7D5)
V("存在感がある人", "そんざいかんがあるひと", "A person who makes their presence felt", "彼は存在感がある人だ。", "かれはそんざいかんがあるひとだ。", "He is a person who makes his presence felt.", VOC7D5)
V("安全性を確かめる", "あんぜんせいをたしかめる", "Ensure/confirm safety", "新しい橋の安全性を確かめた。", "あたらしいはしのあんぜんせいをたしかめた。", "We confirmed the safety of the new bridge.", VOC7D5)
V("可能性を試す", "かのうせいをためす", "Explore the possibility", "新しい治療法の可能性を試している。", "あたらしいちりょうほうのかのうせいをためしている。", "We are exploring the possibility of a new treatment.", VOC7D5)
V("植物性の油", "しょくぶつせいのあぶら", "Vegetable oil", "この料理には植物性の油を使っている。", "このりょうりにはしょくぶつせいのあぶらをつかっている。", "This dish uses vegetable oil.", VOC7D5)
V("日本製のカメラ", "にほんせいのカメラ", "A camera made in Japan", "彼は日本製のカメラを買った。", "かれはにほんせいのカメラをかった。", "He bought a camera made in Japan.", VOC7D5)
V("スチール製の机", "スチールせいのつくえ", "A steel desk", "オフィスにはスチール製の机が並んでいる。", "オフィスにはスチールせいのつくえがならんでいる。", "Steel desks are lined up in the office.", VOC7D5)
V("経営の合理化", "けいえいのごうりか", "Streamlining of the company/business", "会社は経営の合理化を進めている。", "かいしゃはけいえいのごうりかをすすめている。", "The company is proceeding with the streamlining of its business.", VOC7D5)
V("機械化", "きかいか", "Automation / mechanization", "工場の作業は機械化が進んでいる。", "こうじょうのさぎょうはきかいかがすすんでいる。", "Factory work is becoming increasingly mechanized.", VOC7D5)
V("高齢化", "こうれいか", "Aging (population)", "日本は高齢化が進んでいる。", "にほんはこうれいかがすすんでいる。", "Japan's population is aging.", VOC7D5)
V("少子化", "しょうしか", "Declining birth-rate", "少子化は深刻な社会問題だ。", "しょうしかはしんこくなしゃかいもんだいだ。", "The declining birth rate is a serious social problem.", VOC7D5)
V("季節の変わり目", "きせつのかわりめ", "When the season changes / transition of seasons", "季節の変わり目に体調をくずすことが多い。", "きせつのかわりめにたいちょうをくずすことがおおい。", "People often get sick during the change of seasons.", VOC7D5)
V("見た目が悪い", "みためがわるい", "Looks bad (in appearance)", "この料理は味はいいが、見た目が悪い。", "このりょうりはあじはいいが、みためがわるい。", "This dish tastes good, but it looks bad.", VOC7D5)
V("ズボンの折り目", "ズボンのおりめ", "A crease in the pants", "アイロンでズボンの折り目をきれいにつけた。", "アイロンでズボンのおりめをきれいにつけた。", "I neatly pressed a crease into the pants with the iron.", VOC7D5)

# --- Vocabulary Day 6: 言葉の後ろにつく語② (suffixes) ---
# Day 7 (実戦問題) is a pure review/practice test with 25 multiple-choice questions and no new
# vocabulary of its own (answer key lives in a separate booklet not included in the source) --
# confirmed, not an oversight, matching the established Day-7-is-review pattern.
VOC7D6 = "vocabulary::w7 vocabulary::w7d6 jlpt::n2"
V("りんごを丸ごとかじる", "りんごをまるごとかじる", "Bite into a whole apple", "子どもがりんごを丸ごとかじった。", "こどもがりんごをまるごとかじった。", "The child bit into a whole apple.", VOC7D6)
V("りんごを皮ごと食べる", "りんごをかわごとたべる", "Eat an apple with the skin on (unpeeled)", "健康のためにりんごを皮ごと食べている。", "けんこうのためにりんごをかわごとたべている。", "I eat apples with the skin on for my health.", VOC7D6)
V("ケースごと宝石が盗まれた", "ケースごとほうせきがぬすまれた", "The jewelry box and its contents were stolen", "泥棒に入られて、ケースごと宝石が盗まれた。", "どろぼうにはいられて、ケースごとほうせきがぬすまれた。", "A burglar broke in, and the jewelry box and its contents were stolen.", VOC7D6)
V("一雨ごとに暖かくなる", "ひとあめごとにあたたかくなる", "It gets warmer with each rain", "春は一雨ごとに暖かくなる。", "はるはひとあめごとにあたたかくなる。", "In spring, it gets warmer with each rainfall.", VOC7D6)
V("ちらしを家ごとに配る", "ちらしをいえごとにくばる", "Put a flyer in each mailbox", "選挙のちらしを家ごとに配った。", "せんきょのちらしをいえごとにくばった。", "We distributed election flyers to each household.", VOC7D6)
V("失敗するごとに上達する", "しっぱいするごとにじょうたつする", "Improve with each mistake / learn from one's mistakes", "彼は失敗するごとに上達している。", "かれはしっぱいするごとにじょうたつしている。", "He improves with each mistake he makes.", VOC7D6)
V("バスが5分おきに来る", "バスが5ふんおきにくる", "The bus runs every five minutes", "この路線はバスが5分おきに来る。", "このろせんはバスが5ふんおきにくる。", "On this route, the bus comes every five minutes.", VOC7D6)
V("1行おきに書く", "1ぎょうおきにかく", "Write on every other line", "レポートは1行おきに書いてください。", "レポートは1ぎょうおきにかいてください。", "Please write the report on every other line.", VOC7D6)
V("仕事ぶり", "しごとぶり", "How he works / his work style", "新入社員の仕事ぶりが評価された。", "しんにゅうしゃいんのしごとぶりがひょうかされた。", "The new employee's way of working was praised.", VOC7D6)
V("話しぶり", "はなしぶり", "How he speaks / his manner of speaking", "彼の話しぶりには自信があふれていた。", "かれのはなしぶりにはじしんがあふれていた。", "His manner of speaking was full of confidence.", VOC7D6)
V("身ぶり", "みぶり", "Body language / gestures", "言葉が通じないので、身ぶりで伝えた。", "ことばがつうじないので、みぶりでつたえた。", "Since we couldn't communicate verbally, I conveyed it through gestures.", VOC7D6)
V("彼と5年ぶりに会った", "かれと5ねんぶりにあった", "I saw him for the first time in 5 years", "駅で彼と5年ぶりに会った。", "えきでかれと5ねんぶりにあった。", "I met him at the station for the first time in 5 years.", VOC7D6)
V("忘れがたい思い出", "わすれがたいおもいで", "An unforgettable memory", "留学は忘れがたい思い出になった。", "りゅうがくはわすれがたいおもいでになった。", "Studying abroad became an unforgettable memory.", VOC7D6)
V("その要求は認めがたい", "そのようきゅうはみとめがたい", "That demand cannot be readily approved", "その要求は認めがたい。", "そのようきゅうはみとめがたい。", "That demand is hard to accept.", VOC7D6)
V("信じがたい事件", "しんじがたいじけん", "An unbelievable incident", "信じがたい事件が起きた。", "しんじがたいじけんがおきた。", "An unbelievable incident occurred.", VOC7D6)
V("このペンは書きづらい", "このペンはかきづらい", "This pen doesn't write well", "このペンは書きづらいので、別のを使おう。", "このペンはかきづらいので、べつのをつかおう。", "This pen is hard to write with, so let's use a different one.", VOC7D6)
V("歩きづらい道", "あるきづらいみち", "A road difficult to walk on", "雪で歩きづらい道が続いた。", "ゆきであるきづらいみちがつづいた。", "The roads remained difficult to walk on because of the snow.", VOC7D6)
V("言葉づかいが悪い", "ことばづかいがわるい", "Have a foul mouth / use bad language", "彼は先生に対して言葉づかいが悪い。", "かれはせんせいにたいしてことばづかいがわるい。", "He uses bad language toward the teacher.", VOC7D6)
V("金づかいが荒い", "かねづかいがあらい", "Be loose with money / extravagant", "彼は金づかいが荒くて、すぐに貯金がなくなる。", "かれはかねづかいがあらくて、すぐにちょきんがなくなる。", "He is careless with money and quickly runs out of savings.", VOC7D6)
V("人づかいが荒い", "ひとづかいがあらい", "Work one's people hard / drive people hard", "あの上司は人づかいが荒い。", "あのじょうしはひとづかいがあらい。", "That boss drives his people hard.", VOC7D6)
V("パソコンを使いこなす", "パソコンをつかいこなす", "Make full use of the computer", "彼は新しいパソコンを使いこなしている。", "かれはあたらしいパソコンをつかいこなしている。", "He makes full use of his new computer.", VOC7D6)
V("洋服を着こなす", "ようふくをきこなす", "Dress nicely / wear clothes well", "彼女はどんな洋服も上手に着こなす。", "かのじょはどんなようふくもじょうずにきこなす。", "She wears any clothes stylishly.", VOC7D6)
V("顔つき", "かおつき", "A look / facial expression", "彼は真剣な顔つきで話し始めた。", "かれはしんけんなかおつきではなしはじめた。", "He began speaking with a serious look on his face.", VOC7D6)
V("目つき", "めつき", "A look in one's eye", "その子は疑うような目つきで私を見た。", "そのこはうたがうようなめつきでわたしをみた。", "The child looked at me with a suspicious look in their eyes.", VOC7D6)
V("消しゴム付きの鉛筆", "けしゴムつきのえんぴつ", "A pencil with an eraser attached", "子どもに消しゴム付きの鉛筆を買ってあげた。", "こどもにけしゴムつきのえんぴつをかってあげた。", "I bought my child a pencil with an eraser attached.", VOC7D6)
V("一泊二食付き", "いっぱくにしょくつき", "Overnight stay with two meals included", "この旅館は一泊二食付きで1万円だ。", "このりょかんはいっぱくにしょくつきで1まんえんだ。", "This inn costs 10,000 yen for one night with two meals included.", VOC7D6)
V("炊きたてのごはん", "たきたてのごはん", "Freshly cooked rice", "炊きたてのごはんはとてもおいしい。", "たきたてのごはんはとてもおいしい。", "Freshly cooked rice is delicious.", VOC7D6)
V("焼きたてのパン", "やきたてのパン", "Freshly baked bread", "朝、焼きたてのパンを買った。", "あさ、やきたてのパンをかった。", "In the morning, I bought freshly baked bread.", VOC7D6)
V("ペンキ塗りたて", "ペンキぬりたて", "Just painted / wet paint", "ベンチにペンキ塗りたてと書いてあった。", "ベンチにペンキぬりたてとかいてあった。", "It said 'wet paint' on the bench.", VOC7D6)

# --- Extra vocabulary from Grammar Day 4's "もっと！" note on 〜をこめて ---
# 心をこめる -> 心がこもる -> 心のこもった手紙 is a plain word-family aside, not another example of
# the をこめて pattern itself, so it's filed here in Deck 1 (real origin tag kept as grammar::w7d4,
# same precedent as week1's 落ち込む).
GRAM7D4_VOC = "grammar::w7 grammar::w7d4 jlpt::n2"
V("心のこもった手紙", "こころのこもったてがみ", "A heartfelt letter", "彼女から心のこもった手紙をもらった。", "かのじょからこころのこもったてがみをもらった。", "I received a heartfelt letter from her.", GRAM7D4_VOC)

# --- Grammar Day 1: 国籍を問わず ---
GRAM7D1 = "grammar::w7 grammar::w7d1 jlpt::n2 type::grammar"
G("〜もかまわず", "〜もかまわず", "explanation", "Acting without worrying about or being bothered by something",
  [("彼女は人目もかまわず子どものように泣いた。", "かのじょはひとめもかまわずこどものようにないた。", "She cried like a child without caring about how it would appear.")], GRAM7D1)
G("〜もかまわず", "〜もかまわず", "explanation", "Acting without worrying about or being bothered by something",
  [("彼は靴が脱げるのもかまわず走り続けた。", "かれはくつがぬげるのもかまわずはしりつづけた。", "He kept running without caring that his shoes came off.")], GRAM7D1)
G("〜にもかかわらず", "〜にもかかわらず", "explanation", "Doing something despite an obstacle or unexpected situation",
  [("雨にもかかわらず、大勢の人々が集まった。", "あめにもかかわらず、おおぜいのひとびとがあつまった。", "Despite the rain, many people gathered.")], GRAM7D1)
G("〜にもかかわらず", "〜にもかかわらず", "explanation", "Doing something despite an obstacle or unexpected situation",
  [("見たにもかかわらず、彼は見なかったと言った。", "みたにもかかわらず、かれはみなかったといった。", "Though he saw it, he said he didn't.")], GRAM7D1)
G("〜にかかわらず／〜にかかわりなく", "〜にかかわらず／〜にかかわりなく", "explanation", "Doing something regardless of conditions (whether X or Y, age, etc.)",
  [("来る来ないにかかわらず、連絡をください。", "くるこないにかかわらず、れんらくをください。", "Please contact me regardless of whether you are coming or not.")], GRAM7D1)
G("〜にかかわらず／〜にかかわりなく", "〜にかかわらず／〜にかかわりなく", "explanation", "Doing something regardless of conditions (whether X or Y, age, etc.)",
  [("国籍にかかわらず、歓迎します。", "こくせきにかかわらず、かんげいします。", "We welcome anyone regardless of nationality.")], GRAM7D1)
G("〜を問わず", "〜をとわず", "explanation", "A condition (age, gender, etc.) does not matter for the action",
  [("年齢を問わず多くの人々が集まった。", "ねんれいをとわずおおくのひとびとがあつまった。", "Many people of different ages gathered.")], GRAM7D1)
G("〜を問わず", "〜をとわず", "explanation", "A condition (age, gender, etc.) does not matter for the action",
  [("経験の有無を問わず、募集。", "けいけんのうむをとわず、ぼしゅう。", "We are accepting applications, regardless of experience.")], GRAM7D1)
G("〜を問わず", "〜をとわず", "explanation", "A condition (age, gender, etc.) does not matter for the action",
  [("性別は問いません。", "せいべつはといません。", "Regardless of gender.")], GRAM7D1)

# --- Grammar Day 2: クッキーもあればケーキもある ---
GRAM7D2 = "grammar::w7 grammar::w7d2 jlpt::n2 type::grammar"
G("〜やら〜やら", "〜やら〜やら", "explanation", "Listing examples, often overwhelming or chaotic",
  [("机の上は本やらノートやらでいっぱいだ。", "つくえのうえはほんやらノートやらでいっぱいだ。", "The desk is covered with books, notebooks, and so on.")], GRAM7D2)
G("〜やら〜やら", "〜やら〜やら", "explanation", "Listing examples, often overwhelming or chaotic",
  [("この季節は、目がかゆいやら鼻水が出るやら、大変です。", "このきせつは、めがかゆいやらはなみずがでるやら、たいへんです。", "This season is hard because of things like itchy eyes and a runny nose.")], GRAM7D2)
G("〜につけ〜につけ", "〜につけ〜につけ", "explanation", "Whether doing X or Y; in every case of X or Y",
  [("写真を見るにつけ、国を思い出す。", "しゃしんをみるにつけ、くにをおもいだす。", "Photos from my country make me nostalgic.")], GRAM7D2)
G("〜につけ〜につけ", "〜につけ〜につけ", "explanation", "Whether doing X or Y; in every case of X or Y",
  [("いいにつけ悪いにつけ、子は親に似る。", "いいにつけわるいにつけ、こはおやににる。", "Children learn good and bad habits from their parents.")], GRAM7D2)
G("何かにつけ", "なにかにつけ", "explanation", "On every occasion / at every opportunity",
  [("大家さんには何かにつけお世話になっている。", "おおやさんにはなにかにつけおせわになっている。", "I'm indebted to my landlord on every occasion.")], GRAM7D2)
G("何かにつけ", "なにかにつけ", "explanation", "On every occasion / at every opportunity",
  [("何かにつけ心配してくれる母がありがたい。", "なにかにつけしんぱいしてくれるははがありがたい。", "I'm grateful for my mother, who worries about me on every occasion.")], GRAM7D2)
G("〜にしろ〜にしろ／〜にせよ〜にせよ", "〜にしろ〜にしろ／〜にせよ〜にせよ", "explanation", "Whether X or Y; even if X or Y, the outcome is the same",
  [("行くにしろ行かないにしろ、連絡してください。", "いくにしろいかないにしろ、れんらくしてください。", "Please contact me regardless of whether you're going or not.")], GRAM7D2)
G("〜にしろ〜にしろ／〜にせよ〜にせよ", "〜にしろ〜にしろ／〜にせよ〜にせよ", "explanation", "Whether X or Y; even if X or Y, the outcome is the same",
  [("受験はしないにしろ、勉強はしなさい。", "じゅけんはしないにしろ、べんきょうはしなさい。", "Study regardless of whether you take the entrance examinations.")], GRAM7D2)
G("〜も〜ば〜も", "〜も〜ば〜も", "explanation", "Emphasizing that both X and Y share a quality",
  [("彼は勉強もできればスポーツもできる。", "かれはべんきょうもできればスポーツもできる。", "He is outstanding, academically and in sports.")], GRAM7D2)
G("〜も〜ば〜も", "〜も〜ば〜も", "explanation", "Emphasizing that both X and Y share a quality",
  [("私は歌も下手ならダンスも下手だ。", "わたしはうたもへたならダンスもへただ。", "I am bad at singing and at dancing.")], GRAM7D2)

# --- Grammar Day 3: 勉強するものだ ---
GRAM7D3 = "grammar::w7 grammar::w7d3 jlpt::n2 type::grammar"
G("〜ものだ", "〜ものだ", "explanation", "States a general truth/trend, or expresses a wish",
  [("薬は苦いものだ。", "くすりはにがいものだ。", "Medicine is meant to be bitter.")], GRAM7D3)
G("〜ものだ", "〜ものだ", "explanation", "States a general truth/trend, or expresses a wish",
  [("あなたの国へ行ってみたいものだ。", "あなたのくにへいってみたいものだ。", "I wish I could go to your country.")], GRAM7D3)
G("〜ものだ", "〜ものだ", "explanation", "States a general truth/trend, or expresses a wish",
  [("娘には私と同じ仕事はしてほしくないものだ。", "むすめにはわたしとおなじしごとはしてほしくないものだ。", "I do not want my daughter doing the same work as mine.")], GRAM7D3)
G("〜するものではない", "〜するものではない", "explanation", "Giving advice about what one shouldn't do",
  [("目上の人にそんな言い方をするものではない。", "めうえのひとにそんないいかたをするものではない。", "You shouldn't speak like that to someone superior.")], GRAM7D3)
G("〜するものではない", "〜するものではない", "explanation", "Giving advice about what one shouldn't do",
  [("口の中にものを入れたまましゃべるものではない。", "くちのなかにものをいれたまましゃべるものではない。", "You shouldn't speak with your mouth full.")], GRAM7D3)
G("〜というものだ", "〜というものだ", "explanation", "Asserting what something truly amounts to, often critically",
  [("今日中にこれを全部終わらせるのは無理というものだ。", "きょうじゅうにこれをぜんぶおわらせるのはむりというものだ。", "It is impossible to finish this all today.")], GRAM7D3)
G("〜というものだ", "〜というものだ", "explanation", "Asserting what something truly amounts to, often critically",
  [("夜中に電話をしてくるのは非常識というものだ。", "よなかにでんわをしてくるのはひじょうしきというものだ。", "It is unreasonable to call at midnight.")], GRAM7D3)
G("〜ものか", "〜ものか", "explanation", "A strong, emphatic denial or refusal",
  [("あんな店、二度と行くものか。", "あんなみせ、にどといくものか。", "I would never go back to that terrible store again.")], GRAM7D3)
G("〜ものか", "〜ものか", "explanation", "A strong, emphatic denial or refusal",
  [("元気なもんか。くたくただよ。", "げんきなもんか。くたくただよ。", "I don't feel good at all. I'm exhausted.")], GRAM7D3)
G("〜ものか", "〜ものか", "explanation", "A strong, emphatic denial or refusal",
  [("うれしいもんですか。困っているんです。", "うれしいもんですか。こまっているんです。", "I'm not at all pleased. I am not in a good situation.")], GRAM7D3)

# --- Grammar Day 4: 心をこめて ---
GRAM7D4 = "grammar::w7 grammar::w7d4 jlpt::n2 type::grammar"
G("〜を中心に(して)／〜を中心とした", "〜をちゅうしんに(して)／〜をちゅうしんとした", "explanation", "Something is treated as the main focus or core",
  [("東京を中心に関東地方は台風の影響で風が強くなっています。", "とうきょうをちゅうしんにかんとうちほうはたいふうのえいきょうでかぜがつよくなっています。", "In the Kanto Region, especially the Tokyo area, the winds are strong because of a typhoon.")], GRAM7D4)
G("〜を中心に(して)／〜を中心とした", "〜をちゅうしんに(して)／〜をちゅうしんとした", "explanation", "Something is treated as the main focus or core",
  [("この店はスキー用品を中心としたスポーツ専門店です。", "このみせはスキーようひんをちゅうしんとしたスポーツせんもんてんです。", "This sports store sells mainly ski equipment.")], GRAM7D4)
G("〜をこめて", "〜をこめて", "explanation", "Doing something while investing a feeling or intention into it",
  [("感謝の気持ちをこめて編んだマフラーです。", "かんしゃのきもちをこめてあんだマフラーです。", "This is a scarf that I wove as a sign of my gratitude.")], GRAM7D4)
G("〜をこめて", "〜をこめて", "explanation", "Doing something while investing a feeling or intention into it",
  [("愛をこめてカードを贈る。", "あいをこめてカードをおくる。", "Send a card with love.")], GRAM7D4)
G("〜を通じて／〜を通して", "〜をつうじて／〜をとおして", "explanation", "Doing or learning something via a means, person, or period of time",
  [("友人を通じて彼と知り合った。", "ゆうじんをつうじてかれとしりあった。", "I met him through a friend.")], GRAM7D4)
G("〜を通じて／〜を通して", "〜をつうじて／〜をとおして", "explanation", "Doing or learning something via a means, person, or period of time",
  [("テレビのニュースを通じてその事件を知った。", "テレビのニュースをつうじてそのじけんをしった。", "I knew about the incident through the news on television.")], GRAM7D4)
G("〜を通じて／〜を通して", "〜をつうじて／〜をとおして", "explanation", "Doing or learning something via a means, person, or period of time",
  [("ここでは一年を通じて美しい花が見られます。", "ここではいちねんをつうじてうつくしいはながみられます。", "You can see beautiful flowers all year round here.")], GRAM7D4)
G("〜を頼りに(して)", "〜をたよりに(して)", "explanation", "Using something or someone as a means of support",
  [("地図を頼りに、友達に教えてもらったレストランに行った。", "ちずをたよりに、ともだちにおしえてもらったレストランにいった。", "I went to the restaurant that my friend recommended to me with the help of a map.")], GRAM7D4)
G("〜を頼りに(して)", "〜をたよりに(して)", "explanation", "Using something or someone as a means of support",
  [("祖父はつえを頼りにして歩いている。", "そふはつえをたよりにしてあるいている。", "My grandfather walks with the help of a cane.")], GRAM7D4)

# --- Grammar Day 5: すばらしいものがある ---
GRAM7D5 = "grammar::w7 grammar::w7d5 jlpt::n2 type::grammar"
G("〜恐れがある", "〜おそれがある", "explanation", "Expresses concern that a negative event may occur",
  [("地震の際には、窓ガラスが割れたり壁が倒れたりする恐れがある。", "じしんのさいには、まどガラスがわれたりかべがたおれたりするおそれがある。", "In an event of an earthquake, there is a risk that the windows will break or that the walls will collapse.")], GRAM7D5)
G("〜恐れがある", "〜おそれがある", "explanation", "Expresses concern that a negative event may occur",
  [("台風19号は今夜、四国に上陸の恐れがあります。", "たいふう19ごうはこんや、しこくにじょうりくのおそれがあります。", "Typhoon no. 19 is threatening to make landfall on Shikoku tonight.")], GRAM7D5)
G("〜ものがある", "〜ものがある", "explanation", "There's a certain undeniable quality or feeling perceptible in something",
  [("満員電車で毎日通勤するのはつらいものがある。", "まんいんでんしゃでまいにちつうきんするのはつらいものがある。", "It is hard commuting on a packed train every day.")], GRAM7D5)
G("〜ものがある", "〜ものがある", "explanation", "There's a certain undeniable quality or feeling perceptible in something",
  [("彼の歌には心にひびくものがある。", "かれのうたにはこころにひびくものがある。", "His songs are very touching.")], GRAM7D5)
G("〜というものでもない／〜というものではない", "〜というものでもない／〜というものではない", "explanation", "Denies that a simple, blanket assumption always holds true",
  [("何でも多ければいいというものでもない。", "なんでもおおければいいというものでもない。", "Not everything is good in excess.")], GRAM7D5)
G("〜というものでもない／〜というものではない", "〜というものでもない／〜というものではない", "explanation", "Denies that a simple, blanket assumption always holds true",
  [("お金があれば幸せだというものでもない。", "おかねがあればしあわせだというものでもない。", "Just because you have money, it does not mean that you are happy.")], GRAM7D5)
G("〜（どうにか／なんとか／もう少し）〜ないものか", "〜（どうにか／なんとか／もう少し）〜ないものか", "explanation", "Expressing a wish that a difficult situation could somehow be resolved",
  [("最近、変なメールがたくさん来る。どうにかならないものか。", "さいきん、へんなメールがたくさんくる。どうにかならないものか。", "I get a lot of weird e-mails these days. I wish I could do something about it.")], GRAM7D5)
G("〜（どうにか／なんとか／もう少し）〜ないものか", "〜（どうにか／なんとか／もう少し）〜ないものか", "explanation", "Expressing a wish that a difficult situation could somehow be resolved",
  [("デジカメが壊れた。なんとか直らないものだろうか。", "デジカメがこわれた。なんとかなおらないものだろうか。", "My digital camera is not working. I wish I knew how to fix the problem.")], GRAM7D5)

# --- Grammar Day 6: 失敗をもとに ---
GRAM7D6 = "grammar::w7 grammar::w7d6 jlpt::n2 type::grammar"
G("〜をもとに(して)", "〜をもとに(して)", "explanation", "Using something as a foundation or basis for a subsequent action",
  [("この小説は事実をもとに書かれた。", "このしょうせつはじじつをもとにかかれた。", "This novel is based on fact.")], GRAM7D6)
G("〜をもとに(して)", "〜をもとに(して)", "explanation", "Using something as a foundation or basis for a subsequent action",
  [("失敗をもとにして発明する。", "しっぱいをもとにしてはつめいする。", "An invention results from failure.")], GRAM7D6)
G("〜につき", "〜につき", "explanation", "Formal expression giving a reason, often seen in writing or official notices",
  [("この機械はただ今調整中につき、ご使用になれません。", "このきかいはただいまちょうせいちゅうにつき、ごしようになれません。", "This machine is currently unavailable due to maintenance.")], GRAM7D6)
G("〜につき", "〜につき", "explanation", "Formal expression giving a reason, often seen in writing or official notices",
  [("本日は祭日につき、休業させていただきます。", "ほんじつはさいじつにつき、きゅうぎょうさせていただきます。", "Due to the holiday, we are closed today.")], GRAM7D6)
G("〜をきっかけに(して)／〜を契機に(として)", "〜をきっかけに(して)／〜をけいきに(として)", "explanation", "An event serves as the trigger or opportunity for a subsequent change",
  [("大学入学をきっかけに引っ越す。", "だいがくにゅうがくをきっかけにひっこす。", "Because I'll be going to university, I will move.")], GRAM7D6)
G("〜をきっかけに(して)／〜を契機に(として)", "〜をきっかけに(して)／〜をけいきに(として)", "explanation", "An event serves as the trigger or opportunity for a subsequent change",
  [("病気をきっかけに酒をやめた。", "びょうきをきっかけにさけをやめた。", "As a result of an illness, I stopped drinking.")], GRAM7D6)
G("〜をきっかけに(して)／〜を契機に(として)", "〜をきっかけに(して)／〜をけいきに(として)", "explanation", "An event serves as the trigger or opportunity for a subsequent change",
  [("卒業を契機に独立する。", "そつぎょうをけいきにどくりつする。", "I'll take the opportunity of graduating from university to become independent.")], GRAM7D6)
G("〜をきっかけに(して)／〜を契機に(として)", "〜をきっかけに(して)／〜をけいきに(として)", "explanation", "An event serves as the trigger or opportunity for a subsequent change",
  [("昨年の事故を契機として、安全対策が強化された。", "さくねんのじこをけいきとして、あんぜんたいさくがきょうかされた。", "As a result of last year's accident, safety measures were strengthened.")], GRAM7D6)
G("〜の際に／〜際", "〜のさいに／〜さい", "explanation", "A formal way of saying \"when\" or \"on the occasion of\"",
  [("受験の際に、写真が必要です。", "じゅけんのさいに、しゃしんがひつようです。", "A photo is required when you come to take the examination.")], GRAM7D6)
G("〜の際に／〜際", "〜のさいに／〜さい", "explanation", "A formal way of saying \"when\" or \"on the occasion of\"",
  [("申し込んだ際、住所を間違って書いてしまった。", "もうしこんださい、じゅうしょをまちがってかいてしまった。", "I wrote a wrong address when I applied.")], GRAM7D6)

# --- Grammar Bonus: 敬語 (Keigo) — お願いする ---
GRAM7DE = "grammar::w7 grammar::w7dExtra jlpt::n2 type::keigo"
G("お越しください／おいでください", "おこしください／おいでください", "explanation", "Keigo for 来てください (please come)",
  [("受付までお越しください。", "うけつけまでおこしください。", "Please come to the reception desk."),
   ("受付まで来てください。", "うけつけまできてください。", "Please come to the reception desk.")], GRAM7DE)
G("ご意見承りたく、お願い申し上げます", "ごいけんうけたまわりたく、おねがいもうしあげます", "explanation", "Keigo for 意見を聞きたいので、お願いします (I'd like to hear your opinion, so please)",
  [("ご多忙のところ恐縮ですが、ご意見承りたく、お願い申し上げます。", "ごたぼうのところきょうしゅくですが、ごいけんうけたまわりたく、おねがいもうしあげます。", "I know you're busy, but I would be grateful to hear your opinion."),
   ("忙しいところ悪いけど、意見を聞きたいから、お願い。", "いそがしいところわるいけど、いけんをききたいから、おねがい。", "Sorry to bother you when you're busy, but I'd like to hear your opinion, so please.")], GRAM7DE)

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
        "# Week 7 (Sou Matome N2) — Japanese vocabulary: Kanji/Vocabulary words",
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
        "# Week 7 (Sou Matome N2) — Japanese grammar and usage: Grammar patterns",
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

    with open(os.path.join(base, "week7-v3-vocabulary.tsv"), "w", encoding="utf-8") as f:
        f.write(vocab_tsv)
    with open(os.path.join(base, "week7-v3-grammar-usage.tsv"), "w", encoding="utf-8") as f:
        f.write(grammar_tsv)
    print("Wrote TSVs.")

    if not errs:
        model1 = make_model(MODEL1_ID, "Japanese vocabulary")
        model2 = make_model(MODEL2_ID, "Japanese grammar and usage")
        n1 = build_apkg(vocab_tsv, DECK1_ID, "Japanese N2 Vocabulary", model1,
                         os.path.join(base, "week7-v3-vocabulary.apkg"))
        n2 = build_apkg(grammar_tsv, DECK2_ID, "Japanese N2 Grammar & Usage", model2,
                         os.path.join(base, "week7-v3-grammar-usage.apkg"))
        print(f"Wrote apkg: vocabulary={n1} notes, grammar-usage={n2} notes")
