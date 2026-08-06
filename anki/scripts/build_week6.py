#!/usr/bin/env python3
"""Build Week 6 Anki TSV/apkg files (Deck 1 Vocabulary, Deck 2 Grammar & Usage).

Follows specs/anki-tsv-generation-process.md, specs/anki-note-type-vocabulary.md,
specs/anki-note-type-grammar-and-usage.md. Run from repo root:

    .venv/bin/python anki/scripts/build_week6.py

Note: Week 6 has no listening-w6.md (the source listening book doesn't extend past
Chapter 5 / Week 5), so this week's decks are built from Kanji + Vocabulary + Grammar +
Reading only. That's an expected, checked outcome, not a missed extraction.
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

# --- Kanji Day 1: 広告・チラシ ---
K6D1 = "kanji::w6 kanji::w6d1 jlpt::n2"
V("得", "とく", "A profit/benefit", "早めに予約すると得です。", "はやめによやくするととくです。", "It's a benefit to reserve early.", K6D1)
V("得る", "える", "Obtain", "この仕事で貴重な経験を得た。", "このしごとできちょうなけいけんをえた。", "I gained valuable experience from this job.", K6D1)
V("納得", "なっとく", "Assent/understanding", "彼の説明を聞いて納得した。", "かれのせつめいをきいてなっとくした。", "I was convinced after hearing his explanation.", K6D1)
V("心得る", "こころえる", "Understand/be well aware of", "彼はマナーを心得ている。", "かれはマナーをこころえている。", "He is well versed in manners.", K6D1)
V("広告", "こうこく", "An advertisement", "新聞に広告を出した。", "しんぶんにこうこくをだした。", "I placed an ad in the newspaper.", K6D1)
V("警告", "けいこく", "Warning/caution", "医師から警告を受けた。", "いしからけいこくをうけた。", "I received a warning from the doctor.", K6D1)
V("告げる", "つげる", "Inform", "彼女に別れを告げた。", "かのじょにわかれをつげた。", "I told her it was over.", K6D1)
V("税金", "ぜいきん", "A tax", "毎年、税金を納める。", "まいとし、ぜいきんをおさめる。", "I pay taxes every year.", K6D1)
V("消費税", "しょうひぜい", "A consumption tax", "消費税が上がった。", "しょうひぜいがあがった。", "The consumption tax went up.", K6D1)
V("税関", "ぜいかん", "Customs", "空港の税関で荷物を調べられた。", "くうこうのぜいかんでにもつをしらべられた。", "My luggage was inspected at customs at the airport.", K6D1)
V("課税", "かぜい", "Taxation", "高額商品には課税される。", "こうがくしょうひんにはかぜいされる。", "High-value goods are taxed.", K6D1)
V("定価", "ていか", "A fixed price", "この本の定価は2000円だ。", "このほんのていかは2000えんだ。", "The list price of this book is 2000 yen.", K6D1)
V("物価", "ぶっか", "Price/cost of living", "東京は物価が高い。", "とうきょうはぶっかがたかい。", "The cost of living in Tokyo is high.", K6D1)
V("価格", "かかく", "A price", "商品の価格を比較した。", "しょうひんのかかくをひかくした。", "I compared the prices of the products.", K6D1)
V("性格", "せいかく", "Character/personality", "彼女は明るい性格だ。", "かのじょはあかるいせいかくだ。", "She has a cheerful personality.", K6D1)
V("超える", "こえる", "Get over/exceed", "参加者は千人を超えた。", "さんかしゃはせんにんをこえた。", "The number of participants exceeded a thousand.", K6D1)
V("超過", "ちょうか", "Excess/surplus", "荷物の重量が超過した。", "にもつのじゅうりょうがちょうかした。", "The luggage weight was over the limit.", K6D1)
V("超す", "こす", "Cross/pass/exceed", "気温が30度を超した。", "きおんが30どをこした。", "The temperature exceeded 30 degrees.", K6D1)
V("平均", "へいきん", "An average", "平均年齢を調べた。", "へいきんねんれいをしらべた。", "I checked the average age.", K6D1)
V("均一", "きんいつ", "Uniformity", "この店は均一価格だ。", "このみせはきんいつかかくだ。", "This store has uniform pricing.", K6D1)
V("靴", "くつ", "Shoes", "新しい靴を買った。", "あたらしいくつをかった。", "I bought new shoes.", K6D1)
V("長靴", "ながぐつ", "Boots", "雨の日は長靴をはく。", "あめのひはながぐつをはく。", "I wear boots on rainy days.", K6D1)
V("靴下", "くつした", "Socks", "厚い靴下をはいた。", "あついくつしたをはいた。", "I wore thick socks.", K6D1)
V("雨靴", "あまぐつ", "Rain shoes", "雨靴を玄関に置いた。", "あまぐつをげんかんにおいた。", "I put the rain shoes by the entrance.", K6D1)
V("提供", "ていきょう", "An offer/a tender", "情報の提供をお願いします。", "じょうほうのていきょうをおねがいします。", "Please provide information.", K6D1)
V("子供", "こども", "A child", "公園で子供が遊んでいる。", "こうえんでこどもがあそんでいる。", "Children are playing in the park.", K6D1)
V("印象", "いんしょう", "An impression", "彼はいい印象を与えた。", "かれはいいいんしょうをあたえた。", "He made a good impression.", K6D1)
V("対象", "たいしょう", "Object (e.g. of study)", "この調査は学生を対象にしている。", "このちょうさはがくせいをたいしょうにしている。", "This survey targets students.", K6D1)
V("現象", "げんしょう", "A phenomenon", "これは珍しい自然現象だ。", "これはめずらしいしぜんげんしょうだ。", "This is a rare natural phenomenon.", K6D1)
V("象", "ぞう", "An elephant", "動物園で象を見た。", "どうぶつえんでぞうをみた。", "I saw an elephant at the zoo.", K6D1)
V("組織", "そしき", "An organization", "新しい組織を作った。", "あたらしいそしきをつくった。", "We created a new organization.", K6D1)
V("組み合わせ", "くみあわせ", "A combination", "試合の組み合わせが決まった。", "しあいのくみあわせがきまった。", "The match pairings were decided.", K6D1)
V("番組", "ばんぐみ", "A TV program", "好きなテレビ番組を見た。", "すきなテレビばんぐみをみた。", "I watched my favorite TV program.", K6D1)
V("組合", "くみあい", "An association", "労働組合に加入している。", "ろうどうくみあいにかにゅうしている。", "I belong to a labor union.", K6D1)
V("価値", "かち", "Value/worth", "この絵には歴史的な価値がある。", "このえにはれきしてきなかちがある。", "This painting has historical value.", K6D1)
V("値段", "ねだん", "A price", "この靴の値段を聞いた。", "このくつのねだんをきいた。", "I asked the price of these shoes.", K6D1)
V("数値", "すうち", "A numerical value", "検査の数値が正常だった。", "けんさのすうちがせいじょうだった。", "The test values were normal.", K6D1)
V("値", "ね", "Value/price", "この土地は値が上がっている。", "このとちはねがあがっている。", "The price of this land is rising.", K6D1)
V("募集", "ぼしゅう", "Recruitment", "新入社員を募集している。", "しんにゅうしゃいんをぼしゅうしている。", "We are recruiting new employees.", K6D1)
V("募金", "ぼきん", "Fund-raising (money)", "災害のための募金に協力した。", "さいがいのためのぼきんにきょうりょくした。", "I contributed to fundraising for the disaster relief.", K6D1)
V("応募", "おうぼ", "An application", "コンテストに応募した。", "コンテストにおうぼした。", "I applied for the contest.", K6D1)
V("募る", "つのる", "Collect/raise (money), recruit", "ボランティアを募っている。", "ボランティアをつのっている。", "We are recruiting volunteers.", K6D1)
V("無料", "むりょう", "No charge", "この駐車場は無料だ。", "このちゅうしゃじょうはむりょうだ。", "This parking lot is free.", K6D1)
V("無事", "ぶじ", "Unharmed/safe", "全員が無事に帰ってきた。", "ぜんいんがぶじにかえってきた。", "Everyone returned safely.", K6D1)
V("有無", "うむ", "Existence or nonexistence", "経験の有無は問いません。", "けいけんのうむはといません。", "It doesn't matter whether you have experience or not.", K6D1)

# --- Kanji Day 2: 折り込み広告 ---
# 小麦粉 (already carded week5 kanji d5), 承る (already carded week4 grammar keigo), and
# 展示 (near-duplicate of already-carded week5 展示する) skipped as cross-week duplicates.
K6D2 = "kanji::w6 kanji::w6d2 jlpt::n2"
V("詰める", "つめる", "Stuff/cram/pack", "スーツケースに服を詰めた。", "スーツケースにふくをつめた。", "I packed clothes into the suitcase.", K6D2)
V("箱詰め", "はこづめ", "Food etc. in a box", "クッキーを箱詰めにして贈った。", "クッキーをはこづめにしておくった。", "I boxed up cookies and gave them as a gift.", K6D2)
V("缶詰", "かんづめ", "Food etc. in a can", "非常用に缶詰を買っておいた。", "ひじょうようにかんづめをかっておいた。", "I bought canned food for emergencies.", K6D2)
V("麦畑", "むぎばたけ", "A wheat field", "麦畑が黄色く色づいている。", "むぎばたけがきいろくいろづいている。", "The wheat field has turned golden yellow.", K6D2)
V("純粋", "じゅんすいな", "Pure", "彼は純粋な気持ちで謝った。", "かれはじゅんすいなきもちであやまった。", "He apologized with a pure heart.", K6D2)
V("純情", "じゅんじょうな", "Naive/a pure heart", "彼女は純情な少女だった。", "かのじょはじゅんじょうなしょうじょだった。", "She was a naive, pure-hearted girl.", K6D2)
V("単純", "たんじゅんな", "Simple/simple-minded", "この問題は単純ではない。", "このもんだいはたんじゅんではない。", "This problem isn't simple.", K6D2)
V("純米酢", "じゅんまいす", "Pure rice vinegar", "料理に純米酢を使う。", "りょうりにじゅんまいすをつかう。", "I use pure rice vinegar in cooking.", K6D2)
V("雑草", "ざっそう", "Weed", "庭の雑草を抜いた。", "にわのざっそうをぬいた。", "I pulled the weeds in the garden.", K6D2)
V("除草", "じょそう", "Weeding", "毎週末、除草作業をする。", "まいしゅうまつ、じょそうさぎょうをする。", "I do weeding work every weekend.", K6D2)
V("草", "くさ", "Grass", "牛が草を食べている。", "うしがくさをたべている。", "Cows are eating grass.", K6D2)
V("草花", "くさばな", "A flowering plant", "庭に草花を植えた。", "にわにくさばなをうえた。", "I planted flowering plants in the garden.", K6D2)
V("食塩", "しょくえん", "Table salt", "食塩の取りすぎに注意する。", "しょくえんのとりすぎにちゅういする。", "I'm careful not to consume too much table salt.", K6D2)
V("塩", "しお", "Salt", "スープに塩を入れた。", "スープにしおをいれた。", "I added salt to the soup.", K6D2)
V("固定", "こてい", "Stability/fixation", "棚を壁に固定した。", "たなをかべにこていした。", "I fixed the shelf to the wall.", K6D2)
V("固形", "こけい", "Solid (form)", "固形の燃料を使う。", "こけいのねんりょうをつかう。", "I use solid fuel.", K6D2)
V("固体", "こたい", "Solid (body)", "氷は水の固体の状態だ。", "こおりはみずのこたいのじょうたいだ。", "Ice is the solid state of water.", K6D2)
V("固い", "かたい", "Hard", "このパンは固い。", "このパンはかたい。", "This bread is hard.", K6D2)
V("固まる", "かたまる", "Harden", "セメントが固まった。", "セメントがかたまった。", "The cement hardened.", K6D2)
V("実演", "じつえん", "A demonstration", "店員が使い方を実演した。", "てんいんがつかいかたをじつえんした。", "The clerk demonstrated how to use it.", K6D2)
V("演習", "えんしゅう", "Exercises/maneuvers", "消防の演習に参加した。", "しょうぼうのえんしゅうにさんかした。", "I participated in a fire drill.", K6D2)
V("演技", "えんぎ", "Acting/performance", "彼女の演技は素晴らしかった。", "かのじょのえんぎはすばらしかった。", "Her acting was wonderful.", K6D2)
V("演説", "えんぜつ", "A speech/oration", "候補者が駅前で演説した。", "こうほしゃがえきまえでえんぜつした。", "The candidate gave a speech in front of the station.", K6D2)
V("菓子", "かし", "Sweets/point", "子どもにお菓子をあげた。", "こどもにおかしをあげた。", "I gave sweets to the child.", K6D2)
V("和菓子", "わがし", "Japanese sweets", "お茶と一緒に和菓子を食べた。", "おちゃといっしょにわがしをたべた。", "I ate Japanese sweets with tea.", K6D2)
V("洋菓子", "ようがし", "Western sweets", "洋菓子店でケーキを買った。", "ようがしてんでケーキをかった。", "I bought a cake at a Western-style confectionery.", K6D2)
V("贈り物", "おくりもの", "A gift", "友人に贈り物をした。", "ゆうじんにおくりものをした。", "I gave a gift to my friend.", K6D2)
V("贈る", "おくる", "Present/give", "卒業生に花束を贈った。", "そつぎょうせいにはなたばをおくった。", "I presented a bouquet to the graduate.", K6D2)
V("帰省", "きせい", "Homecoming", "お盆に帰省する予定だ。", "おぼんにきせいするよていだ。", "I plan to go back to my hometown for Obon.", K6D2)
V("省く", "はぶく", "Delete/omit", "説明を省いて要点だけ話した。", "せつめいをはぶいてようてんだけはなした。", "I omitted the explanation and just spoke the main points.", K6D2)
V("反省", "はんせい", "Self-examination", "自分の行動を反省した。", "じぶんのこうどうをはんせいした。", "I reflected on my own behavior.", K6D2)
V("省エネ", "しょうえね", "Energy saving", "省エネのため電気を消した。", "しょうえねのためでんきをけした。", "I turned off the lights to save energy.", K6D2)
V("省略", "しょうりゃく", "An abbreviation/omission", "詳しい説明は省略します。", "くわしいせつめいはしょうりゃくします。", "I will omit the detailed explanation.", K6D2)
V("了承", "りょうしょう", "Consent/approval", "計画の変更を了承した。", "けいかくのへんこうをりょうしょうした。", "I agreed to the change of plan.", K6D2)
V("承知", "しょうち", "Knowledge/consent", "その件については承知しております。", "そのけんについてはしょうちしております。", "I am aware of that matter.", K6D2)
V("承認", "しょうにん", "Approval/confirmation", "新しい規則が承認された。", "あたらしいきそくがしょうにんされた。", "The new rule was approved.", K6D2)
V("展覧会", "てんらんかい", "An exhibition", "絵画の展覧会を見に行った。", "かいがのてんらんかいをみにいった。", "I went to see a painting exhibition.", K6D2)
V("発展", "はってん", "Development", "この町は急速に発展した。", "このまちはきゅうそくにはってんした。", "This town developed rapidly.", K6D2)
V("破格", "はかく", "Exceptional", "破格の値段で売られている。", "はかくのねだんでうられている。", "It's being sold at an exceptionally low price.", K6D2)
V("破片", "はへん", "A fragment", "ガラスの破片が散らばっていた。", "ガラスのはへんがちらばっていた。", "Glass fragments were scattered around.", K6D2)
V("破れる", "やぶれる", "Break/rip", "紙が破れてしまった。", "かみがやぶれてしまった。", "The paper got torn.", K6D2)
V("破産", "はさん", "Bankruptcy", "会社が破産した。", "かいしゃがはさんした。", "The company went bankrupt.", K6D2)
V("破る", "やぶる", "Break/rip/violate (something)", "世界記録を破った。", "せかいきろくをやぶった。", "He broke the world record.", K6D2)
V("処理", "しょり", "Disposal/processing", "データの処理に時間がかかる。", "データのしょりにじかんがかかる。", "Data processing takes time.", K6D2)
V("処分", "しょぶん", "Disposal/punishment", "古い家具を処分した。", "ふるいかぐをしょぶんした。", "I disposed of old furniture.", K6D2)
V("処置", "しょち", "Management/measure", "事故現場で応急処置をした。", "じこげんばでおうきゅうしょちをした。", "First aid was given at the accident scene.", K6D2)

# --- Kanji Day 3: 広告 (hotel/travel) ---
K6D3 = "kanji::w6 kanji::w6d3 jlpt::n2"
V("温泉", "おんせん", "A hot spring", "週末は温泉に行ってゆっくりした。", "しゅうまつはおんせんにいってゆっくりした。", "I went to a hot spring and relaxed over the weekend.", K6D3)
V("泉", "いずみ", "A spring", "山の中に泉を見つけた。", "やまのなかにいずみをみつけた。", "I found a spring in the mountains.", K6D3)
V("宿題", "しゅくだい", "Homework", "今日中に宿題を終わらせる。", "きょうじゅうにしゅくだいをおわらせる。", "I'll finish my homework today.", K6D3)
V("宿", "やど", "An inn", "温泉地でいい宿を見つけた。", "おんせんちでいいやどをみつけた。", "I found a good inn at the hot spring resort.", K6D3)
V("下宿", "げしゅく", "Lodgings", "大学時代は下宿していた。", "だいがくじだいはげしゅくしていた。", "During university, I lived in a boarding house.", K6D3)
V("季節", "きせつ", "A season", "日本には四つの季節がある。", "にほんにはよっつのきせつがある。", "Japan has four seasons.", K6D3)
V("四季", "しき", "Four seasons", "日本の四季は美しい。", "にほんのしきはうつくしい。", "Japan's four seasons are beautiful.", K6D3)
V("冬季", "とうき", "The winter season", "冬季オリンピックを見た。", "とうきオリンピックをみた。", "I watched the Winter Olympics.", K6D3)
V("豊作", "ほうさく", "A bumper crop", "今年は米が豊作だ。", "ことしはこめがほうさくだ。", "This year's rice harvest is bountiful.", K6D3)
V("豊か", "ゆたかな", "Wealthy/abundant", "この町は自然が豊かだ。", "このまちはしぜんがゆたかだ。", "This town is rich in nature.", K6D3)
V("豊富", "ほうふな", "Abundant", "この店は品揃えが豊富だ。", "このみせはしなぞろえがほうふだ。", "This store has an abundant selection.", K6D3)
V("富士山", "ふじさん", "Mount Fuji", "富士山に登ったことがある。", "ふじさんにのぼったことがある。", "I've climbed Mt. Fuji.", K6D3)
V("富む", "とむ", "Be wealthy/abundant", "彼のアイデアは独創性に富んでいる。", "かれのアイデアはどくそうせいにとんでいる。", "His ideas are rich in originality.", K6D3)
V("送迎", "そうげい", "A pickup service", "ホテルの送迎バスを利用した。", "ホテルのそうげいバスをりようした。", "I used the hotel's shuttle bus.", K6D3)
V("迎える", "むかえる", "Meet/welcome", "空港で友人を迎えた。", "くうこうでゆうじんをむかえた。", "I met my friend at the airport.", K6D3)
V("歓迎", "かんげい", "A welcome", "新入生を歓迎するパーティーを開いた。", "しんにゅうせいをかんげいするパーティーをひらいた。", "We held a party to welcome the new students.", K6D3)
V("出迎え", "でむかえ", "Going to meet someone", "駅まで出迎えに行った。", "えきまででむかえにいった。", "I went to meet them at the station.", K6D3)
V("泊まる", "とまる", "Stay", "友人の家に泊まった。", "ゆうじんのいえにとまった。", "I stayed over at my friend's house.", K6D3)
V("宿泊", "しゅくはく", "Lodging", "ホテルに宿泊した。", "ホテルにしゅくはくした。", "I stayed at a hotel.", K6D3)

# --- Kanji Day 4: 地図 ---
# 居眠り (week3 vocab), 築〜年 (week4 listening), 列島 (week5 kanji), 警察 (week4 listening)
# skipped as cross-week duplicates. 美術 skipped as a within-day duplicate (美 vs 術 groups).
K6D4 = "kanji::w6 kanji::w6d4 jlpt::n2"
V("入居", "にゅうきょ", "Moving into (e.g. an apartment)", "来月、新しいアパートに入居する。", "らいげつ、あたらしいアパートににゅうきょする。", "I'll move into a new apartment next month.", K6D4)
V("居間", "いま", "A living room", "家族で居間でくつろいだ。", "かぞくでいまでくつろいだ。", "The family relaxed in the living room.", K6D4)
V("居る", "いる", "Be (in a place)/exist", "兄は今、家に居る。", "あにはいま、いえにいる。", "My older brother is home right now.", K6D4)
V("建築", "けんちく", "Architecture", "大学で建築を学んでいる。", "だいがくでけんちくをまなんでいる。", "I'm studying architecture at university.", K6D4)
V("三角", "さんかく", "A triangle", "三角の形の旗を作った。", "さんかくのかたちのはたをつくった。", "I made a triangle-shaped flag.", K6D4)
V("角度", "かくど", "An angle", "様々な角度から検討した。", "さまざまなかくどからけんとうした。", "We considered it from various angles.", K6D4)
V("方角", "ほうがく", "Direction/way", "方角がわからなくなった。", "ほうがくがわからなくなった。", "I lost track of which direction I was facing.", K6D4)
V("角", "かど", "A corner", "その角を右に曲がってください。", "そのかどをみぎにまがってください。", "Please turn right at that corner.", K6D4)
V("生徒", "せいと", "A student", "この学校には生徒が500人いる。", "このがっこうにはせいとが500にんいる。", "This school has 500 students.", K6D4)
V("徒歩", "とほ", "Going on foot", "駅から徒歩5分です。", "えきからとほ5ふんです。", "It's a 5-minute walk from the station.", K6D4)
V("畳", "たたみ", "Tatami (Japanese straw mat)", "和室には畳が敷いてある。", "わしつにはたたみがしいてある。", "Tatami mats are laid in the Japanese-style room.", K6D4)
V("畳む", "たたむ", "Fold", "洗濯物をきれいに畳んだ。", "せんたくものをきれいにたたんだ。", "I folded the laundry neatly.", K6D4)
V("欧米", "おうべい", "Europe and America/the West", "欧米の文化に興味がある。", "おうべいのぶんかにきょうみがある。", "I'm interested in Western culture.", K6D4)
V("新米", "しんまい", "New rice/new face", "彼はまだ新米の社員だ。", "かれはまだしんまいのしゃいんだ。", "He's still a new/inexperienced employee.", K6D4)
V("平米", "へいべい", "Square meters", "この部屋は50平米ある。", "このへやは50へいべいある。", "This room is 50 square meters.", K6D4)
V("米", "こめ", "Rice", "日本人は米をよく食べる。", "にほんじんはこめをよくたべる。", "Japanese people eat a lot of rice.", K6D4)
V("解説", "かいせつ", "An explanation", "専門家がニュースを解説した。", "せんもんかがニュースをかいせつした。", "An expert explained the news.", K6D4)
V("解放", "かいほう", "A release", "人質が解放された。", "ひとじちがかいほうされた。", "The hostage was released.", K6D4)
V("解約", "かいやく", "A cancellation (of a contract)", "携帯電話の契約を解約した。", "けいたいでんわのけいやくをかいやくした。", "I cancelled my phone contract.", K6D4)
V("解決", "かいけつ", "A solution", "問題が無事に解決した。", "もんだいがぶじにかいけつした。", "The problem was successfully resolved.", K6D4)
V("解散", "かいさん", "Dissolution", "会議は3時に解散した。", "かいぎは3じにかいさんした。", "The meeting broke up at 3 o'clock.", K6D4)
V("解く", "とく", "Solve/untie", "難しい数学の問題を解いた。", "むずかしいすうがくのもんだいをといた。", "I solved a difficult math problem.", K6D4)
V("この辺", "このへん", "Around here", "この辺にコンビニはありますか。", "このへんにコンビニはありますか。", "Is there a convenience store around here?", K6D4)
V("辺り", "あたり", "Around", "辺りは静かだった。", "あたりはしずかだった。", "The area around was quiet.", K6D4)
V("周辺", "しゅうへん", "Vicinity", "駅の周辺にお店が多い。", "えきのしゅうへんにおみせがおおい。", "There are many shops around the station.", K6D4)
V("海辺", "うみべ", "A beach", "海辺を散歩した。", "うみべをさんぽした。", "I took a walk along the beach.", K6D4)
V("診察", "しんさつ", "A medical consultation", "病院で診察を受けた。", "びょういんでしんさつをうけた。", "I had a medical checkup at the hospital.", K6D4)
V("役所", "やくしょ", "A government office", "役所に書類を提出した。", "やくしょにしょるいをていしゅつした。", "I submitted documents to the government office.", K6D4)
V("役者", "やくしゃ", "An actor", "彼は有名な役者だ。", "かれはゆうめいなやくしゃだ。", "He is a famous actor.", K6D4)
V("役目", "やくめ", "A role/duty", "司会の役目を任された。", "しかいのやくめをまかされた。", "I was entrusted with the role of MC.", K6D4)
V("現役", "げんえき", "Active service", "彼は現役の選手だ。", "かれはげんえきのせんしゅだ。", "He is an active player.", K6D4)
V("美人", "びじん", "A beautiful woman", "彼女は近所で有名な美人だ。", "かのじょはきんじょでゆうめいなびじんだ。", "She's known as the beauty in the neighborhood.", K6D4)
V("美しい", "うつくしい", "Beautiful", "夕焼けがとても美しかった。", "ゆうやけがとてもうつくしかった。", "The sunset was very beautiful.", K6D4)
V("美容", "びよう", "Beauty treatment", "美容のために野菜をたくさん食べる。", "びようのためにやさいをたくさんたべる。", "I eat a lot of vegetables for beauty's sake.", K6D4)
V("手術", "しゅじゅつ", "Surgery/operation", "母は先週手術を受けた。", "はははせんしゅうしゅじゅつをうけた。", "My mother had surgery last week.", K6D4)
V("技術", "ぎじゅつ", "Technique/technology", "日本の技術は世界的に有名だ。", "にほんのぎじゅつはせかいてきにゆうめいだ。", "Japanese technology is world-famous.", K6D4)
V("芸術", "げいじゅつ", "Art", "彼は芸術に深い関心を持っている。", "かれはげいじゅつにふかいかんしんをもっている。", "He has a deep interest in art.", K6D4)
V("坂", "さか", "Hill/slope", "この坂を上ると学校がある。", "このさかをのぼるとがっこうがある。", "The school is up this hill.", K6D4)
V("寺", "てら", "A temple", "京都には古い寺がたくさんある。", "きょうとにはふるいてらがたくさんある。", "There are many old temples in Kyoto.", K6D4)
V("寺院", "じいん", "A temple/an abbey", "その寺院は国宝に指定されている。", "そのじいんはこくほうにしていされている。", "That temple is designated a national treasure.", K6D4)
V("湾", "わん", "A bay", "船は湾の中に停泊している。", "ふねはわんのなかにていはくしている。", "The ship is anchored in the bay.", K6D4)
V("島", "しま", "An island", "小さな島に旅行に行った。", "ちいさなしまにりょこうにいった。", "I went on a trip to a small island.", K6D4)
V("海岸", "かいがん", "A seashore", "海岸を散歩した。", "かいがんをさんぽした。", "I walked along the coast.", K6D4)
V("岸", "きし", "A shore/bank", "船が岸に着いた。", "ふねがきしについた。", "The boat arrived at the shore.", K6D4)
V("湾岸", "わんがん", "A gulf/the coast along a bay", "湾岸沿いに道路がある。", "わんがんぞいにどうろがある。", "There's a road along the bay coast.", K6D4)
V("川岸", "かわぎし", "A riverbank", "川岸で釣りをした。", "かわぎしでつりをした。", "I fished on the riverbank.", K6D4)
V("公園", "こうえん", "A park", "公園で子どもたちが遊んでいる。", "こうえんでこどもたちがあそんでいる。", "Children are playing in the park.", K6D4)
V("遊園地", "ゆうえんち", "An amusement park", "週末に遊園地に行った。", "しゅうまつにゆうえんちにいった。", "I went to an amusement park on the weekend.", K6D4)
V("動物園", "どうぶつえん", "A zoo", "動物園でパンダを見た。", "どうぶつえんでパンダをみた。", "I saw a panda at the zoo.", K6D4)
V("湖", "みずうみ", "A lake", "湖のほとりでキャンプをした。", "みずうみのほとりでキャンプをした。", "I camped by the lake.", K6D4)
V("城", "しろ", "A castle", "この城は500年前に建てられた。", "このしろは500ねんまえにたてられた。", "This castle was built 500 years ago.", K6D4)
V("渓谷", "けいこく", "A gorge/ravine", "美しい渓谷を訪れた。", "うつくしいけいこくをおとずれた。", "I visited a beautiful gorge.", K6D4)
V("谷間", "たにま", "A valley/ravine", "谷間に村がある。", "たにまにむらがある。", "There's a village in the valley.", K6D4)
V("谷", "たに", "A valley", "谷を越えて山道を進んだ。", "たにをこえてやまみちをすすんだ。", "I crossed the valley and continued on the mountain path.", K6D4)
V("谷川", "たにがわ", "A mountain stream", "谷川の水はとても冷たかった。", "たにがわのみずはとてもつめたかった。", "The mountain stream's water was very cold.", K6D4)

# --- Kanji Day 5: 文化財・展示 ---
# 省略 (already carded Day 2, under 省) and 芸術 (already carded Day 4, under 術) skipped as
# within-week duplicates.
K6D5 = "kanji::w6 kanji::w6d5 jlpt::n2"
V("財産", "ざいさん", "Property/fortune", "祖父から財産を相続した。", "そふからざいさんをそうぞくした。", "I inherited property from my grandfather.", K6D5)
V("財布", "さいふ", "A wallet/purse", "財布を落としてしまった。", "さいふをおとしてしまった。", "I lost my wallet.", K6D5)
V("文化財", "ぶんかざい", "Cultural property", "この寺は重要文化財に指定されている。", "このてらはじゅうようぶんかざいにしていされている。", "This temple is designated an important cultural property.", K6D5)
V("観光", "かんこう", "Sightseeing", "京都を観光した。", "きょうとをかんこうした。", "I went sightseeing in Kyoto.", K6D5)
V("観察", "かんさつ", "Observation", "昆虫の観察をした。", "こんちゅうのかんさつをした。", "I observed insects.", K6D5)
V("観客", "かんきゃく", "A spectator/audience", "観客が満員だった。", "かんきゃくがまんいんだった。", "The audience filled the venue.", K6D5)
V("観音", "かんのん", "Kannon/the Buddhist Deity of Mercy", "観音像を拝んだ。", "かんのんぞうをおがんだ。", "I prayed to the statue of Kannon.", K6D5)
V("宝石", "ほうせき", "A jewel/gem", "誕生日に宝石をもらった。", "たんじょうびにほうせきをもらった。", "I received jewelry for my birthday.", K6D5)
V("国宝", "こくほう", "A national treasure", "この仏像は国宝だ。", "このぶつぞうはこくほうだ。", "This statue of Buddha is a national treasure.", K6D5)
V("宝物館", "ほうもつかん", "A museum of treasures", "神社の宝物館を見学した。", "じんじゃのほうもつかんをけんがくした。", "I toured the shrine's treasure museum.", K6D5)
V("宝物", "たからもの", "Treasure", "亡き祖母の指輪は私の宝物だ。", "なきそぼのゆびわはわたしのたからものだ。", "My late grandmother's ring is my treasure.", K6D5)
V("仏教", "ぶっきょう", "Buddhism", "仏教の歴史を学んでいる。", "ぶっきょうのれきしをまなんでいる。", "I'm studying the history of Buddhism.", K6D5)
V("仏", "ほとけ", "Buddha/deceased person", "亡くなった父はもう仏になった。", "なくなったちちはもうほとけになった。", "My deceased father has become a Buddha.", K6D5)
V("仏像", "ぶつぞう", "A statue of Buddha", "寺で古い仏像を見た。", "てらでふるいぶつぞうをみた。", "I saw an old Buddha statue at the temple.", K6D5)
V("日仏", "にちぶつ", "Japan and France", "日仏の文化交流が盛んだ。", "にちぶつのぶんかこうりゅうがさかんだ。", "Japan-France cultural exchange is thriving.", K6D5)
V("国王", "こくおう", "A king", "その国の国王が来日した。", "そのくにのこくおうがらいにちした。", "The king of that country visited Japan.", K6D5)
V("王女", "おうじょ", "A princess", "王女は美しいドレスを着ていた。", "おうじょはうつくしいドレスをきていた。", "The princess wore a beautiful dress.", K6D5)
V("王子", "おうじ", "A prince", "あの国には3人の王子がいる。", "あのくにには3にんのおうじがいる。", "That country has three princes.", K6D5)
V("女王", "じょおう", "A queen", "女王が国民に演説した。", "じょおうがこくみんにえんぜつした。", "The queen gave a speech to the people.", K6D5)
V("銅", "どう", "Copper/bronze", "このやかんは銅でできている。", "このやかんはどうでできている。", "This kettle is made of copper.", K6D5)
V("銅像", "どうぞう", "A bronze statue", "駅前に銅像が立っている。", "えきまえにどうぞうがたっている。", "A bronze statue stands in front of the station.", K6D5)
V("塔", "とう", "A tower/pagoda", "遠くに高い塔が見えた。", "とおくにたかいとうがみえた。", "I could see a tall tower in the distance.", K6D5)
V("五重の塔", "ごじゅうのとう", "A five-storied pagoda", "五重の塔を見に奈良へ行った。", "ごじゅうのとうをみにならへいった。", "I went to Nara to see the five-storied pagoda.", K6D5)
V("絵", "え", "A picture", "娘は絵を描くのが好きだ。", "むすめはえをかくのがすきだ。", "My daughter likes drawing pictures.", K6D5)
V("絵画", "かいが", "A painting", "美術館で絵画を鑑賞した。", "びじゅつかんでかいがをかんしょうした。", "I admired paintings at the art museum.", K6D5)
V("絵の具", "えのぐ", "Paints/colors", "絵の具で色を塗った。", "えのぐでいろをぬった。", "I painted with watercolors.", K6D5)
V("略す", "りゃくす", "Abbreviate", "長い名前を略して呼ぶ。", "ながいなまえをりゃくしてよぶ。", "I abbreviate the long name when calling it.", K6D5)
V("略歴", "りゃくれき", "A profile", "履歴書に略歴を書いた。", "りれきしょにりゃくれきをかいた。", "I wrote a brief profile on my resume.", K6D5)
V("順", "じゅん", "Order", "名前の順に並んだ。", "なまえのじゅんにならんだ。", "We lined up in order of name.", K6D5)
V("順番", "じゅんばん", "A turn/order", "順番を待っている。", "じゅんばんをまっている。", "I'm waiting for my turn.", K6D5)
V("順路", "じゅんろ", "A route", "美術館の順路に従って進んだ。", "びじゅつかんのじゅんろにしたがってすすんだ。", "I proceeded following the museum's designated route.", K6D5)
V("順調", "じゅんちょう", "Smooth/favorable", "仕事は順調に進んでいる。", "しごとはじゅんちょうにすすんでいる。", "Work is progressing smoothly.", K6D5)
V("出版", "しゅっぱん", "A publication", "新しい本を出版した。", "あたらしいほんをしゅっぱんした。", "I published a new book.", K6D5)
V("出版社", "しゅっぱんしゃ", "A publishing company", "出版社に原稿を送った。", "しゅっぱんしゃにげんこうをおくった。", "I sent the manuscript to the publisher.", K6D5)
V("版画", "はんが", "A print/an engraving", "版画の展示会を見に行った。", "はんがのてんじかいをみにいった。", "I went to see a print exhibition.", K6D5)
V("芸能", "げいのう", "Public entertainments", "芸能界のニュースを見た。", "げいのうかいのニュースをみた。", "I watched news from the entertainment world.", K6D5)
V("工芸", "こうげい", "Industrial arts", "日本の伝統工芸を学んだ。", "にほんのでんとうこうげいをまなんだ。", "I learned about traditional Japanese crafts.", K6D5)
V("園芸", "えんげい", "Gardening", "趣味は園芸です。", "しゅみはえんげいです。", "My hobby is gardening.", K6D5)
V("複製", "ふくせい", "A duplicate/replica", "有名な絵画の複製を部屋に飾った。", "ゆうめいなかいがのふくせいをへやにかざった。", "I displayed a replica of a famous painting in my room.", K6D5)
V("複写", "ふくしゃ", "A duplicate/copy", "書類を複写した。", "しょるいをふくしゃした。", "I made a copy of the documents.", K6D5)
V("複雑", "ふくざつな", "Complex/complicated", "この問題は複雑だ。", "このもんだいはふくざつだ。", "This problem is complicated.", K6D5)
V("複数", "ふくすう", "The plural (number)", "複数の候補から一つ選んだ。", "ふくすうのこうほからひとつえらんだ。", "I chose one from multiple candidates.", K6D5)
V("刊行物", "かんこうぶつ", "A publication", "出版社の刊行物を確認した。", "しゅっぱんしゃのかんこうぶつをかくにんした。", "I checked the publisher's publications.", K6D5)
V("週刊", "しゅうかん", "Weekly publication", "週刊誌を毎週買っている。", "しゅうかんしをまいしゅうかっている。", "I buy a weekly magazine every week.", K6D5)
V("朝刊", "ちょうかん", "A morning newspaper", "朝刊を読みながら朝食をとる。", "ちょうかんをよみながらちょうしょくをとる。", "I have breakfast while reading the morning paper.", K6D5)
V("月刊", "げっかん", "Monthly publication", "月刊の雑誌を定期購読している。", "げっかんのざっしをていきこうどくしている。", "I have a subscription to a monthly magazine.", K6D5)

# --- Kanji Day 6: どっち？ ---
# 約束 (already carded elsewhere, week4), 厚かましい (week1 vocab), and 苦痛 (week5 kanji d4)
# skipped as cross-week duplicates.
K6D6 = "kanji::w6 kanji::w6d6 jlpt::n2"
V("高層", "こうそう", "The upper layers", "高層マンションに住んでいる。", "こうそうマンションにすんでいる。", "I live in a high-rise condo.", K6D6)
V("一層", "いっそう", "More/still more", "練習して一層上手になった。", "れんしゅうしていっそうじょうずになった。", "I practiced and got even better.", K6D6)
V("低層", "ていそう", "The lower layers", "この地域は低層の建物が多い。", "このちいきはていそうのたてものがおおい。", "This area has many low-rise buildings.", K6D6)
V("花束", "はなたば", "A bunch of flowers", "母に花束を贈った。", "ははにはなたばをおくった。", "I gave my mother a bouquet.", K6D6)
V("束", "たば", "A bunch/bundle", "書類を束にして整理した。", "しょるいをたばにしてせいりした。", "I bundled the documents together and organized them.", K6D6)
V("束ねる", "たばねる", "Bind in a bunch/bundle", "髪を後ろで束ねた。", "かみをうしろでたばねた。", "I tied my hair back.", K6D6)
V("甘い", "あまい", "Sweet", "このケーキはとても甘い。", "このケーキはとてもあまい。", "This cake is very sweet.", K6D6)
V("甘やかす", "あまやかす", "Spoil (a child)", "子どもを甘やかしすぎるのはよくない。", "こどもをあまやかしすぎるのはよくない。", "Spoiling children too much isn't good.", K6D6)
V("甘口", "あまくち", "The sweet side", "甘口のカレーを注文した。", "あまくちのカレーをちゅうもんした。", "I ordered mild curry.", K6D6)
V("辛い", "からい", "(Spicy) hot", "このスープはとても辛い。", "このスープはとてもからい。", "This soup is very spicy.", K6D6)
V("辛口", "からくち", "The dry side", "辛口のワインが好きだ。", "からくちのワインがすきだ。", "I like dry wine.", K6D6)
V("皿", "さら", "A plate", "皿を洗った。", "さらをあらった。", "I washed the plates.", K6D6)
V("大皿", "おおざら", "A big plate", "料理を大皿に盛った。", "りょうりをおおざらにもった。", "I served the food on a big plate.", K6D6)
V("小皿", "こざら", "A small plate", "小皿に醤油を入れた。", "こざらにしょうゆをいれた。", "I poured soy sauce into a small dish.", K6D6)
V("綿", "めん", "Cotton", "綿のシャツは着心地がいい。", "めんのシャツはきごこちがいい。", "Cotton shirts are comfortable to wear.", K6D6)
V("木綿", "もめん", "Cotton/cotton cloth", "木綿の豆腐を買った。", "もめんのとうふをかった。", "I bought firm/cotton tofu.", K6D6)
V("綿", "わた", "Cotton (wool)/a cotton plant", "布団に綿を詰めた。", "ふとんにわたをつめた。", "I stuffed the futon with cotton batting.", K6D6)
V("旧館", "きゅうかん", "The older building", "ホテルの旧館に泊まった。", "ホテルのきゅうかんにとまった。", "I stayed in the hotel's old wing.", K6D6)
V("旧姓", "きゅうせい", "A maiden name", "今は田中ですが、旧姓は林です。", "いまはたなかですが、きゅうせいははやしです。", "I'm Tanaka now, but my maiden name is Hayashi.", K6D6)
V("復旧", "ふっきゅう", "Restoration", "停電が復旧した。", "ていでんがふっきゅうした。", "Power was restored.", K6D6)
V("厚生労働省", "こうせいろうどうしょう", "Ministry of Health, Labour and Welfare", "厚生労働省が新しい方針を発表した。", "こうせいろうどうしょうがあたらしいほうしんをはっぴょうした。", "The Ministry of Health, Labour and Welfare announced a new policy.", K6D6)
V("厚い", "あつい", "Thick", "厚い本を読んでいる。", "あついほんをよんでいる。", "I'm reading a thick book.", K6D6)
V("厚切り", "あつぎり", "A thick slice", "厚切りのパンを買った。", "あつぎりのパンをかった。", "I bought thick-sliced bread.", K6D6)
V("厚手", "あつで", "A thickly made article", "厚手のセーターを着た。", "あつでのセーターをきた。", "I wore a thick sweater.", K6D6)
V("薄い", "うすい", "Thin (material)/light (color)/weak (drink)", "このお茶は味が薄い。", "このおちゃはあじがうすい。", "This tea tastes weak.", K6D6)
V("薄手", "うすで", "A thinly made article", "薄手のコートを買った。", "うすでのコートをかった。", "I bought a lightweight coat.", K6D6)
V("薄切り", "うすぎり", "A thin slice", "薄切りの肉を炒めた。", "うすぎりのにくをいためた。", "I stir-fried thinly sliced meat.", K6D6)
V("薄める", "うすめる", "Dilute", "ジュースを水で薄めた。", "ジュースをみずでうすめた。", "I diluted the juice with water.", K6D6)
V("粒", "つぶ", "A grain", "米の粒を数えた。", "こめのつぶをかぞえた。", "I counted grains of rice.", K6D6)
V("北極", "ほっきょく", "The North Pole", "北極には氷が広がっている。", "ほっきょくにはこおりがひろがっている。", "Ice spreads across the Arctic.", K6D6)
V("積極的", "せっきょくてきな", "Active/positive", "もっと積極的に発言してください。", "もっとせっきょくてきにはつげんしてください。", "Please speak up more actively.", K6D6)
V("南極", "なんきょく", "The South Pole", "南極大陸を探検した学者がいる。", "なんきょくたいりくをたんけんしたがくしゃがいる。", "There are scholars who explored the Antarctic continent.", K6D6)
V("消極的", "しょうきょくてきな", "Passive/negative", "彼は消極的な性格だ。", "かれはしょうきょくてきなせいかくだ。", "He has a passive personality.", K6D6)
V("極", "ごく", "Very/extremely", "極普通の生活を送っている。", "ごくふつうのせいかつをおくっている。", "I lead a perfectly ordinary life.", K6D6)
V("改革", "かいかく", "A reform", "教育制度の改革が必要だ。", "きょういくせいどのかいかくがひつようだ。", "Educational system reform is necessary.", K6D6)
V("革", "かわ", "Leather", "革のバッグを買った。", "かわのバッグをかった。", "I bought a leather bag.", K6D6)
V("革命", "かくめい", "A revolution", "フランス革命について学んだ。", "フランスかくめいについてまなんだ。", "I studied the French Revolution.", K6D6)
V("革製", "かわせい", "Made of leather", "革製の財布を使っている。", "かわせいのさいふをつかっている。", "I use a leather wallet.", K6D6)
V("苦しい", "くるしい", "Distressful/trying", "生活が苦しい。", "せいかつがくるしい。", "Life is hard/difficult.", K6D6)
V("苦い", "にがい", "Bitter", "このコーヒーは苦い。", "このコーヒーはにがい。", "This coffee is bitter.", K6D6)
V("苦しむ", "くるしむ", "Suffer", "病気で苦しんでいる。", "びょうきでくるしんでいる。", "He is suffering from illness.", K6D6)

# --- Kanji Day 7 Extra: 見た目が似ている漢字 (bonus puzzle, kanji 554-564) ---
# 永's only listed word, 永久, was already carded under 週 week4 kanji d3 -- skipped as a duplicate.
K6DE = "kanji::w6 kanji::w6dExtra jlpt::n2"
V("困る", "こまる", "Be in trouble", "お金がなくて困っている。", "おかねがなくてこまっている。", "I'm in trouble because I have no money.", K6DE)
V("氷", "こおり", "Ice", "氷をグラスに入れた。", "こおりをグラスにいれた。", "I put ice in the glass.", K6DE)
V("夫", "おっと", "A husband", "夫は今、出張中だ。", "おっとはいま、しゅっちょうちゅうだ。", "My husband is on a business trip right now.", K6DE)
V("知識", "ちしき", "Knowledge", "彼は幅広い知識を持っている。", "かれははばひろいちしきをもっている。", "He has broad knowledge.", K6DE)
V("挟む", "はさむ", "Pinch/insert", "パンにハムを挟んだ。", "パンにハムをはさんだ。", "I put ham in the bread.", K6DE)
V("狭い", "せまい", "Narrow", "この部屋は狭い。", "このへやはせまい。", "This room is small/narrow.", K6DE)
V("群れ", "むれ", "A group/flock", "鳥の群れが空を飛んでいる。", "とりのむれがそらをとんでいる。", "A flock of birds is flying in the sky.", K6DE)
V("祖先", "そせん", "Ancestors", "私たちの祖先はこの土地に住んでいた。", "わたしたちのそせんはこのとちにすんでいた。", "Our ancestors lived on this land.", K6DE)
V("隅", "すみ", "A corner (of a room)", "部屋の隅に荷物を置いた。", "へやのすみににもつをおいた。", "I put the luggage in the corner of the room.", K6DE)
V("偶数", "ぐうすう", "An even number", "2は偶数だ。", "2はぐうすうだ。", "2 is an even number.", K6DE)

# --- Vocabulary Day 1: カタカナで書く言葉① (Abbreviations & Pronunciation) ---
VOC6D1 = "vocabulary::w6 vocabulary::w6d1 jlpt::n2"
V("デジカメ／デジタルカメラ", "デジカメ／デジタルカメラ", "Digital camera", "旅行にデジカメを持っていった。", "りょこうにデジカメをもっていった。", "I brought a digital camera on my trip.", VOC6D1)
V("ラッシュ／ラッシュアワー", "ラッシュ／ラッシュアワー", "Rush hour", "朝のラッシュを避けて出勤する。", "あさのラッシュをさけてしゅっきんする。", "I go to work avoiding the morning rush hour.", VOC6D1)
V("マスコミ／マスコミュニケーション", "マスコミ／マスコミュニケーション", "Mass media", "マスコミが事件を大きく報じた。", "マスコミがじけんをおおきくほうじた。", "The mass media reported the incident extensively.", VOC6D1)
V("テロ／テロリズム", "テロ／テロリズム", "Terrorism/terrorist attack", "世界各地でテロが起きている。", "せかいかくちでテロがおきている。", "Terrorist attacks are occurring around the world.", VOC6D1)
V("インフレ／インフレーション", "インフレ／インフレーション", "Inflation", "最近、インフレが進んでいる。", "さいきん、インフレがすすんでいる。", "Inflation has been progressing recently.", VOC6D1)
V("デフレ", "デフレ", "Deflation", "デフレで物価が下がった。", "デフレでぶっかがさがった。", "Prices fell due to deflation.", VOC6D1)
V("アポ（イント）／アポイントメント", "アポ（イント）／アポイントメント", "Appointment", "明日の12時に面会のアポをとった。", "あしたの12じにめんかいのアポをとった。", "I made an appointment to meet at 12 tomorrow.", VOC6D1)
V("ミス", "ミス", "Mistake", "試験でミスをしないように気をつける。", "しけんでミスをしないようにきをつける。", "I'm careful not to make mistakes on the exam.", VOC6D1)
V("イラスト／イラストレーション", "イラスト／イラストレーション", "Illustration", "本にかわいいイラストが入っている。", "ほんにかわいいイラストがはいっている。", "The book has cute illustrations.", VOC6D1)
V("アマ／アマチュア", "アマ／アマチュア", "Amateur", "彼はアマチュアのゴルファーだ。", "かれはアマチュアのゴルファーだ。", "He is an amateur golfer.", VOC6D1)
V("プロ／プロフェッショナル", "プロ／プロフェッショナル", "Professional", "彼はプロのカメラマンです。", "かれはプロのカメラマンです。", "He is a professional photographer.", VOC6D1)
V("プロダクション", "プロダクション", "Production (e.g. show business)", "芸能プロダクションに所属している。", "げいのうプロダクションにしょぞくしている。", "She belongs to a talent production agency.", VOC6D1)
V("スト／ストライキ", "スト／ストライキ", "Strike", "電車はストで動いておりません。", "でんしゃはストでうごいておりません。", "The train isn't running due to a strike.", VOC6D1)
V("レジ", "レジ", "Cash-register", "レジで支払いをした。", "レジでしはらいをした。", "I paid at the cash register.", VOC6D1)
V("ゼミ／ゼミナール", "ゼミ／ゼミナール", "Seminar", "大学でゼミに参加している。", "だいがくでゼミにさんかしている。", "I participate in a seminar at university.", VOC6D1)
V("ホーム／プラットフォーム", "ホーム／プラットフォーム", "Platform", "電車はホームに到着した。", "でんしゃはホームにとうちゃくした。", "The train arrived at the platform.", VOC6D1)
V("ホイル／アルミホイル", "ホイル／アルミホイル", "Aluminium foil", "魚をホイルで包んで焼いた。", "さかなをホイルでつつんでやいた。", "I wrapped the fish in foil and grilled it.", VOC6D1)
V("バーゲン／バーゲンセール", "バーゲン／バーゲンセール", "Sale", "デパートでバーゲンが始まった。", "デパートでバーゲンがはじまった。", "A sale started at the department store.", VOC6D1)
V("ファミレス／ファミリーレストラン", "ファミレス／ファミリーレストラン", "Family restaurant", "週末はよくファミレスで食事する。", "しゅうまつはよくファミレスでしょくじする。", "I often eat at a family restaurant on weekends.", VOC6D1)
V("エコ／エコロジー", "エコ／エコロジー", "Ecology/eco-friendly", "エコな生活を心がけている。", "エコなせいかつをこころがけている。", "I try to live an eco-friendly lifestyle.", VOC6D1)
V("アレルギー", "アレルギー", "Allergy/allergic reaction", "卵にアレルギーがある。", "たまごにアレルギーがある。", "I'm allergic to eggs.", VOC6D1)
V("エネルギー", "エネルギー", "Energy", "太陽エネルギーを利用する。", "たいようエネルギーをりようする。", "We use solar energy.", VOC6D1)
V("ウイルス", "ウイルス", "Virus", "パソコンがウイルスに感染した。", "パソコンがウイルスにかんせんした。", "My computer got infected with a virus.", VOC6D1)
V("ワクチン", "ワクチン", "Vaccine", "インフルエンザのワクチンを打った。", "インフルエンザのワクチンをうった。", "I got a flu vaccine shot.", VOC6D1)
V("ビタミン", "ビタミン", "Vitamin", "野菜にはビタミンが多く含まれる。", "やさいにはビタミンがおおくふくまれる。", "Vegetables contain a lot of vitamins.", VOC6D1)
V("サプリメント", "サプリメント", "Supplements", "毎日サプリメントを飲んでいる。", "まいにちサプリメントをのんでいる。", "I take supplements every day.", VOC6D1)
V("テーマ", "テーマ", "Theme/topic", "今日はこの問題をテーマに講義します。", "きょうはこのもんだいをテーマにこうぎします。", "Today's lecture will be themed around this issue.", VOC6D1)
V("ビニール", "ビニール", "Plastic/vinyl", "ビニール袋に入れて持ち帰った。", "ビニールぶくろにいれてもちかえった。", "I put it in a plastic bag and took it home.", VOC6D1)

# --- Vocabulary Day 2: カタカナで書く言葉② (Media, Services & Daily Life) ---
VOC6D2 = "vocabulary::w6 vocabulary::w6d2 jlpt::n2"
V("アイドル歌手", "アイドルかしゅ", "A popular young singer/idol", "娘はアイドル歌手のファンだ。", "むすめはアイドルかしゅのファンだ。", "My daughter is a fan of an idol singer.", VOC6D2)
V("テレビタレント", "テレビタレント", "A TV personality", "彼はテレビタレントとして人気がある。", "かれはテレビタレントとしてにんきがある。", "He is popular as a TV personality.", VOC6D2)
V("クレームをつける／言う", "クレームをつける／いう", "Complain/make a claim", "商品にクレームをつけた。", "しょうひんにクレームをつけた。", "I made a complaint about the product.", VOC6D2)
V("サービスがいい", "サービスがいい", "Provides good service", "あのホテルはサービスがいい。", "あのホテルはサービスがいい。", "That hotel provides good service.", VOC6D2)
V("ホテルのフロント", "ホテルのフロント", "Reception desk", "ホテルのフロントで鍵を受け取った。", "ホテルのフロントでかぎをうけとった。", "I received the key at the hotel's front desk.", VOC6D2)
V("シングル", "シングル", "A single room", "シングルの部屋を予約した。", "シングルのへやをよやくした。", "I booked a single room.", VOC6D2)
V("ツイン", "ツイン", "A twin room", "ツインの部屋に二人で泊まった。", "ツインのへやにふたりでとまった。", "Two of us stayed in a twin room.", VOC6D2)
V("フルコース／コース料理", "フルコース／コースりょうり", "A multiple course meal", "記念日にフルコースの料理を食べた。", "きねんびにフルコースのりょうりをたべた。", "I had a full-course meal on our anniversary.", VOC6D2)
V("バイキング形式の食事", "バイキングけいしきのしょくじ", "Buffet meal", "朝食はバイキング形式だった。", "ちょうしょくはバイキングけいしきだった。", "Breakfast was a buffet.", VOC6D2)
V("ドライな性格", "ドライなせいかく", "A cold/dry personality", "彼女はドライな性格だ。", "かのじょはドライなせいかくだ。", "She has a cool/detached personality.", VOC6D2)
V("（車の）ハンドル", "（くるまの）ハンドル", "Steering wheel", "運転中はハンドルをしっかり握る。", "うんてんちゅうはハンドルをしっかりにぎる。", "Hold the steering wheel firmly while driving.", VOC6D2)
V("タイヤがパンクする", "タイヤがパンクする", "Have a flat tire", "帰り道でタイヤがパンクした。", "かえりみちでタイヤがパンクした。", "I got a flat tire on the way home.", VOC6D2)
V("学校のグラウンド", "がっこうのグラウンド", "The school yard", "学校のグラウンドでサッカーをした。", "がっこうのグラウンドでサッカーをした。", "We played soccer on the school grounds.", VOC6D2)
V("コピー機／コピー用紙", "コピーき／コピーようし", "A photo copying machine/paper", "コピー機の用紙がなくなった。", "コピーきのようしがなくなった。", "The photocopier ran out of paper.", VOC6D2)
V("デパートの化粧品コーナー", "デパートのけしょうひんコーナー", "Cosmetic section in a department store", "デパートの化粧品コーナーで口紅を買った。", "デパートのけしょうひんコーナーでくちべにをかった。", "I bought lipstick at the department store's cosmetics section.", VOC6D2)
V("ガソリンスタンド", "ガソリンスタンド", "A gas station", "ガソリンスタンドで給油した。", "ガソリンスタンドできゅうゆした。", "I filled up at the gas station.", VOC6D2)
V("電気スタンド", "でんきスタンド", "A desk lamp", "机に電気スタンドを置いた。", "つくえにでんきスタンドをおいた。", "I put a desk lamp on the desk.", VOC6D2)
V("ビジネスマン", "ビジネスマン", "A businessman/company employee", "兄はビジネスマン関係の会社に勤めています。", "あにはビジネスマンかんけいのかいしゃにつとめています。", "My brother works at a business-related company.", VOC6D2)
V("ポイントカード", "ポイントカード", "Point card", "クレジットカードのポイントをためて商品券をもらった。", "クレジットカードのポイントをためてしょうひんけんをもらった。", "I saved up my credit card points and got a gift certificate.", VOC6D2)
V("コメントをする／述べる", "コメントをする／のべる", "Voice your opinion/comment", "その件についてコメントを述べた。", "そのけんについてコメントをのべた。", "I commented on that matter.", VOC6D2)
V("ノーコメント", "ノーコメント", "No comment", "その件に関してはノーコメントです。", "そのけんにかんしてはノーコメントです。", "I have no comment on that matter.", VOC6D2)
V("予算がオーバーする", "よさんがオーバーする", "Be over budget", "旅行の費用が予算をオーバーした。", "りょこうのひようがよさんをオーバーした。", "The trip's cost went over budget.", VOC6D2)
V("オーバーに話す", "オーバーにはなす", "Exaggerate", "彼はいつもオーバーに話す。", "かれはいつもオーバーにはなす。", "He always exaggerates when he talks.", VOC6D2)
V("日本人とドイツ人のハーフ", "にほんじんとドイツじんのハーフ", "A person who is half Japanese and half German", "彼女は日本人とドイツ人のハーフだ。", "かのじょはにほんじんとドイツじんのハーフだ。", "She is half Japanese, half German.", VOC6D2)
V("ユニークな人／考え", "ユニークなひと／かんがえ", "A unique person/a unique opinion", "とてもユニークなデザインの衣装ですね。", "とてもユニークなデザインのいしょうですね。", "What a unique design for a costume.", VOC6D2)
V("ベテラン", "ベテラン", "An expert/someone with a lot of experience", "父はキャリア30年のベテランパイロットです。", "ちちはキャリア30ねんのベテランパイロットです。", "My father is a veteran pilot with 30 years of experience.", VOC6D2)
V("トレーナー", "トレーナー", "Sweat shirt/trainer (coach)", "寒い日はトレーナーを着る。", "さむいひはトレーナーをきる。", "I wear a sweatshirt on cold days.", VOC6D2)
V("受け取りのサインをする", "うけとりのサインをする", "Sign the receipt", "荷物の受け取りのサインをした。", "にもつのうけとりのサインをした。", "I signed for receipt of the package.", VOC6D2)

# --- Vocabulary Day 3: カタカナで書く言葉③ (Wasei-Eigo & Common Katakana Terms) ---
VOC6D3 = "vocabulary::w6 vocabulary::w6d3 jlpt::n2"
V("コンパ", "コンパ", "A welcoming party for new students", "新入生歓迎のコンパに参加した。", "しんにゅうせいかんげいのコンパにさんかした。", "I attended the welcome party for new students.", VOC6D3)
V("合コン", "ごうコン", "A coed party/mixer", "友達に誘われて合コンに行った。", "ともだちにさそわれてごうコンにいった。", "I was invited by a friend and went to a mixer.", VOC6D3)
V("ワンパターン（な）", "ワンパターン（な）", "A person with a one-track mind/monotonous", "彼の話はいつもワンパターンだ。", "かれのはなしはいつもワンパターンだ。", "His stories are always the same pattern.", VOC6D3)
V("ゴールデンウィーク", "ゴールデンウィーク", "Golden Week", "ゴールデンウィークに旅行する予定だ。", "ゴールデンウィークにりょこうするよていだ。", "I plan to travel during Golden Week.", VOC6D3)
V("Uターン", "ユーターン", "Make a U-turn/return to one's hometown", "正月に田舎へUターンする人が多い。", "しょうがつにいなかへユーターンするひとがおおい。", "Many people return to their hometown for New Year's.", VOC6D3)
V("オフ", "オフ", "A day off work", "今日は仕事がオフの日だ。", "きょうはしごとがオフのひだ。", "Today is my day off from work.", VOC6D3)
V("フリーダイヤル", "フリーダイヤル", "A toll-free number", "テレビショッピングの商品をフリーダイヤルで注文した。", "テレビショッピングのしょうひんをフリーダイヤルでちゅうもんした。", "I ordered the TV shopping product using the toll-free number.", VOC6D3)
V("フリーサイズ", "フリーサイズ", "One size fits all", "この服はフリーサイズです。", "このふくはフリーサイズです。", "This clothing is one-size-fits-all.", VOC6D3)
V("キャッチボール", "キャッチボール", "Play catch", "子どものころ、よく父とキャッチボールをした。", "こどものころ、よくちちとキャッチボールをした。", "When I was a child, I often played catch with my father.", VOC6D3)
V("コインランドリー", "コインランドリー", "A laundromat", "コインランドリーで布団を洗った。", "コインランドリーでふとんをあらった。", "I washed my futon at the laundromat.", VOC6D3)
V("リサイクルショップ", "リサイクルショップ", "A recycling shop", "古い洗濯機をリサイクルショップで売った。", "ふるいせんたくきをリサイクルショップでうった。", "I sold my old washing machine at a recycling shop.", VOC6D3)
V("ジェットコースター", "ジェットコースター", "A roller coaster", "遊園地でジェットコースターに乗った。", "ゆうえんちでジェットコースターにのった。", "I rode the roller coaster at the amusement park.", VOC6D3)
V("パトカー", "パトカー", "A police car", "パトカーがサイレンを鳴らして通り過ぎた。", "パトカーがサイレンをならしてとおりすぎた。", "A police car passed by with its siren blaring.", VOC6D3)
V("ガードマン", "ガードマン", "A security guard", "ビルの入り口にガードマンが立っている。", "ビルのいりぐちにガードマンがたっている。", "A security guard stands at the building's entrance.", VOC6D3)
V("サインペン", "サインペン", "A felt-tipped pen", "サインペンで名前を書いた。", "サインペンでなまえをかいた。", "I wrote my name with a felt-tip pen.", VOC6D3)
V("マイホーム", "マイホーム", "A private house/one's own home", "夫婦でマイホームを購入した。", "ふうふでマイホームをこうにゅうした。", "The couple bought their own home.", VOC6D3)
V("キーホルダー", "キーホルダー", "A key chain", "お土産にキーホルダーを買った。", "おみやげにキーホルダーをかった。", "I bought a keychain as a souvenir.", VOC6D3)
V("シルバーシート", "シルバーシート", "A priority seat", "電車のシルバーシートに座った。", "でんしゃのシルバーシートにすわった。", "I sat in the priority seat on the train.", VOC6D3)
V("ホチキス", "ホチキス", "Stapler", "書類をホチキスで留めた。", "しょるいをホチキスでとめた。", "I stapled the documents together.", VOC6D3)
V("コンテスト", "コンテスト", "Contest", "写真コンテストに応募した。", "しゃしんコンテストにおうぼした。", "I entered a photo contest.", VOC6D3)
V("コンクール", "コンクール", "Competition", "合唱コンクールで優勝した。", "がっしょうコンクールでゆうしょうした。", "We won the choir competition.", VOC6D3)
V("セロテープ", "セロテープ", "Cellophane tape/clear tape", "チラシをセロテープで壁に貼った。", "チラシをセロテープでかべにはった。", "I taped the flyer to the wall with cellophane tape.", VOC6D3)
V("タイプ", "タイプ", "Type", "あの店の服は、どれも安っぽいタイプだ。", "あのみせのふくは、どれもやすっぽいタイプだ。", "All the clothes at that shop seem cheap.", VOC6D3)
V("イメージ", "イメージ", "Image/impression", "会社のイメージが変わった。", "かいしゃのイメージがかわった。", "The company's image has changed.", VOC6D3)
V("テンポ", "テンポ", "Tempo/pace", "この曲はテンポが速い。", "このきょくはテンポがはやい。", "This song has a fast tempo.", VOC6D3)
V("リズム", "リズム", "Rhythm/beat", "生活のリズムを整える。", "せいかつのリズムをととのえる。", "I'm regulating my daily rhythm.", VOC6D3)
V("バランス", "バランス", "Balance", "バランスのよい食事を心がけている。", "バランスのよいしょくじをこころがけている。", "I try to have a balanced diet.", VOC6D3)
V("ハンサム（な）", "ハンサム（な）", "Handsome/good-looking", "彼はハンサムな男性だ。", "かれはハンサムなだんせいだ。", "He is a handsome man.", VOC6D3)
V("スマート（な）", "スマート（な）", "Slim/slender", "彼女はスマートな体型をしている。", "かのじょはスマートなたいけいをしている。", "She has a slender figure.", VOC6D3)

# --- Vocabulary Day 4: 似ている言葉① ---
# 破る (already carded kanji d2), 埋める (week3 kanji), ぶらさげる (week2 vocab), 枯れる
# (week5 kanji extra) skipped as cross-week/within-week duplicates.
VOC6D4 = "vocabulary::w6 vocabulary::w6d4 jlpt::n2"
V("飛ぶ", "とぶ", "Fly", "鳥が空を飛んでいる。", "とりがそらをとんでいる。", "Birds are flying in the sky.", VOC6D4)
V("跳ねる", "はねる", "Jump", "池で、魚が跳ねている。", "いけで、さかながはねている。", "Fish are jumping in the pond.", VOC6D4)
V("転ぶ", "ころぶ", "Fall/trip", "道で転んでけがをした。", "みちでころんでけがをした。", "I fell on the street and got hurt.", VOC6D4)
V("転がる", "ころがる", "Roll", "ボールが道路に転がっていった。", "ボールがどうろにころがっていった。", "The ball rolled into the road.", VOC6D4)
V("ちぎる", "ちぎる", "Tear off", "パンを小さくちぎって食べた。", "パンをちいさくちぎってたべた。", "I tore the bread into small pieces and ate it.", VOC6D4)
V("ほえる", "ほえる", "Bark", "犬が大きな声でほえた。", "いぬがおおきなこえでほえた。", "The dog barked loudly.", VOC6D4)
V("うなる", "うなる", "Growl/groan", "問題の答えがわからずうなってしまった。", "もんだいのこたえがわからずうなってしまった。", "I groaned because I couldn't figure out the answer to the problem.", VOC6D4)
V("もれる", "もれる", "Leak (e.g. water leaks out)", "天井から雨がもれている。", "てんじょうからあめがもれている。", "Rain is leaking from the ceiling.", VOC6D4)
V("こぼれる", "こぼれる", "Spill", "コップから水がこぼれた。", "コップからみずがこぼれた。", "Water spilled from the cup.", VOC6D4)
V("ふさぐ", "ふさぐ", "Cover/block up", "くしゃみをするとき、手で口をふさいだ。", "くしゃみをするとき、てでくちをふさいだ。", "I covered my mouth with my hand when sneezing.", VOC6D4)
V("つるす", "つるす", "Hang (e.g. a curtain)", "窓にカーテンをつるした。", "まどにカーテンをつるした。", "I hung curtains on the window.", VOC6D4)
V("なめる", "なめる", "Lick", "犬が私の手をなめた。", "いぬがわたしのてをなめた。", "The dog licked my hand.", VOC6D4)
V("しゃぶる", "しゃぶる", "Suck (e.g. candy)", "風邪でのどが痛いので、あめをしゃぶった。", "かぜでのどがいたいので、あめをしゃぶった。", "My throat hurt from a cold, so I sucked on a candy.", VOC6D4)
V("ずらす", "ずらす", "Put off/shift", "雪のため、試験の開始時間を30分ずらした。", "ゆきのため、しけんのかいしじかんを30ぷんずらした。", "Due to snow, the exam start time was shifted by 30 minutes.", VOC6D4)
V("どける", "どける", "Move (something) out of the way", "通行のじゃまになるので、このいすをどけてください。", "つうこうのじゃまになるので、このいすをどけてください。", "Please move this chair out of the way, it's blocking traffic.", VOC6D4)
V("しぼむ", "しぼむ", "Wilt/fade (for flowers/balloons)", "風船が一日でしぼんでしまった。", "ふうせんがいちにちでしぼんでしまった。", "The balloon deflated within a day.", VOC6D4)
V("傷つく", "きずつく", "Be hurt", "彼の言葉に傷ついた。", "かれのことばにきずついた。", "I was hurt by his words.", VOC6D4)
V("傷がつく", "きずがつく", "Get a scratch", "新車にもう傷がついてしまった。", "しんしゃにもうきずがついてしまった。", "My new car already has a scratch on it.", VOC6D4)
V("新たにする", "あらたにする", "Renew", "契約を新たにした。", "けいやくをあらたにした。", "We renewed the contract.", VOC6D4)
V("改める", "あらためる", "Deal with shortcomings/change/call again", "彼は先生に注意されて、態度を改めた。", "かれはせんせいにちゅういされて、たいどをあらためた。", "He was warned by the teacher and changed his attitude.", VOC6D4)
V("先に", "さきに", "Previously/ahead", "先に田中さんからお電話がありました。", "さきにたなかさんからおでんわがありました。", "Mr. Tanaka called earlier.", VOC6D4)
V("先ほど", "さきほど", "Earlier/a short while ago", "先ほどお伝えした通りです。", "さきほどおつたえしたとおりです。", "It's as I mentioned earlier.", VOC6D4)

# --- Vocabulary Day 5: 似ている言葉② ---
# 意外 is deliberately left out here even though the source lists it under Day 5 -- it's the same
# headword as Day 6's 意外／以外 contrastive pair, so it's carded once, under Day 6.
VOC6D5 = "vocabulary::w6 vocabulary::w6d5 jlpt::n2"
V("すべて", "すべて", "All/entirely", "すべての参加者に賞品が当たった。", "すべてのさんかしゃにしょうひんがあたった。", "All participants received a prize.", VOC6D5)
V("第一（に）", "だいいち（に）", "First of all", "何よりも第一に安全を考えるべきだ。", "なによりもだいいちにあんぜんをかんがえるべきだ。", "Safety should be considered first above all else.", VOC6D5)
V("真っ先に", "まっさきに", "The very first", "地震のとき、教室から真っ先に逃げ出したのは先生だった。", "じしんのとき、きょうしつからまっさきににげだしたのはせんせいだった。", "When the earthquake hit, the teacher was the very first to run out of the classroom.", VOC6D5)
V("あらゆる", "あらゆる", "Every possible", "あらゆる方法を試してみた。", "あらゆるほうほうをためしてみた。", "I tried every possible method.", VOC6D5)
V("以前", "いぜん", "Previously/used to be", "1900年以前の記録はもう残っていません。", "1900ねんいぜんのきろくはもうのこっていません。", "Records from before 1900 no longer remain.", VOC6D5)
V("かつて", "かつて", "Once/formerly", "この辺りにはかつて公園があった。", "このあたりにはかつてこうえんがあった。", "There used to be a park around here.", VOC6D5)
V("単に", "たんに", "Simply/merely", "これは単なる誤解にすぎない。", "これはたんなるごかいにすぎない。", "This is merely a misunderstanding.", VOC6D5)
V("ただ", "ただ", "Just/only", "ただ見ているだけでは何も変わらない。", "ただみているだけではなにもかわらない。", "Just watching won't change anything.", VOC6D5)
V("まね", "まね", "Imitate/act like", "クモは危険を感じると死んだまねをする。", "クモはきけんをかんじるとしんだまねをする。", "Spiders play dead when they sense danger.", VOC6D5)
V("ふり", "ふり", "Pretend", "眠っているふりをした。", "ねむっているふりをした。", "I pretended to be asleep.", VOC6D5)
V("必死に", "ひっしに", "Desperately/frantically", "彼は必死に勉強して医者になった。", "かれはひっしにべんきょうしていしゃになった。", "He studied desperately hard and became a doctor.", VOC6D5)
V("無理に／無理やり", "むりに／むりやり", "By force/forcefully", "子どもに野菜を無理に食べさせた。", "こどもにやさいをむりにたべさせた。", "I forced the child to eat vegetables.", VOC6D5)
V("高級（な）", "こうきゅうな", "High class/luxury", "友人に高級なワインをもらった。", "ゆうじんにこうきゅうなワインをもらった。", "I received a high-class wine from a friend.", VOC6D5)
V("上等（な）", "じょうとうな", "High quality/excellent", "このバッグは上等な革でできている。", "このバッグはじょうとうなかわでできている。", "This bag is made of high-quality leather.", VOC6D5)
V("高度（な）", "こうどな", "High degree/advanced", "高度な技術が必要な仕事だ。", "こうどなぎじゅつがひつようなしごとだ。", "This job requires advanced skill.", VOC6D5)
V("高等（な）", "こうとうな", "Higher grade (e.g. higher education)", "高等教育を受ける機会が増えた。", "こうとうきょういくをうけるきかいがふえた。", "Opportunities to receive higher education have increased.", VOC6D5)
V("高価（な）", "こうかな", "Highly priced/expensive", "高価な時計を買った。", "こうかなとけいをかった。", "I bought an expensive watch.", VOC6D5)
V("勝手に", "かってに", "On one's own/selfishly", "人の物を勝手に使わないでください。", "ひとのものをかってにつかわないでください。", "Please don't use other people's things without permission.", VOC6D5)
V("無断で", "むだんで", "Without permission/without notice", "無断で欠席してはいけません。", "むだんでけっせきしてはいけません。", "You must not be absent without permission.", VOC6D5)
V("次々（に／と）", "つぎつぎに", "One after another", "新しい店が次々にオープンしている。", "あたらしいみせがつぎつぎにオープンしている。", "New shops are opening one after another.", VOC6D5)
V("続々（と）", "ぞくぞくと", "Successively/one after another", "インフルエンザが流行し、患者が続々と増えている。", "インフルエンザがりゅうこうし、かんじゃがぞくぞくとふえている。", "The flu is spreading and patients are increasing successively.", VOC6D5)
V("案外（と）", "あんがいと", "Unexpectedly/contrary to expectation", "その映画はみんなはつまらないと言っていたが、案外面白かった。", "そのえいがはみんなはつまらないといっていたが、あんがいおもしろかった。", "Everyone said the movie was boring, but it was surprisingly interesting.", VOC6D5)
V("余計に", "よけいに", "More/excessively", "医者へ行ったら余計に症状が悪化した。", "いしゃへいったらよけいにしょうじょうがあっかした。", "After going to the doctor, my symptoms got worse instead.", VOC6D5)
V("余分に", "よぶんに", "Extra/in excess", "余分にコピーを取っておいた。", "よぶんにコピーをとっておいた。", "I made extra copies just in case.", VOC6D5)

# --- Vocabulary Day 6: 似ている言葉③ ---
# 辺り (already carded kanji d4), 見方 (week5 vocab), あきる／あきれる／あきらめる／もたれる／
# くやしい (all week3 vocab) skipped as cross-week duplicates.
VOC6D6 = "vocabulary::w6 vocabulary::w6d6 jlpt::n2"
V("責める", "せめる", "Blame/condemn", "失敗した部下を責めた。", "しっぱいしたぶかをせめた。", "I blamed my subordinate for the failure.", VOC6D6)
V("攻める", "せめる", "Attack", "敵の城を攻めた。", "てきのしろをせめた。", "They attacked the enemy's castle.", VOC6D6)
V("乗る", "のる", "Ride/take part in", "電車に乗って会社に行く。", "でんしゃにのってかいしゃにいく。", "I take the train to work.", VOC6D6)
V("載る", "のる", "Be published/be placed on", "犯人の名前が新聞に載っていた。", "はんにんのなまえがしんぶんにのっていた。", "The culprit's name was published in the newspaper.", VOC6D6)
V("当たり", "あたり", "Per (e.g. per person)/a hit", "1人当たり1000円かかる。", "1にんあたり1000えんかかる。", "It costs 1000 yen per person.", VOC6D6)
V("以外", "いがい", "Except/other than", "彼以外は全員来た。", "かれいがいはぜんいんきた。", "Everyone except him came.", VOC6D6)
V("意外", "いがい", "Unexpected/surprising", "事件の犯人は意外な人物だった。", "じけんのはんにんはいがいなじんぶつだった。", "The culprit of the incident was an unexpected person.", VOC6D6)
V("夫人", "ふじん", "Mrs./wife", "大統領夫人が来日した。", "だいとうりょうふじんがらいにちした。", "The president's wife visited Japan.", VOC6D6)
V("婦人", "ふじん", "Woman/lady", "婦人服売り場で服を買った。", "ふじんふくうりばでふくをかった。", "I bought clothes at the women's clothing section.", VOC6D6)
V("人口", "じんこう", "Population", "この都市の人口は年々増えている。", "このとしのじんこうはねんねんふえている。", "This city's population is increasing year by year.", VOC6D6)
V("人工", "じんこう", "Artificial/man-made", "これは人工で作られた湖である。", "これはじんこうでつくられたみずうみである。", "This is an artificially created lake.", VOC6D6)
V("味方", "みかた", "Ally/supporter", "彼はいつも私の味方をしてくれる。", "かれはいつもわたしのみかたをしてくれる。", "He always takes my side.", VOC6D6)
V("特徴", "とくちょう", "Distinguishing feature (good or bad)", "キリンは首が長いのが特徴です。", "キリンはくびがながいのがとくちょうです。", "The giraffe's distinguishing feature is its long neck.", VOC6D6)
V("特長", "とくちょう", "Strong point/merit", "この製品の特長は軽さです。", "このせいひんのとくちょうはかるさです。", "This product's strong point is its lightness.", VOC6D6)
V("ある", "ある", "A certain/some", "ある日、彼から手紙が届いた。", "あるひ、かれからてがみがとどいた。", "One day, I received a letter from him.", VOC6D6)
V("あくる", "あくる", "Next/following (day)", "彼女は入社したあくる年に結婚した。", "かのじょはにゅうしゃしたあくるとしにけっこんした。", "She got married the year after joining the company.", VOC6D6)
V("もたらす", "もたらす", "Bring about/cause", "インターネットは情報社会に大きい変化をもたらした。", "インターネットはじょうほうしゃかいにおおきいへんかをもたらした。", "The internet brought about a great change to the information society.", VOC6D6)
V("詳しい", "くわしい", "Detailed/knowledgeable", "彼は歴史に詳しい。", "かれはれきしにくわしい。", "He is knowledgeable about history.", VOC6D6)
V("実は", "じつは", "To tell the truth/actually", "死んだと思った猫は実は隣の家で飼われていた。", "しんだとおもったねこはじつはとなりのいえでかわれていた。", "The cat I thought had died was actually being kept next door.", VOC6D6)
V("実に", "じつに", "Really/truly", "実に美しい景色だ。", "じつにうつくしいけしきだ。", "What a truly beautiful view.", VOC6D6)

# --- Reading extraction (annotated/glossary vocabulary from reading-w6.md) ---
# 用語 skipped (already carded week5 as ようご).
R6D1 = "reading::w6 reading::w6d1 jlpt::n2"
V("掲示板", "けいじばん", "A bulletin board system (BBS)", "インターネットの掲示板に意見を書き込んだ。", "インターネットのけいじばんにいけんをかきこんだ。", "I posted my opinion on the internet bulletin board.", R6D1)
V("書き込み", "かきこみ", "Posting", "掲示板の書き込みを読んだ。", "けいじばんのかきこみをよんだ。", "I read the posts on the bulletin board.", R6D1)
V("進化する", "しんかする", "To evolve", "言葉は時代とともに進化する。", "ことばはじだいとともにしんかする。", "Language evolves with the times.", R6D1)
V("猛烈なスピードで", "もうれつなスピードで", "At a breakneck speed", "技術が猛烈なスピードで進歩している。", "ぎじゅつがもうれつなスピードでしんぽしている。", "Technology is advancing at a breakneck speed.", R6D1)

R6D2 = "reading::w6 reading::w6d2 jlpt::n2"
V("チカチカする", "チカチカする", "(eyes) burning/stinging", "目がチカチカして痛い。", "めがチカチカしていたい。", "My eyes are stinging and hurt.", R6D2)
V("シックハウス症候群", "シックハウスしょうこうぐん", "Sick-house syndrome", "新築の家でシックハウス症候群になった。", "しんちくのいえでシックハウスしょうこうぐんになった。", "I developed sick-house syndrome in the newly built house.", R6D2)
V("接着剤", "せっちゃくざい", "Adhesive", "壁紙を接着剤で貼った。", "かべがみをせっちゃくざいではった。", "I glued the wallpaper on with adhesive.", R6D2)
V("反応", "はんのう", "A reaction", "薬にアレルギー反応を起こした。", "くすりにアレルギーはんのうをおこした。", "I had an allergic reaction to the medicine.", R6D2)
V("ホルムアルデヒド", "ホルムアルデヒド", "Formaldehyde", "接着剤にホルムアルデヒドが含まれている。", "せっちゃくざいにホルムアルデヒドがふくまれている。", "The adhesive contains formaldehyde.", R6D2)
V("たんぱく質", "たんぱくしつ", "Protein", "肉や魚にはたんぱく質が多い。", "にくやさかなにはたんぱくしつがおおい。", "Meat and fish are high in protein.", R6D2)
V("形成する", "けいせいする", "To form", "人体の多くはたんぱく質で形成されている。", "じんたいのおおくはたんぱくしつでけいせいされている。", "Much of the human body is formed of protein.", R6D2)

R6D3 = "reading::w6 reading::w6d3 jlpt::n2"
V("スズメバチ", "スズメバチ", "A hornet", "庭でスズメバチを見かけた。", "にわでスズメバチをみかけた。", "I saw a hornet in the garden.", R6D3)
V("はれる", "はれる", "To swell", "蚊に刺されたところがはれた。", "かにさされたところがはれた。", "The spot where I was bitten by a mosquito swelled up.", R6D3)
V("アレルギー体質", "アレルギーたいしつ", "Allergic constitution", "私はアレルギー体質だ。", "わたしはアレルギーたいしつだ。", "I have an allergic constitution.", R6D3)
V("毒性が強い", "どくせいがつよい", "Very poisonous", "このきのこは毒性が強い。", "このきのこはどくせいがつよい。", "This mushroom is highly poisonous.", R6D3)
V("襲う", "おそう", "To attack", "熊が人を襲った。", "くまがひとをおそった。", "A bear attacked a person.", R6D3)
V("ショック症状", "ショックしょうじょう", "Shock symptoms", "彼はアレルギーのショック症状を起こした。", "かれはアレルギーのショックしょうじょうをおこした。", "He had an allergic shock reaction.", R6D3)
V("抗体", "こうたい", "Antibody", "体の中に抗体ができた。", "からだのなかにこうたいができた。", "Antibodies formed in the body.", R6D3)
V("習性", "しゅうせい", "Behavior patterns", "ハチには黒いものを攻撃する習性がある。", "ハチにはくろいものをこうげきするしゅうせいがある。", "Bees have a behavior pattern of attacking black objects.", R6D3)

R6D4 = "reading::w6 reading::w6d4 jlpt::n2"
V("てっぺん", "てっぺん", "The top/summit", "山のてっぺんまで登った。", "やまのてっぺんまでのぼった。", "I climbed to the top of the mountain.", R6D4)
V("遠心力", "えんしんりょく", "Centrifugal force", "遠心力で水がこぼれなかった。", "えんしんりょくでみずがこぼれなかった。", "The water didn't spill due to centrifugal force.", R6D4)
V("差し掛かる", "さしかかる", "To approach", "車が坂道に差し掛かった。", "くるまがさかみちにさしかかった。", "The car approached the slope.", R6D4)

R6D5 = "reading::w6 reading::w6d5 jlpt::n2"
V("けいれん", "けいれん", "Convulsions", "足がけいれんして動けなかった。", "あしがけいれんしてうごけなかった。", "My leg cramped up and I couldn't move.", R6D5)

R6D6 = "reading::w6 reading::w6d6 jlpt::n2"
V("割り切れる", "わりきれる", "Can be divided by", "17は2でも3でも割り切れない。", "17は2でも3でもわりきれない。", "17 cannot be evenly divided by 2 or 3.", R6D6)
V("前述の", "ぜんじゅつの", "Aforementioned", "前述の理由により、計画を中止します。", "ぜんじゅつのりゆうにより、けいかくをちゅうしします。", "For the aforementioned reasons, we will cancel the plan.", R6D6)

R6D7 = "reading::w6 reading::w6d7 jlpt::n2"
V("猛獣", "もうじゅう", "A fierce/wild beast", "動物園で猛獣を見た。", "どうぶつえんでもうじゅうをみた。", "I saw a wild beast at the zoo.", R6D7)
V("とっさに", "とっさに", "Instantly/in a split second", "とっさに体が動いた。", "とっさにからだがうごいた。", "My body moved instantly.", R6D7)
V("白ける", "しらける", "To become awkward/lose enthusiasm", "彼の一言で場が白けた。", "かれのひとことでばがしらけた。", "His one remark made the atmosphere awkward.", R6D7)
V("しどろもどろ", "しどろもどろ", "Flustered/incoherent", "質問されてしどろもどろになった。", "しつもんされてしどろもどろになった。", "I became flustered when asked the question.", R6D7)
V("かねてから", "かねてから", "From before", "かねてから計画していたことを実行した。", "かねてからけいかくしていたことをじっこうした。", "I carried out something I had been planning for a while.", R6D7)
V("一気になごむ", "いっきになごむ", "Atmosphere suddenly improves", "冗談を言うと場が一気になごんだ。", "じょうだんをいうとばがいっきになごんだ。", "The atmosphere suddenly relaxed when he made a joke.", R6D7)
V("朝礼", "ちょうれい", "Morning meeting", "毎朝、会社で朝礼がある。", "まいあさ、かいしゃでちょうれいがある。", "There's a morning meeting at the company every day.", R6D7)
V("取引先", "とりひきさき", "Business partner", "取引先と打ち合わせをした。", "とりひきさきとうちあわせをした。", "I had a meeting with a business partner.", R6D7)
V("ネタ", "ネタ", "Material/topic (of a story)", "面白いネタを探している。", "おもしろいネタをさがしている。", "I'm looking for interesting material.", R6D7)
V("客観的に", "きゃっかんてきに", "Objectively", "客観的に物事を見るようにしている。", "きゃっかんてきにものごとをみるようにしている。", "I try to look at things objectively.", R6D7)
V("肝心である", "かんじんである", "Crucial", "最初の一歩が肝心である。", "さいしょのいっぽがかんじんである。", "The first step is crucial.", R6D7)
V("あけたて", "あけたて", "Opening and closing", "障子のあけたてに気をつける。", "しょうじのあけたてにきをつける。", "Be careful when opening and closing the shoji screen.", R6D7)
V("いたく", "いたく", "Very, deeply", "彼はその話にいたく感動した。", "かれはそのはなしにいたくかんどうした。", "He was deeply moved by that story.", R6D7)

# --- Grammar Day 1: 決めた以上 ---
G6D1 = "grammar::w6 grammar::w6d1 jlpt::n2 type::grammar"
G("〜て以来", "ていらい", "explanation", "ever since",
  [("日本に来て以来、母の料理を食べていない。", "にほんにきていらい、ははのりょうりをたべていない。", "Since I came to Japan, I haven't eaten my mother's food.")], G6D1)
G("〜て以来", "ていらい", "explanation", "ever since",
  [("入学以来、一度も授業を休んでいない。", "にゅうがくいらい、いちどもじゅぎょうをやすんでいない。", "Since I entered school, I have never missed class.")], G6D1)
G("〜以上(は)", "いじょう(は)", "explanation", "now that/since... (must act accordingly)",
  [("試験を受ける以上、いい点を取りたい。", "しけんをうけるいじょう、いいてんをとりたい。", "Now that I'm taking the test, I want to do well.")], G6D1)
G("〜以上(は)", "いじょう(は)", "explanation", "now that/since... (must act accordingly)",
  [("日本に来た以上は、日本語ができるようになりたい。", "にほんにきたいじょうは、にほんごができるようになりたい。", "Now that I've come to Japan, I want to become competent in Japanese.")], G6D1)
G("〜からには", "からには", "explanation", "now that/since... (strong resolve or duty)",
  [("約束したからには、守るべきだ。", "やくそくしたからには、まもるべきだ。", "Since you have made a promise, you should keep it.")], G6D1)
G("〜からには", "からには", "explanation", "now that/since... (strong resolve or duty)",
  [("試合に出るからには、勝ちたい。", "しあいにでるからには、かちたい。", "Since I'll be in the games, I want to win.")], G6D1)
G("〜折(に)", "おり(に)", "explanation", "when/at the time of (formal)",
  [("来日の折には、ぜひこちらにお立ち寄りください。", "らいにちのおりには、ぜひこちらにおたちよりください。", "Please visit us when you come to Japan.")], G6D1)
G("〜折(に)", "おり(に)", "explanation", "when/at the time of (formal)",
  [("次にお目にかかった折に、お返しします。", "つぎにおめにかかったおりに、おかえしします。", "I will return it the next time I see you.")], G6D1)

# --- Grammar Day 2: ぼくから見ると ---
G6D2 = "grammar::w6 grammar::w6d2 jlpt::n2 type::grammar"
G("〜から言うと／〜から言えば", "からいうと／からいえば", "explanation", "from the perspective of...",
  [("客の立場から言うと、この店は入り口がせまくて入りにくい。", "きゃくのたちばからいうと、このみせはいりぐちがせまくてはいりにくい。", "From the customer's perspective, this shop has a small entrance and is hard to enter.")], G6D2)
G("〜から言うと／〜から言えば", "からいうと／からいえば", "explanation", "from the perspective of...",
  [("しかし、店の側から言えば管理しやすい。", "しかし、みせのがわからいえばかんりしやすい。", "However, from the perspective of the shop, it is easy to manage.")], G6D2)
G("〜からすると／〜からすれば／〜からいって", "からすると／からすれば／からいって", "explanation", "judging from",
  [("症状からすると、心臓の病気かもしれません。", "しょうじょうからすると、しんぞうのびょうきかもしれません。", "Judging from the symptoms, it might be a heart disease.")], G6D2)
G("〜からすると／〜からすれば／〜からいって", "からすると／からすれば／からいって", "explanation", "judging from",
  [("周りの態度からすると、あの方が社長ではないでしょうか。", "まわりのたいどからすると、あのかたがしゃちょうではないでしょうか。", "Judging from the attitudes of the people around him, he is probably the president.")], G6D2)
G("〜からして", "からして", "explanation", "judging from/even just by...",
  [("彼は服装からしてだらしない。きっと、ほかの面も同じだろう。", "かれはふくそうからしてだらしない。きっと、ほかのめんもおなじだろう。", "He is sloppy, even just looking at his dress. He's probably the same in other aspects.")], G6D2)
G("〜からして", "からして", "explanation", "judging from/even just by...",
  [("あの映画は、題名からして悲しそうだ。", "あのえいがは、だいめいからしてかなしそうだ。", "Based on the title alone, the movie seems sad.")], G6D2)
G("〜から見ると／〜から見れば", "からみると／からみれば", "explanation", "from the perspective of...",
  [("日本の習慣には、外国人から見ると妙なものもあるだろう。", "にほんのしゅうかんには、がいこくじんからみるとみょうなものもあるだろう。", "From a foreigner's perspective, some Japanese customs may seem strange.")], G6D2)
G("〜から見ると／〜から見れば", "からみると／からみれば", "explanation", "from the perspective of...",
  [("昔の人から見ると、現代人の生活のリズムは速すぎるかもしれない。", "むかしのひとからみると、げんだいじんのせいかつのリズムははやすぎるかもしれない。", "From the perspective of people in the past, modern life might seem too fast.")], G6D2)

# --- Grammar Day 3: 声の大きさにかけては ---
G6D3 = "grammar::w6 grammar::w6d3 jlpt::n2 type::grammar"
G("〜からといって", "からといって", "explanation", "just because...",
  [("好きだからといって、同じ食品ばかり食べるのはよくない。", "すきだからといって、おなじしょくひんばかりたべるのはよくない。", "Just because you like it, it's not good to eat the same food all the time.")], G6D3)
G("〜からといって", "からといって", "explanation", "just because...",
  [("日本に住んでいるからといって、日本語がしゃべれるようにはならない。", "にほんにすんでいるからといって、にほんごがしゃべれるようにはならない。", "Just because you live in Japan doesn't mean you can speak Japanese.")], G6D3)
G("〜てからでないと／〜てからでなければ", "てからでないと／てからでなければ", "explanation", "unless/until after...",
  [("手続きしてからでないと、図書館の本は借りられない。", "てつづきしてからでないと、としょかんのほんはかりられない。", "Unless you complete the procedures, you cannot borrow library books.")], G6D3)
G("〜てからでないと／〜てからでなければ", "てからでないと／てからでなければ", "explanation", "unless/until after...",
  [("親の許可をもらってからでなければ、申し込めない。", "おやのきょかをもらってからでなければ、もうしこめない。", "Unless you get your parents' permission, you cannot apply.")], G6D3)
G("〜から〜にかけて", "から〜にかけて", "explanation", "from X to Y (time or place)",
  [("私は、2007年から2009年にかけて、ロンドンに住んでいました。", "わたしは、2007ねんから2009ねんにかけて、ロンドンにすんでいました。", "I lived in London from 2007 to 2009.")], G6D3)
G("〜から〜にかけて", "から〜にかけて", "explanation", "from X to Y (time or place)",
  [("この駅から、あそこの通りにかけて、再開発されるそうです。", "このえきから、あそこのとおりにかけて、さいかいはつされるそうです。", "They are going to redevelop the space between this station and that street.")], G6D3)
G("〜にかけては", "にかけては", "explanation", "when it comes to...",
  [("足の速さにかけては、彼は町で一番だ。", "あしのはやさにかけては、かれはまちでいちばんだ。", "When it comes to running, he is the best in town.")], G6D3)
G("〜にかけては", "にかけては", "explanation", "when it comes to...",
  [("歌のうまさにかけては、彼に勝てる人はいない。", "うたのうまさにかけては、かれにかてるひとはいない。", "When it comes to singing, no one can beat him.")], G6D3)

# --- Grammar Day 4: 行こうか行くまいか ---
G6D4 = "grammar::w6 grammar::w6d4 jlpt::n2 type::grammar"
G("〜とか", "とか", "explanation", "I hear that.../they say that... (uncertain hearsay)",
  [("今夜の花火大会は、雨で中止だとか。", "こんやのはなびたいかいは、あめでちゅうしだとか。", "I hear that the fireworks display tonight has been cancelled because of the rain.")], G6D4)
G("〜とか", "とか", "explanation", "I hear that.../they say that... (uncertain hearsay)",
  [("今、インフルエンザがはやっているとか。", "いま、インフルエンザがはやっているとか。", "I hear that the flu has broken out right now.")], G6D4)
G("〜まい", "まい", "explanation", "will not (negative volition, formal)",
  [("あんなひどいところ、二度と行くまい。", "あんなひどいところ、にどといくまい。", "I will never go to such an awful place.")], G6D4)
G("〜まい", "まい", "explanation", "will not (negative volition, formal)",
  [("海外旅行では、絶対に買った水以外は飲むまいと思った。", "かいがいりょこうでは、ぜったいにかったみずいがいはのむまいとおもった。", "On overseas trips, I've decided only to drink bottled water.")], G6D4)
G("〜まい", "まい", "explanation", "probably not (negative conjecture)",
  [("彼には私の気持ちはわかるまい。", "かれにはわたしのきもちはわかるまい。", "He will not understand my feelings.")], G6D4)
G("〜まい", "まい", "explanation", "probably not (negative conjecture)",
  [("上級者でも、この問題はできまい。", "じょうきゅうしゃでも、このもんだいはできまい。", "This is a question even advanced students won't be able to answer.")], G6D4)
G("〜まい", "まい", "explanation", "probably not (negative conjecture)",
  [("もっと！夢ではあるまいか。", "もっと！ゆめではあるまいか。", "Am I perhaps dreaming?")], G6D4)
G("〜ようか〜まいか", "ようか〜まいか", "explanation", "whether to do X or not",
  [("本当のことを話そうか話すまいか迷ったが、結局全部話した。", "ほんとうのことをはなそうかはなすまいかまよったが、けっきょくぜんぶはなした。", "I didn't know whether to tell or not, but in the end I told everything.")], G6D4)
G("〜ようか〜まいか", "ようか〜まいか", "explanation", "whether to do X or not",
  [("食べたいけど、太りたくないし、食べようか食べまいか考えているところです。", "たべたいけど、ふとりたくないし、たべようかたべまいかかんがえているところです。", "I want to eat it, but I don't want to get fat. To eat or not to eat, this is a question.")], G6D4)

# --- Grammar Day 5: 負けるに決まっている ---
G6D5 = "grammar::w6 grammar::w6d5 jlpt::n2 type::grammar"
G("〜に決まっている／〜に違いない／〜に相違ない", "にきまっている／にちがいない／にそういない", "explanation", "must be/bound to be",
  [("あのチームが勝つに決まっている。", "あのチームがかつにきまっている。", "That team is bound to win.")], G6D5)
G("〜に決まっている／〜に違いない／〜に相違ない", "にきまっている／にちがいない／にそういない", "explanation", "must be/bound to be",
  [("彼がやったに違いない。", "かれがやったにちがいない。", "He must have done it.")], G6D5)
G("〜に決まっている／〜に違いない／〜に相違ない", "にきまっている／にちがいない／にそういない", "explanation", "must be/bound to be",
  [("彼が犯人に相違ない。", "かれがはんにんにそういない。", "He must be the offender.")], G6D5)
G("〜とは限らない", "とはかぎらない", "explanation", "not necessarily",
  [("相手が弱いチームであっても、必ず勝つとは限らない。", "あいてがよわいチームであっても、かならずかつとはかぎらない。", "Just because the other team is not good, there is always the possibility of us losing.")], G6D5)
G("〜とは限らない", "とはかぎらない", "explanation", "not necessarily",
  [("あまり使わない表現だが、必ずしもテストに出ないとは限らない。", "あまりつかわないひょうげんだが、かならずしもテストにでないとはかぎらない。", "It is not an expression that is used a lot, but there is the possibility of it appearing on the test.")], G6D5)
G("〜より(は)ほかない／〜よりほかはない", "より(は)ほかない／よりほかはない", "explanation", "no choice but to (formal)",
  [("全力をつくした。あとは祈るほかない。", "ぜんりょくをつくした。あとはいのるほかない。", "I tried my best. All I can do now is to pray.")], G6D5)
G("〜より(は)ほかない／〜よりほかはない", "より(は)ほかない／よりほかはない", "explanation", "no choice but to (formal)",
  [("もう後には戻れない。前進するほかない。", "もうあとにはもどれない。ぜんしんするほかない。", "I can't go back now. I have no choice but to move forward.")], G6D5)
G("〜にほかならない", "にほかならない", "explanation", "nothing but/precisely because of",
  [("合格したのは、彼の努力の結果にほかならない。", "ごうかくしたのは、かれのどりょくのけっかにほかならない。", "The reason why he passed is nothing but a result of his effort.")], G6D5)
G("〜にほかならない", "にほかならない", "explanation", "nothing but/precisely because of",
  [("彼があなたをからかうのは、まさに愛情表現にほかならない。", "かれがあなたをからかうのは、まさにあいじょうひょうげんにほかならない。", "The reason he teases you is nothing but an expression of his love.")], G6D5)

# --- Grammar Day 6: 金メダルをめぐって ---
G6D6 = "grammar::w6 grammar::w6d6 jlpt::n2 type::grammar"
G("〜をはじめ／〜をはじめとする", "をはじめ／をはじめとする", "explanation", "starting with/such as",
  [("会議には中国をはじめ、アジアの国々が参加した。", "かいぎにはちゅうごくをはじめ、アジアのくにぐにがさんかした。", "China and other Asian countries participated in the conference.")], G6D6)
G("〜をはじめ／〜をはじめとする", "をはじめ／をはじめとする", "explanation", "starting with/such as",
  [("わが国では、野球をはじめとして、サッカーやテニスなど、様々なスポーツがさかんである。", "わがくにでは、やきゅうをはじめとして、サッカーやテニスなど、さまざまなスポーツがさかんである。", "In our country, various sports are played enthusiastically including baseball, soccer, and tennis.")], G6D6)
G("〜をめぐって／〜をめぐる", "をめぐって／をめぐる", "explanation", "concerning/over",
  [("憲法改正をめぐって、長い間、論争が続いている。", "けんぽうかいせいをめぐって、ながいあいだ、ろんそうがつづいている。", "Over a long time, there has been a continuing dispute over a constitutional amendment.")], G6D6)
G("〜をめぐって／〜をめぐる", "をめぐって／をめぐる", "explanation", "concerning/over",
  [("教育制度をめぐる諸問題について、話し合う。", "きょういくせいどをめぐるしょもんだいについて、はなしあう。", "We discuss the problems about the educational system.")], G6D6)
G("〜において(は)／〜における", "において(は)／における", "explanation", "in/at (formal)",
  [("京都において、シンポジウムが行われた。", "きょうとにおいて、シンポジウムがおこなわれた。", "A symposium was held in Kyoto.")], G6D6)
G("〜において(は)／〜における", "において(は)／における", "explanation", "in/at (formal)",
  [("国際社会におけるわが国の役割を考える。", "こくさいしゃかいにおけるわがくにのやくわりをかんがえる。", "We think about the role of our nation in the international community.")], G6D6)
G("〜において(は)／〜における", "において(は)／における", "explanation", "in/at (formal)",
  [("Aさんの主張には、その点においては疑問があります。", "エーさんのしゅちょうには、そのてんにおいてはぎもんがあります。", "I have a question about one of Mr. A's points.")], G6D6)
G("〜にて", "にて", "explanation", "at/by (formal, notices and correspondence)",
  [("現地にて解散となります。", "げんちにてかいさんとなります。", "We plan to break up on the spot.")], G6D6)
G("〜にて", "にて", "explanation", "at/by (formal, notices and correspondence)",
  [("電話かメールにてご連絡ください。", "でんわかメールにてごれんらくください。", "Please contact me either by e-mail or phone.")], G6D6)
G("〜にて", "にて", "explanation", "at/by (formal, notices and correspondence)",
  [("京都にて　洋子より", "きょうとにて　ようこより", "From Yoko in Kyoto (used at the end of a postcard sent while traveling).")], G6D6)

# --- Reading-derived Deck 2 items (reading-w6.md Day 2's negative constructions) ---
G("一概に〜ない", "いちがいに〜ない", "explanation", "cannot generalize/cannot say across the board",
  [("これが原因だとは一概に言えない。", "これがげんいんだとはいちがいにいえない。", "You can't say across the board that this is the cause."),
   ("空気中のホルムアルデヒドの量はごくわずかで、一概に危険とも言えない。", "くうきちゅうのホルムアルデヒドのりょうはごくわずかで、いちがいにきけんともいえない。", "The amount of formaldehyde in the air is minimal, so it can't be called dangerous across the board.")],
  "reading::w6 reading::w6d2 jlpt::n2 type::grammar")
G("〜に満たない", "にみたない", "explanation", "insufficient/does not reach",
  [("空気中のホルムアルデヒドは、たんぱく質を変質させる量には満たない。", "くうきちゅうのホルムアルデヒドは、たんぱくしつをへんしつさせるりょうにはみたない。", "The formaldehyde in the air doesn't reach the amount needed to alter protein."),
   ("参加者は定員の半分にも満たなかった。", "さんかしゃはていいんのはんぶんにもみたなかった。", "The number of participants didn't even reach half the capacity.")],
  "reading::w6 reading::w6d2 jlpt::n2 type::grammar")

# --- Grammar Bonus: 敬語 (Keigo) — ほかの人について話す② ---
G6KEIGO = "grammar::w6 grammar::w6dExtra jlpt::n2 type::keigo"
G("いらっしゃる／しておいでになる", "いらっしゃる／しておいでになる", "explanation", "keigo for いる／している (to be/be doing, respectful)",
  [("社長のお父様は90歳でお元気でいらっしゃいます。", "しゃちょうのおとうさまは90さいでおげんきでいらっしゃいます。", "The company president's father is 90 years old and doing well."),
   ("社長のお父さんは90歳で元気だよ。", "しゃちょうのおとうさんは90さいでげんきだよ。", "The president's father is 90 and doing well.")], G6KEIGO)
G("お〜になれる／ご〜になれる", "お〜になれる／ご〜になれる", "explanation", "respectful potential form of 〜できる (never ×ご〜できます)",
  [("このカードはご利用になれます。", "このカードはごりようになれます。", "This card can be used."),
   ("このカードは使えます。", "このカードはつかえます。", "This card can be used.")], G6KEIGO)

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
        "# Week 6 (Sou Matome N2) — Japanese vocabulary: Kanji/Vocabulary/Reading words",
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
        "# Week 6 (Sou Matome N2) — Japanese grammar and usage: Grammar patterns",
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

    with open(os.path.join(base, "week6-v3-vocabulary.tsv"), "w", encoding="utf-8") as f:
        f.write(vocab_tsv)
    with open(os.path.join(base, "week6-v3-grammar-usage.tsv"), "w", encoding="utf-8") as f:
        f.write(grammar_tsv)
    print("Wrote TSVs.")

    if not errs:
        model1 = make_model(MODEL1_ID, "Japanese vocabulary")
        model2 = make_model(MODEL2_ID, "Japanese grammar and usage")
        n1 = build_apkg(vocab_tsv, DECK1_ID, "Japanese N2 Vocabulary", model1,
                         os.path.join(base, "week6-v3-vocabulary.apkg"))
        n2 = build_apkg(grammar_tsv, DECK2_ID, "Japanese N2 Grammar & Usage", model2,
                         os.path.join(base, "week6-v3-grammar-usage.apkg"))
        print(f"Wrote apkg: vocabulary={n1} notes, grammar-usage={n2} notes")
