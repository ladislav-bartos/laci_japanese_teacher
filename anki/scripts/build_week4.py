#!/usr/bin/env python3
"""Build Week 4 Anki TSV/apkg files (Deck 1 Vocabulary, Deck 2 Grammar & Usage).

Follows specs/anki-tsv-generation-process.md, specs/anki-note-type-vocabulary.md,
specs/anki-note-type-grammar-and-usage.md. Run from repo root:

    .venv/bin/python anki/scripts/build_week4.py
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

# --- Kanji Day 1: 伝票・申込書 ---
K4D1 = "kanji::w4 kanji::w4d1 jlpt::n2"
V("署名", "しょめい", "Signature", "契約書に署名をお願いします。", "けいやくしょにしょめいをおねがいします。", "Please sign the contract.", K4D1)
V("部署", "ぶしょ", "Post/station (department)", "彼は去年、別の部署に異動した。", "かれはきょねん、べつのぶしょにいどうした。", "He was transferred to a different department last year.", K4D1)
V("消防署", "しょうぼうしょ", "Fire station", "消防署に電話をして、火事を知らせた。", "しょうぼうしょにでんわをして、かじをしらせた。", "I called the fire station to report the fire.", K4D1)
V("税務署", "ぜいむしょ", "Tax office", "確定申告のために税務署へ行った。", "かくていしんこくのためにぜいむしょへいった。", "I went to the tax office to file my tax return.", K4D1)
V("依頼", "いらい", "Request/commission", "友人に通訳を依頼した。", "ゆうじんにつうやくをいらいした。", "I asked a friend to interpret for me.", K4D1)
V("信頼", "しんらい", "Trust", "彼は同僚からの信頼が厚い。", "かれはどうりょうからのしんらいがあつい。", "He is deeply trusted by his colleagues.", K4D1)
V("頼む", "たのむ", "Request", "引っ越しの手伝いを友達に頼んだ。", "ひっこしのてつだいをともだちにたのんだ。", "I asked a friend to help me move.", K4D1)
V("頼もしい", "たのもしい", "Reliable", "彼はいつも冷静で、頼もしい存在だ。", "かれはいつもれいせいで、たのもしいそんざいだ。", "He's always calm and a reliable presence.", K4D1)
V("頼る", "たよる", "Depend upon", "一人暮らしを始めてから、両親に頼ることが減った。", "ひとりぐらしをはじめてから、りょうしんにたよることがへった。", "Since living alone, I rely on my parents less.", K4D1)
V("頼りない", "たよりない", "Powerless/unreliable", "新人はまだ頼りないが、成長が早い。", "しんじんはまだたよりないが、せいちょうがはやい。", "The new employee is still unreliable, but growing fast.", K4D1)
V("都道府県", "とどうふけん", "Prefectures", "日本には47の都道府県がある。", "にほんには47のとどうふけんがある。", "Japan has 47 prefectures.", K4D1)
V("京都府", "きょうとふ", "Kyoto Prefecture", "京都府には歴史的な寺や神社が多い。", "きょうとふにはれきしてきなてらやじんじゃがおおい。", "Kyoto Prefecture has many historic temples and shrines.", K4D1)
V("到着", "とうちゃく", "Arrival", "飛行機は定刻通りに到着した。", "ひこうきはていこくどおりにとうちゃくした。", "The plane arrived on schedule.", K4D1)
V("希望", "きぼう", "Hope", "彼女は将来、医者になることを希望している。", "かのじょはしょうらい、いしゃになることをきぼうしている。", "She hopes to become a doctor in the future.", K4D1)
V("失望", "しつぼう", "Loss of hope/despair", "試験の結果に失望した。", "しけんのけっかにしつぼうした。", "I was disappointed by the exam results.", K4D1)
V("望む", "のぞむ", "Want/hope for", "平和な世界を望む人は多い。", "へいわなせかいをのぞむひとはおおい。", "Many people wish for a peaceful world.", K4D1)
V("望遠鏡", "ぼうえんきょう", "Telescope", "望遠鏡で星を観察する。", "ぼうえんきょうでほしをかんさつする。", "I observe stars with a telescope.", K4D1)
V("申請", "しんせい", "Application", "パスポートの申請をした。", "パスポートのしんせいをした。", "I applied for a passport.", K4D1)
V("申し込み", "もうしこみ", "Application/proposal", "講座の申し込みは来週までです。", "こうざのもうしこみはらいしゅうまでです。", "Applications for the course are due by next week.", K4D1)
V("申す", "もうす", "Say (humble)", "私は田中と申します。", "わたしはたなかともうします。", "My name is Tanaka.", K4D1)
V("申し上げる", "もうしあげる", "Say (very humble)", "心よりお礼を申し上げます。", "こころよりおれいをもうしあげます。", "I offer my sincere thanks.", K4D1)
V("姓", "せい", "Family name", "結婚して姓が変わった。", "けっこんしてせいがかわった。", "My family name changed when I got married.", K4D1)
V("姓名", "せいめい", "Full name", "申込書に姓名を記入してください。", "もうしこみしょにせいめいをきにゅうしてください。", "Please fill in your full name on the application form.", K4D1)
V("年齢", "ねんれい", "Age", "この仕事に年齢の制限はありません。", "このしごとにねんれいのせいげんはありません。", "There is no age limit for this job.", K4D1)
V("高齢", "こうれい", "Old age", "高齢の両親が心配だ。", "こうれいのりょうしんがしんぱいだ。", "I worry about my elderly parents.", K4D1)
V("男性", "だんせい", "Man", "この服は男性にも女性にも人気がある。", "このふくはだんせいにもじょせいにもにんきがある。", "This clothing is popular with both men and women.", K4D1)
V("女性", "じょせい", "Woman", "女性の管理職が増えている。", "じょせいのかんりしょくがふえている。", "The number of female managers is increasing.", K4D1)
V("性別", "せいべつ", "Sex/gender", "この調査では性別を答える必要はない。", "このちょうさではせいべつをこたえるひつようはない。", "In this survey, you don't need to answer your gender.", K4D1)
V("性質", "せいしつ", "Nature/disposition", "彼は穏やかな性質の人だ。", "かれはおだやかなせいしつのひとだ。", "He has a calm disposition.", K4D1)
V("安全性", "あんぜんせい", "Safety", "この製品の安全性が確認された。", "このせいひんのあんぜんせいがかくにんされた。", "This product's safety has been confirmed.", K4D1)
V("可能性", "かのうせい", "Possibility", "計画が成功する可能性は低い。", "けいかくがせいこうするかのうせいはひくい。", "The possibility of the plan succeeding is low.", K4D1)
V("お宅", "おたく", "House/home (respectful)", "来週、先生のお宅に伺います。", "らいしゅう、せんせいのおたくにうかがいます。", "I will visit my teacher's home next week.", K4D1)
V("住宅", "じゅうたく", "Housing", "この辺りは静かな住宅街だ。", "このあたりはしずかなじゅうたくがいだ。", "This area is a quiet residential neighborhood.", K4D1)
V("自宅", "じたく", "One's house/home", "今日は自宅で仕事をする。", "きょうはじたくでしごとをする。", "Today I will work from home.", K4D1)
V("帰宅", "きたく", "Returning home", "毎日、夜9時に帰宅する。", "まいにち、よる9じにきたくする。", "I return home at 9pm every day.", K4D1)
V("勤務", "きんむ", "Service/duty", "彼は病院で勤務している。", "かれはびょういんできんむしている。", "He works at a hospital.", K4D1)
V("出勤", "しゅっきん", "Attendance at work", "明日は9時に出勤します。", "あしたは9じにしゅっきんします。", "I will come to work at 9 tomorrow.", K4D1)
V("通勤", "つうきん", "Commuting to work", "電車で通勤しています。", "でんしゃでつうきんしています。", "I commute to work by train.", K4D1)
V("勤める", "つとめる", "Work/be employed", "姉は銀行に勤めている。", "あねはぎんこうにつとめている。", "My older sister works at a bank.", K4D1)
V("全部", "ぜんぶ", "All/whole", "宿題は全部終わった。", "しゅくだいはぜんぶおわった。", "I finished all of my homework.", K4D1)
V("部分", "ぶぶん", "Part", "この文章の重要な部分に線を引いた。", "このぶんしょうのじゅうようなぶぶんにせんをひいた。", "I underlined the important part of this text.", K4D1)
V("部長", "ぶちょう", "Department head/manager", "部長に相談してから決めます。", "ぶちょうにそうだんしてからきめます。", "I'll decide after consulting with the department head.", K4D1)
V("学部", "がくぶ", "Faculty", "彼は経済学部に通っている。", "かれはけいざいがくぶにかよっている。", "He attends the faculty of economics.", K4D1)
V("部屋", "へや", "Room", "自分の部屋を掃除した。", "じぶんのへやをそうじした。", "I cleaned my own room.", K4D1)


# --- Kanji Day 2: 返事を書く ---
K4D2 = "kanji::w4 kanji::w4d2 jlpt::n2"
V("結婚", "けっこん", "Marriage", "来年、二人は結婚する予定だ。", "らいねん、ふたりはけっこんするよていだ。", "The two of them plan to marry next year.", K4D2)
V("未婚", "みこん", "Unmarried", "彼は40歳になっても未婚だ。", "かれは40さいになってもみこんだ。", "He's still unmarried even at 40.", K4D2)
V("婚約", "こんやく", "Engagement", "二人は先月、婚約した。", "ふたりはせんげつ、こんやくした。", "The two got engaged last month.", K4D2)
V("新婚", "しんこん", "Newly wedded", "新婚旅行はハワイに行った。", "しんこんりょこうはハワイにいった。", "We went to Hawaii for our honeymoon.", K4D2)
V("招待", "しょうたい", "Invitation", "パーティーに招待された。", "パーティーにしょうたいされた。", "I was invited to the party.", K4D2)
V("招く", "まねく", "Invite", "結婚式に多くの友人を招いた。", "けっこんしきにおおくのゆうじんをまねいた。", "I invited many friends to my wedding.", K4D2)
V("状態", "じょうたい", "Situation/state", "車はまだ動かせる状態だ。", "くるまはまだうごかせるじょうたいだ。", "The car is still in a drivable state.", K4D2)
V("現状", "げんじょう", "Existing situation", "現状では改善は難しい。", "げんじょうではかいぜんはむずかしい。", "Improvement is difficult given the current situation.", K4D2)
V("年賀状", "ねんがじょう", "New Year's card", "毎年、友人に年賀状を送っている。", "まいとし、ゆうじんにねんがじょうをおくっている。", "I send New Year's cards to my friends every year.", K4D2)
V("欠席", "けっせき", "Absence", "風邪のため会議を欠席した。", "かぜのためかいぎをけっせきした。", "I was absent from the meeting due to a cold.", K4D2)
V("欠点", "けってん", "Shortcoming", "誰にでも欠点はある。", "だれにでもけってんはある。", "Everyone has shortcomings.", K4D2)
V("欠けている", "かけている", "Lacking", "この計画には具体性が欠けている。", "このけいかくにはぐたいせいがかけている。", "This plan is lacking in concreteness.", K4D2)
V("出欠", "しゅっけつ", "Attendance or absence", "出欠を確認してから始めます。", "しゅっけつをかくにんしてからはじめます。", "We'll start after confirming attendance.", K4D2)
V("喜ぶ", "よろこぶ", "Be pleased", "合格の知らせを聞いて家族が喜んだ。", "ごうかくのしらせをきいてかぞくがよろこんだ。", "My family was delighted to hear news of my passing.", K4D2)
V("喜んで", "よろこんで", "Gladly", "喜んでお手伝いします。", "よろこんでおてつだいします。", "I'll be glad to help.", K4D2)
V("政治", "せいじ", "Politics", "彼は政治に強い関心を持っている。", "かれはせいじにつよいかんしんをもっている。", "He has a strong interest in politics.", K4D2)
V("自治体", "じちたい", "Self-governing body", "この制度は各自治体によって異なる。", "このせいどはかくじちたいによってことなる。", "This system differs by local government.", K4D2)
V("自治会", "じちかい", "Self-governing association", "町内の自治会に参加している。", "ちょうないのじちかいにさんかしている。", "I participate in the neighborhood association.", K4D2)
V("治す", "なおす", "Cure", "早く風邪を治したい。", "はやくかぜをなおしたい。", "I want to get over my cold quickly.", K4D2)
V("委員", "いいん", "Committee member", "クラスの学級委員に選ばれた。", "クラスのがっきゅういいんにえらばれた。", "I was elected as the class representative.", K4D2)
V("委任状", "いにんじょう", "Power of attorney", "手続きには委任状が必要だ。", "てつづきにはいにんじょうがひつようだ。", "A power of attorney is required for the procedure.", K4D2)
V("委員会", "いいんかい", "Committee", "来週、委員会が開かれる。", "らいしゅう、いいんかいがひらかれる。", "The committee will be held next week.", K4D2)
V("祝日", "しゅくじつ", "Holiday/festival day", "来週の月曜日は祝日で休みだ。", "らいしゅうのげつようびはしゅくじつでやすみだ。", "Next Monday is a national holiday, so it's a day off.", K4D2)
V("祝う", "いわう", "Celebrate/congratulate", "友人の誕生日を祝った。", "ゆうじんのたんじょうびをいわった。", "I celebrated my friend's birthday.", K4D2)
V("お祝い", "おいわい", "Celebration/congratulation", "卒業のお祝いにプレゼントをもらった。", "そつぎょうのおいわいにプレゼントをもらった。", "I received a present to celebrate my graduation.", K4D2)
V("舞台", "ぶたい", "Stage", "彼女は舞台の上で緊張していた。", "かのじょはぶたいのうえできんちょうしていた。", "She was nervous on stage.", K4D2)
V("舞う", "まう", "Dance/flutter", "桜の花びらが風に舞っている。", "さくらのはなびらがかぜにまっている。", "Cherry blossom petals are fluttering in the wind.", K4D2)
V("お見舞い", "おみまい", "Call of inquiry/visit", "入院した友人にお見舞いに行った。", "にゅういんしたゆうじんにおみまいにいった。", "I went to visit my hospitalized friend.", K4D2)
V("お礼", "おれい", "Thanks/reward", "お世話になった先生にお礼を言った。", "おせわになったせんせいにおれいをいった。", "I thanked the teacher who had helped me.", K4D2)
V("礼儀", "れいぎ", "Etiquette", "彼は礼儀正しい青年だ。", "かれはれいぎただしいせいねんだ。", "He is a courteous young man.", K4D2)
V("失礼", "しつれいな", "Rude", "人前でそんなことを言うのは失礼だ。", "ひとまえでそんなことをいうのはしつれいだ。", "It's rude to say such a thing in front of others.", K4D2)
V("多忙", "たぼうな", "Busy with many things", "部長は多忙な毎日を送っている。", "ぶちょうはたぼうなまいにちをおくっている。", "The department head leads a very busy daily life.", K4D2)
V("忙しい", "いそがしい", "Busy", "今週はずっと忙しい。", "こんしゅうはずっといそがしい。", "I've been busy all this week.", K4D2)
V("夫妻", "ふさい", "Husband and wife", "田中夫妻をパーティーに招待した。", "たなかふさいをパーティーにしょうたいした。", "We invited Mr. and Mrs. Tanaka to the party.", K4D2)
V("妻", "つま", "Wife", "妻と一緒に買い物に行った。", "つまといっしょにかいものにいった。", "I went shopping with my wife.", K4D2)
V("主張", "しゅちょう", "Assertion/claim", "彼女は自分の権利を主張した。", "かのじょはじぶんのけんりをしゅちょうした。", "She asserted her own rights.", K4D2)
V("出張", "しゅっちょう", "Business trip", "来月、大阪へ出張することになった。", "らいげつ、おおさかへしゅっちょうすることになった。", "I'm going on a business trip to Osaka next month.", K4D2)
V("頑張る", "がんばる", "Try one's hardest", "試験に向けて頑張っている。", "しけんにむけてがんばっている。", "I'm working hard for the exam.", K4D2)
V("引っ張る", "ひっぱる", "Pull", "ロープを強く引っ張った。", "ロープをつよくひっぱった。", "I pulled the rope hard.", K4D2)
V("張る", "はる", "Stretch/tighten", "壁に大きな地図を張った。", "かべにおおきなちずをはった。", "I put a large map up on the wall.", K4D2)
V("奥様", "おくさま", "Wife (respectful form)", "社長の奥様にごあいさつした。", "しゃちょうのおくさまにごあいさつした。", "I greeted the company president's wife.", K4D2)
V("奥", "おく", "Inner recesses", "部屋の奥に本棚がある。", "へやのおくにほんだながある。", "There's a bookshelf at the back of the room.", K4D2)

# --- Kanji Day 3: メール・はがき ---
K4D3 = "kanji::w4 kanji::w4d3 jlpt::n2"
V("浅い", "あさい", "Shallow", "この川は浅いので子どもでも安全だ。", "このかわはあさいのでこどもでもあんぜんだ。", "This river is shallow, so it's safe even for children.", K4D3)
V("浅ましい", "あさましい", "Shameful/sordid", "お金のためなら何でもするなんて浅ましい。", "おかねのためならなんでもするなんてあさましい。", "Doing anything for money is shameful.", K4D3)
V("浅草", "あさくさ", "Asakusa (place name)", "浅草には古いお寺がある。", "あさくさにはふるいおてらがある。", "There's an old temple in Asakusa.", K4D3)
V("君", "きみ", "You", "君の意見を聞かせてほしい。", "きみのいけんをきかせてほしい。", "I want to hear your opinion.", K4D3)
V("永久", "えいきゅう", "Permanent", "この記念碑は永久に残るだろう。", "このきねんひはえいきゅうにのこるだろう。", "This monument will remain forever.", K4D3)
V("久しぶり", "ひさしぶり", "Long time no see", "久しぶりに高校時代の友人に会った。", "ひさしぶりにこうこうじだいのゆうじんにあった。", "I met an old high school friend after a long time.", K4D3)
V("相互", "そうご", "Mutual/reciprocal", "両国は相互に協力することにした。", "りょうこくはそうごにきょうりょくすることにした。", "The two countries decided to cooperate mutually.", K4D3)
V("お互いに", "おたがいに", "Mutually", "お互いに助け合いましょう。", "おたがいにたすけあいましょう。", "Let's help each other.", K4D3)
V("交互", "こうご", "Alternation", "二人は交互に運転した。", "ふたりはこうごにうんてんした。", "The two of them took turns driving.", K4D3)
V("追加", "ついか", "Addition/supplement", "料理をもう一品追加した。", "りょうりをもういっぴんついかした。", "I added one more dish to the order.", K4D3)
V("追い越す", "おいこす", "Overtake", "前の車を追い越した。", "まえのくるまをおいこした。", "I overtook the car in front.", K4D3)
V("追伸", "ついしん", "Postscript/P.S.", "手紙の最後に追伸を書いた。", "てがみのさいごについしんをかいた。", "I wrote a postscript at the end of the letter.", K4D3)
V("追い付く", "おいつく", "Catch up", "急いで走って友人に追い付いた。", "いそいではしってゆうじんにおいついた。", "I ran hard and caught up with my friend.", K4D3)
V("追う", "おう", "Pursue", "警察は犯人を追っている。", "けいさつははんにんをおっている。", "The police are pursuing the criminal.", K4D3)
V("伸ばす", "のばす", "Extend/stretch", "締め切りを一週間伸ばしてもらった。", "しめきりをいっしゅうかんのばしてもらった。", "I had the deadline extended by a week.", K4D3)
V("伸びる", "のびる", "Grow/stretch", "子どもの背がずいぶん伸びた。", "こどものせがずいぶんのびた。", "The child has grown quite tall.", K4D3)
V("伸びをする", "のびをする", "Stretch out", "朝起きて大きく伸びをした。", "あさおきておおきくのびをした。", "I woke up in the morning and stretched myself out.", K4D3)
V("皆", "みな", "All", "皆で協力して問題を解決した。", "みなできょうりょくしてもんだいをかいけつした。", "We all cooperated to solve the problem.", K4D3)
V("皆さん", "みなさん", "Everyone", "皆さん、お元気ですか。", "みなさん、おげんきですか。", "Everyone, how are you doing?", K4D3)
V("お歳暮", "おせいぼ", "Year-end gift", "毎年、お世話になった方にお歳暮を送る。", "まいとし、おせわになったかたにおせいぼをおくる。", "Every year, I send a year-end gift to those who have helped me.", K4D3)
V("暮れ", "くれ", "End of the year", "年の暮れは何かと忙しい。", "としのくれはなにかといそがしい。", "The end of the year is busy in various ways.", K4D3)
V("暮らす", "くらす", "Live/dwell", "田舎で静かに暮らしたい。", "いなかでしずかにくらしたい。", "I want to live quietly in the countryside.", K4D3)
V("夕暮れ", "ゆうぐれ", "Dusk", "夕暮れの空がきれいだった。", "ゆうぐれのそらがきれいだった。", "The sky at dusk was beautiful.", K4D3)
V("習慣", "しゅうかん", "Custom/habit", "毎朝走る習慣がある。", "まいあさはしるしゅうかんがある。", "I have a habit of running every morning.", K4D3)
V("慣れる", "なれる", "Become accustomed to", "新しい仕事にだいぶ慣れてきた。", "あたらしいしごとにだいぶなれてきた。", "I've gotten quite used to the new job.", K4D3)
V("生活", "せいかつ", "Life/livelihood", "都会での生活は物価が高い。", "とかいでのせいかつはぶっかがたかい。", "Living in the city is expensive.", K4D3)
V("活字", "かつじ", "Printing type", "最近は活字を読む機会が減った。", "さいきんはかつじをよむきかいがへった。", "Opportunities to read print have decreased recently.", K4D3)
V("活用", "かつよう", "Practical use", "この道具を有効に活用したい。", "このどうぐをゆうこうにかつようしたい。", "I want to make effective use of this tool.", K4D3)
V("活発", "かっぱつな", "Activity/vivacity", "クラスで活発な議論が行われた。", "クラスでかっぱつなぎろんがおこなわれた。", "There was an active discussion in class.", K4D3)
V("恋愛", "れんあい", "Love/romance", "二人は大学で恋愛関係になった。", "ふたりはだいがくでれんあいかんけいになった。", "The two started a romantic relationship in college.", K4D3)
V("恋人", "こいびと", "Lover", "彼には恋人がいる。", "かれにはこいびとがいる。", "He has a girlfriend.", K4D3)
V("恋", "こい", "Love", "初めての恋を思い出す。", "はじめてのこいをおもいだす。", "I remember my first love.", K4D3)
V("恋しい", "こいしい", "Homesick/lonely", "海外にいると故郷が恋しくなる。", "かいがいにいるとこきょうがこいしくなる。", "When abroad, I start to miss my hometown.", K4D3)
V("健在", "けんざい", "Being in good health", "祖父はまだ健在で、毎日散歩している。", "そふはまだけんざいで、まいにちさんぽしている。", "My grandfather is still going strong and walks every day.", K4D3)
V("健やか", "すこやかな", "Sound/healthy", "子どもの健やかな成長を願う。", "こどものすこやかなせいちょうをねがう。", "I wish for my child's healthy growth.", K4D3)
V("健康", "けんこう", "Health", "健康のために毎日運動している。", "けんこうのためにまいにちうんどうしている。", "I exercise every day for my health.", K4D3)
V("健全", "けんぜんな", "Sound/wholesome", "健全な財政を維持することが重要だ。", "けんぜんなざいせいをいじすることがじゅうようだ。", "Maintaining sound finances is important.", K4D3)
V("健康保険証", "けんこうほけんしょう", "Health insurance card", "病院に行くときは健康保険証を持っていく。", "びょういんにいくときはけんこうほけんしょうをもっていく。", "I bring my health insurance card when going to the hospital.", K4D3)
V("祈願", "きがん", "Prayer", "神社で合格祈願をした。", "じんじゃでごうかくきがんをした。", "I prayed for success at the shrine.", K4D3)
V("祈る", "いのる", "Pray", "家族の健康を祈った。", "かぞくのけんこうをいのった。", "I prayed for my family's health.", K4D3)
V("祈り", "いのり", "A prayer/grace", "食事の前に祈りをささげた。", "しょくじのまえにいのりをささげた。", "We said grace before the meal.", K4D3)

# --- Kanji Day 4: ビジネスメール ---
K4D4 = "kanji::w4 kanji::w4d4 jlpt::n2"
V("幸福", "こうふく", "Happiness", "お金があれば幸福だとは限らない。", "おかねがあればこうふくだとはかぎらない。", "Having money doesn't necessarily mean happiness.", K4D4)
V("福祉", "ふくし", "Welfare", "高齢者福祉の充実が求められている。", "こうれいしゃふくしのじゅうじつがもとめられている。", "There is a demand for improved welfare for the elderly.", K4D4)
V("拝見", "はいけん", "Looking (humble)", "お手紙を拝見しました。", "おてがみをはいけんしました。", "I have read your letter.", K4D4)
V("参拝者", "さんぱいしゃ", "Visitor to a shrine", "元日は神社に多くの参拝者が訪れる。", "がんじつはじんじゃにおおくのさんぱいしゃがおとずれる。", "Many worshippers visit shrines on New Year's Day.", K4D4)
V("拝借", "はいしゃく", "Borrowing (humble)", "お手洗いを拝借してもよろしいですか。", "おてあらいをはいしゃくしてもよろしいですか。", "May I borrow your restroom?", K4D4)
V("拝む", "おがむ", "Worship", "毎朝、仏壇を拝んでいる。", "まいあさ、ぶつだんをおがんでいる。", "I worship at the family altar every morning.", K4D4)
V("打者", "だしゃ", "Batter/hitter", "あの打者はホームランを打った。", "あのだしゃはホームランをうった。", "That batter hit a home run.", K4D4)
V("打つ", "うつ", "Strike/hit", "釘を金づちで打った。", "くぎをかなづちでうった。", "I hammered in a nail.", K4D4)
V("打ち合わせ", "うちあわせ", "Arrangement in advance", "明日の午後、打ち合わせがあります。", "あしたのごご、うちあわせがあります。", "There's a meeting tomorrow afternoon.", K4D4)
V("伺う", "うかがう", "Visit/ask (humble)", "明日、お宅に伺います。", "あした、おたくにうかがいます。", "I will visit your home tomorrow.", K4D4)
V("幸運", "こううんな", "Lucky", "幸運にも試験に合格した。", "こううんにもしけんにごうかくした。", "Luckily, I passed the exam.", K4D4)
V("不幸", "ふこうな", "Unhappy/unfortunate", "不幸な事故が起きてしまった。", "ふこうなじこがおきてしまった。", "An unfortunate accident occurred.", K4D4)
V("幸せ", "しあわせな", "Happy", "家族と一緒にいる時間が幸せだ。", "かぞくといっしょにいるじかんがしあわせだ。", "Time spent with my family makes me happy.", K4D4)
V("幸い", "さいわい", "Good fortune/fortunately", "幸い、けがはなかった。", "さいわい、けがはなかった。", "Fortunately, no one was injured.", K4D4)
V("失業", "しつぎょう", "Unemployment", "不況で失業する人が増えた。", "ふきょうでしつぎょうするひとがふえた。", "Unemployment increased due to the recession.", K4D4)
V("失う", "うしなう", "Lose", "事故で記憶を失った。", "じこできおくをうしなった。", "I lost my memory in the accident.", K4D4)
V("突然", "とつぜん", "Sudden", "突然、雨が降り出した。", "とつぜん、あめがふりだした。", "It suddenly started to rain.", K4D4)
V("突き当たり", "つきあたり", "End of the road", "この道の突き当たりを右に曲がってください。", "このみちのつきあたりをみぎにまがってください。", "Turn right at the end of this street.", K4D4)
V("煙突", "えんとつ", "Chimney", "古い家には煙突がある。", "ふるいいえにはえんとつがある。", "The old house has a chimney.", K4D4)
V("突っ込む", "つっこむ", "Thrust into/plunge", "車が店に突っ込んだ。", "くるまがみせにつっこんだ。", "A car crashed into the store.", K4D4)
V("全然", "ぜんぜん", "Not at all", "この問題は全然わからない。", "このもんだいはぜんぜんわからない。", "I don't understand this problem at all.", K4D4)
V("当然", "とうぜん", "Of course", "約束を守るのは当然のことだ。", "やくそくをまもるのはとうぜんのことだ。", "Keeping promises is only natural.", K4D4)
V("自然", "しぜん", "Nature/natural", "この町は自然が豊かだ。", "このまちはしぜんがゆたかだ。", "This town is rich in nature.", K4D4)
V("天然", "てんねん", "Natural/unartificial", "このジュースは天然の果物から作られている。", "このジュースはてんねんのくだものからつくられている。", "This juice is made from natural fruit.", K4D4)
V("諸般", "しょはん", "Variety/all sorts", "諸般の事情により中止となりました。", "しょはんのじじょうによりちゅうしとなりました。", "It was cancelled due to various circumstances.", K4D4)
V("諸問題", "しょもんだい", "Various problems", "環境の諸問題について話し合った。", "かんきょうのしょもんだいについてはなしあった。", "We discussed various environmental problems.", K4D4)
V("事情", "じじょう", "Circumstance", "家庭の事情で仕事を辞めた。", "かていのじじょうでしごとをやめた。", "I quit my job due to family circumstances.", K4D4)
V("表情", "ひょうじょう", "Facial expression", "彼女は暗い表情をしていた。", "かのじょはくらいひょうじょうをしていた。", "She had a gloomy expression.", K4D4)
V("友情", "ゆうじょう", "Friendship", "二人の友情は今も続いている。", "ふたりのゆうじょうはいまもつづいている。", "Their friendship continues to this day.", K4D4)
V("情け", "なさけ", "Sympathy/mercy", "彼は敵にも情けをかけた。", "かれはてきにもなさけをかけた。", "He showed mercy even to his enemy.", K4D4)
V("情けない", "なさけない", "Woeful/disgraceful", "自分の失敗が情けない。", "じぶんのしっぱいがなさけない。", "I'm disgusted with my own failure.", K4D4)
V("引退", "いんたい", "Retirement", "あの選手は来年引退するそうだ。", "あのせんしゅはらいねんいんたいするそうだ。", "I heard that player will retire next year.", K4D4)
V("退学", "たいがく", "Withdrawal from school", "彼は事情があって退学した。", "かれはじじょうがあってたいがくした。", "He withdrew from school due to circumstances.", K4D4)
V("退院", "たいいん", "Discharge from hospital", "来週、祖母が退院する予定だ。", "らいしゅう、そぼがたいいんするよていだ。", "My grandmother is scheduled to be discharged next week.", K4D4)
V("退く", "しりぞく", "Retreat/withdraw", "彼は社長の座を退いた。", "かれはしゃちょうのざをしりぞいた。", "He stepped down from the position of president.", K4D4)
V("退職", "たいしょく", "Retirement", "父は60歳で退職した。", "ちちは60さいでたいしょくした。", "My father retired at 60.", K4D4)
V("職業", "しょくぎょう", "Occupation/profession", "職業は何ですか。", "しょくぎょうはなんですか。", "What is your occupation?", K4D4)
V("職場", "しょくば", "Workplace", "新しい職場に慣れてきた。", "あたらしいしょくばになれてきた。", "I've gotten used to my new workplace.", K4D4)
V("職人", "しょくにん", "Artisan", "祖父は伝統工芸の職人だった。", "そふはでんとうこうげいのしょくにんだった。", "My grandfather was an artisan of traditional crafts.", K4D4)
V("紹介", "しょうかい", "Introduction", "友人に彼女を紹介した。", "ゆうじんにかのじょをしょうかいした。", "I introduced her to my friend.", K4D4)
V("介入", "かいにゅう", "Intervention", "政府がその問題に介入した。", "せいふがそのもんだいにかいにゅうした。", "The government intervened in that issue.", K4D4)
V("介護", "かいご", "Nursing care", "母の介護をしている。", "ははのかいごをしている。", "I'm taking care of my mother.", K4D4)

# --- Kanji Day 5: 答案用紙 ---
K4D5 = "kanji::w4 kanji::w4d5 jlpt::n2"
V("一次試験", "いちじしけん", "First examination", "一次試験に合格した。", "いちじしけんにごうかくした。", "I passed the first-round exam.", K4D5)
V("次第", "しだい", "Depending on circumstances", "結果は努力次第だ。", "けっかはどりょくしだいだ。", "The result depends on effort.", K4D5)
V("次", "つぎ", "Next", "次の駅で降りてください。", "つぎのえきでおりてください。", "Please get off at the next station.", K4D5)
V("文章", "ぶんしょう", "Sentence/composition", "この文章は意味がわかりにくい。", "このぶんしょうはいみがわかりにくい。", "This piece of writing is hard to understand.", K4D5)
V("章", "しょう", "Chapter", "この本の第三章を読んだ。", "このほんのだいさんしょうをよんだ。", "I read the third chapter of this book.", K4D5)
V("対する", "たいする", "Toward/against", "彼の意見に対する反論が多かった。", "かれのいけんにたいするはんろんがおおかった。", "There were many objections to his opinion.", K4D5)
V("反対", "はんたい", "Opposition/reverse", "計画に反対する人が多い。", "けいかくにはんたいするひとがおおい。", "Many people oppose the plan.", K4D5)
V("対照的", "たいしょうてきな", "Contrasting", "兄弟なのに二人の性格は対照的だ。", "きょうだいなのにふたりのせいかくはたいしょうてきだ。", "Despite being brothers, the two have contrasting personalities.", K4D5)
V("対", "つい", "Pair/couple", "この茶碗は対で使うものだ。", "このちゃわんはついでつかうものだ。", "These tea bowls are meant to be used as a pair.", K4D5)
V("最初", "さいしょ", "First/beginning", "最初に自己紹介をしてください。", "さいしょにじこしょうかいをしてください。", "Please introduce yourself first.", K4D5)
V("最後", "さいご", "Last/end", "最後まであきらめなかった。", "さいごまであきらめなかった。", "I didn't give up until the end.", K4D5)
V("最近", "さいきん", "Recently", "最近、忙しくて疲れている。", "さいきん、いそがしくてつかれている。", "I've been busy and tired recently.", K4D5)
V("最も", "もっとも", "Most", "これが最も重要な点だ。", "これがもっともじゅうようなてんだ。", "This is the most important point.", K4D5)
V("適当", "てきとうな", "Appropriate/reasonable", "適当な広さの部屋を探している。", "てきとうなひろさのへやをさがしている。", "I'm looking for a room of an appropriate size.", K4D5)
V("適切", "てきせつな", "Appropriate/proper", "適切な処置をとる必要がある。", "てきせつなしょちをとるひつようがある。", "Appropriate measures need to be taken.", K4D5)
V("適する", "てきする", "Suit/be fit for", "この土地は農業に適している。", "このとちはのうぎょうにてきしている。", "This land is suited for agriculture.", K4D5)
V("適度", "てきどな", "Moderate", "適度な運動は体にいい。", "てきどなうんどうはからだにいい。", "Moderate exercise is good for the body.", K4D5)
V("誤解", "ごかい", "Misunderstanding", "彼の言葉を誤解してしまった。", "かれのことばをごかいしてしまった。", "I misunderstood his words.", K4D5)
V("誤り", "あやまり", "Mistake", "文章の誤りを直した。", "ぶんしょうのあやまりをなおした。", "I corrected the mistakes in the text.", K4D5)
V("直線", "ちょくせん", "Straight line", "定規で直線を引いた。", "じょうぎでちょくせんをひいた。", "I drew a straight line with a ruler.", K4D5)
V("正直", "しょうじきな", "Honest", "正直な人はみんなに信頼される。", "しょうじきなひとはみんなにしんらいされる。", "Honest people are trusted by everyone.", K4D5)
V("素直", "すなおな", "Obedient/submissive", "子どもは素直に謝った。", "こどもはすなおにあやまった。", "The child apologized obediently.", K4D5)
V("直す", "なおす", "Fix", "壊れた時計を直した。", "こわれたとけいをなおした。", "I fixed the broken clock.", K4D5)
V("直ちに", "ただちに", "Immediately", "危険な場合は直ちに避難してください。", "きけんなばあいはただちにひなんしてください。", "In case of danger, evacuate immediately.", K4D5)
V("例", "れい", "Example", "具体的な例を挙げて説明した。", "ぐたいてきなれいをあげてせつめいした。", "I explained by giving a concrete example.", K4D5)
V("例外", "れいがい", "Exception", "このルールに例外はない。", "このルールにれいがいはない。", "There is no exception to this rule.", K4D5)
V("実例", "じつれい", "Example/instance", "実例を示しながら説明する。", "じつれいをしめしながらせつめいする。", "I explain while showing real examples.", K4D5)
V("例えば", "たとえば", "For example", "例えば、りんごやみかんが好きだ。", "たとえば、りんごやみかんがすきだ。", "For example, I like apples and mandarins.", K4D5)
V("例える", "たとえる", "Compare/liken", "人生をよく旅に例える。", "じんせいをよくたびにたとえる。", "Life is often compared to a journey.", K4D5)
V("名詞", "めいし", "Noun", "この文の名詞に丸をつけてください。", "このぶんのめいしにまるをつけてください。", "Please circle the nouns in this sentence.", K4D5)
V("動詞", "どうし", "Verb", "動詞の活用を覚える。", "どうしのかつようをおぼえる。", "I memorize verb conjugations.", K4D5)
V("自動詞", "じどうし", "Intransitive verb", "「開く」は自動詞だ。", "「ひらく」はじどうしだ。", "「開く」 is an intransitive verb.", K4D5)
V("他動詞", "たどうし", "Transitive verb", "「開ける」は他動詞だ。", "「あける」はたどうしだ。", "「開ける」 is a transitive verb.", K4D5)
V("形容詞", "けいようし", "Adjective", "この文には形容詞が二つある。", "このぶんにはけいようしがふたつある。", "There are two adjectives in this sentence.", K4D5)
V("助詞", "じょし", "Particle", "日本語の助詞の使い方は難しい。", "にほんごのじょしのつかいかたはむずかしい。", "The usage of Japanese particles is difficult.", K4D5)
V("副詞", "ふくし", "Adverb", "「とても」は副詞だ。", "「とても」はふくしだ。", "「とても」 is an adverb.", K4D5)
V("形式", "けいしき", "Form/formality", "会議は形式的なものだった。", "かいぎはけいしきてきなものだった。", "The meeting was a mere formality.", K4D5)
V("図形", "ずけい", "Diagram", "数学の授業で図形の問題を解いた。", "すうがくのじゅぎょうでずけいのもんだいをといた。", "I solved a geometry problem in math class.", K4D5)
V("形", "かたち", "Shape/form", "この雲は星の形をしている。", "このくもはほしのかたちをしている。", "This cloud is shaped like a star.", K4D5)
V("人形", "にんぎょう", "Doll/puppet", "娘は人形で遊ぶのが好きだ。", "むすめはにんぎょうであそぶのがすきだ。", "My daughter likes playing with dolls.", K4D5)
V("救助", "きゅうじょ", "Rescue/help", "登山者が救助された。", "とざんしゃがきゅうじょされた。", "The mountain climber was rescued.", K4D5)
V("助手", "じょしゅ", "Assistant", "教授の助手として働いている。", "きょうじゅのじょしゅとしてはたらいている。", "I work as an assistant to the professor.", K4D5)
V("助かる", "たすかる", "Be saved/be helpful", "手伝ってもらえて助かった。", "てつだってもらえてたすかった。", "It was a big help to have you assist me.", K4D5)
V("助ける", "たすける", "Help", "溺れている人を助けた。", "おぼれているひとをたすけた。", "I helped a drowning person.", K4D5)
V("周囲", "しゅうい", "Perimeter/neighborhood", "湖の周囲を散歩した。", "みずうみのしゅういをさんぽした。", "I took a walk around the lake.", K4D5)
V("囲む", "かこむ", "Surround", "家の周りを塀が囲んでいる。", "いえのまわりをへいがかこんでいる。", "A wall surrounds the house.", K4D5)

# --- Kanji Day 6: 作文 ---
K4D6 = "kanji::w4 kanji::w4d6 jlpt::n2"
V("夢中", "むちゅう", "Be engrossed", "息子はゲームに夢中になっている。", "むすこはゲームにむちゅうになっている。", "My son is absorbed in the game.", K4D6)
V("夢", "ゆめ", "Dream", "昨夜、変な夢を見た。", "さくや、へんなゆめをみた。", "I had a strange dream last night.", K4D6)
V("専門", "せんもん", "Specialty", "彼の専門は経済学だ。", "かれのせんもんはけいざいがくだ。", "His specialty is economics.", K4D6)
V("専攻", "せんこう", "Major", "大学では歴史を専攻した。", "だいがくではれきしをせんこうした。", "I majored in history in college.", K4D6)
V("専用", "せんよう", "Exclusive use", "これは社員専用の駐車場だ。", "これはしゃいんせんようのちゅうしゃじょうだ。", "This is a parking lot exclusively for employees.", K4D6)
V("歴史", "れきし", "History", "この町には長い歴史がある。", "このまちにはながいれきしがある。", "This town has a long history.", K4D6)
V("区域", "くいき", "Area/zone", "この区域は立ち入り禁止だ。", "このくいきはたちいりきんしだ。", "This zone is off-limits.", K4D6)
V("地域", "ちいき", "Area/region", "この地域は雪が多い。", "このちいきはゆきがおおい。", "This region gets a lot of snow.", K4D6)
V("祭日", "さいじつ", "Holiday/festival day", "明日は祭日で学校が休みだ。", "あしたはさいじつでがっこうがやすみだ。", "Tomorrow is a holiday, so school is off.", K4D6)
V("お祭り", "おまつり", "Festival", "夏に町のお祭りに行った。", "なつにまちのおまつりにいった。", "I went to the town festival in summer.", K4D6)
V("検査", "けんさ", "Inspection/test", "病院で血液検査を受けた。", "びょういんでけつえきけんさをうけた。", "I had a blood test at the hospital.", K4D6)
V("審査", "しんさ", "Examination/judgement", "応募作品はこれから審査される。", "おうぼさくひんはこれからしんさされる。", "The entries will now be judged.", K4D6)
V("調査", "ちょうさ", "Investigation/inquiry", "事故の原因を調査している。", "じこのげんいんをちょうさしている。", "They are investigating the cause of the accident.", K4D6)
V("戦争", "せんそう", "War", "戦争のない世界を願う。", "せんそうのないせかいをねがう。", "I wish for a world without war.", K4D6)
V("大戦", "たいせん", "Major war", "祖父は第二次世界大戦を経験した。", "そふはだいにじせかいたいせんをけいけんした。", "My grandfather experienced World War II.", K4D6)
V("戦う", "たたかう", "Fight", "選手たちは最後まで戦った。", "せんしゅたちはさいごまでたたかった。", "The players fought until the end.", K4D6)
V("競争", "きょうそう", "Competition", "会社間の競争が激しい。", "かいしゃかんのきょうそうがはげしい。", "Competition among companies is fierce.", K4D6)
V("争う", "あらそう", "Fight/dispute", "兄弟が遺産をめぐって争った。", "きょうだいがいさんをめぐってあらそった。", "The siblings fought over the inheritance.", K4D6)
V("将来", "しょうらい", "Future", "将来は医者になりたい。", "しょうらいはいしゃになりたい。", "I want to become a doctor in the future.", K4D6)
V("将棋", "しょうぎ", "Shogi/Japanese chess", "祖父とよく将棋をした。", "そふとよくしょうぎをした。", "I often played shogi with my grandfather.", K4D6)
V("歩道橋", "ほどうきょう", "Footbridge", "歩道橋を渡って駅に行く。", "ほどうきょうをわたってえきにいく。", "I cross the pedestrian bridge to get to the station.", K4D6)
V("鉄橋", "てっきょう", "Railroad bridge", "電車が鉄橋を渡っていく。", "でんしゃがてっきょうをわたっていく。", "The train crosses the railroad bridge.", K4D6)
V("橋", "はし", "Bridge", "この橋を渡ると隣町に着く。", "このはしをわたるととなりまちにつく。", "Crossing this bridge takes you to the neighboring town.", K4D6)
V("架け橋", "かけはし", "Bridge/go-between", "彼は両国の架け橋となる存在だ。", "かれはりょうこくのかけはしとなるそんざいだ。", "He serves as a bridge between the two countries.", K4D6)
V("憎い", "にくい", "Detestable", "彼のずるいやり方が憎い。", "かれのずるいやりかたがにくい。", "I detest his sneaky way of doing things.", K4D6)
V("憎しみ", "にくしみ", "Hatred", "彼女の心には憎しみが残っていた。", "かのじょのこころにはにくしみがのこっていた。", "Hatred remained in her heart.", K4D6)
V("憎む", "にくむ", "Detest", "人を憎むのはつらいことだ。", "ひとをにくむのはつらいことだ。", "Hating someone is a painful thing.", K4D6)
V("憎らしい", "にくらしい", "Detestable", "あの態度は本当に憎らしい。", "あのたいどはほんとうににくらしい。", "That attitude is truly infuriating.", K4D6)
V("自殺", "じさつ", "Suicide", "そのニュースは自殺について報じた。", "そのニュースはじさつについてほうじた。", "The news reported on a suicide.", K4D6)
V("殺す", "ころす", "Kill", "虫を殺すのはかわいそうだ。", "むしをころすのはかわいそうだ。", "It's sad to kill an insect.", K4D6)
V("悲観", "ひかん", "Pessimism", "将来を悲観するのはやめよう。", "しょうらいをひかんするのはやめよう。", "Let's stop being pessimistic about the future.", K4D6)
V("悲しい", "かなしい", "Sad", "友人が引っ越すのは悲しい。", "ゆうじんがひっこすのはかなしい。", "It's sad that my friend is moving away.", K4D6)
V("悲しむ", "かなしむ", "Grieve/lament", "家族はペットの死を悲しんだ。", "かぞくはペットのしをかなしんだ。", "The family grieved the death of their pet.", K4D6)
V("恥", "はじ", "Shame/humiliation", "人前で転んで恥をかいた。", "ひとまえでころんではじをかいた。", "I fell in public and was embarrassed.", K4D6)
V("恥ずかしい", "はずかしい", "Ashamed/embarrassed", "間違えて恥ずかしい思いをした。", "まちがえてはずかしいおもいをした。", "I made a mistake and felt embarrassed.", K4D6)
V("感じる", "かんじる", "Feel", "秋の訪れを感じる。", "あきのおとずれをかんじる。", "I feel the arrival of autumn.", K4D6)
V("感心", "かんしんな", "Admirable", "彼の努力には感心する。", "かれのどりょくにはかんしんする。", "I'm impressed by his effort.", K4D6)
V("感情", "かんじょう", "Emotion", "感情を顔に出さないようにした。", "かんじょうをかおにださないようにした。", "I tried not to show my emotions on my face.", K4D6)
V("感動", "かんどう", "Emotion/inspiration", "映画に感動して泣いた。", "えいがにかんどうしてないた。", "I was moved by the movie and cried.", K4D6)
V("地球", "ちきゅう", "Earth", "地球は太陽の周りを回っている。", "ちきゅうはたいようのまわりをまわっている。", "The Earth revolves around the sun.", K4D6)
V("野球", "やきゅう", "Baseball", "週末は友人と野球を見に行く。", "しゅうまつはゆうじんとやきゅうをみにいく。", "I'm going to watch baseball with a friend this weekend.", K4D6)
V("電球", "でんきゅう", "Light bulb", "切れた電球を交換した。", "きれたでんきゅうをこうかんした。", "I replaced the burnt-out light bulb.", K4D6)
V("球", "たま", "Ball/sphere", "子どもが球を追いかけて遊んでいる。", "こどもがたまをおいかけてあそんでいる。", "The children are playing, chasing a ball.", K4D6)
V("平和", "へいわ", "Peace", "世界の平和を祈る。", "せかいのへいわをいのる。", "I pray for world peace.", K4D6)
V("和式", "わしき", "Japanese style", "このトイレは和式だ。", "このトイレはわしきだ。", "This toilet is Japanese-style.", K4D6)
V("愛", "あい", "Love", "親の愛は深い。", "おやのあいはふかい。", "A parent's love is deep.", K4D6)
V("愛情", "あいじょう", "Love/affection", "母親の愛情を感じる。", "ははおやのあいじょうをかんじる。", "I feel my mother's affection.", K4D6)
V("愛する", "あいする", "Love/care for", "彼は家族を心から愛している。", "かれはかぞくをこころからあいしている。", "He loves his family from the bottom of his heart.", K4D6)
V("仲", "なか", "Relations/terms", "二人はとても仲がいい。", "ふたりはとてもなかがいい。", "The two of them get along very well.", K4D6)
V("仲間", "なかま", "Friend/circle", "大学のサークルの仲間と旅行に行った。", "だいがくのサークルのなかまとりょこうにいった。", "I went on a trip with my friends from the college club.", K4D6)
V("改良", "かいりょう", "Improvement", "製品の改良を重ねている。", "せいひんのかいりょうをかさねている。", "We keep improving the product.", K4D6)
V("良い", "よい", "Good", "良い天気が続いている。", "よいてんきがつづいている。", "The good weather continues.", K4D6)

# --- Kanji Day 7: Extra Medical Kanji (問診票) ---
K4D7 = "kanji::w4 kanji::w4d7 jlpt::n2"
V("腹痛", "ふくつう", "Stomachache", "食べ過ぎて腹痛がする。", "たべすぎてふくつうがする。", "I ate too much and have a stomachache.", K4D7)
V("背中", "せなか", "Back", "背中が痛くて病院に行った。", "せなかがいたくてびょういんにいった。", "My back hurt, so I went to the hospital.", K4D7)
V("休息", "きゅうそく", "Rest", "十分な休息を取ることが大切だ。", "じゅうぶんなきゅうそくをとることがたいせつだ。", "It's important to get enough rest.", K4D7)
V("息", "いき", "Breath", "階段を上ると息が切れる。", "かいだんをのぼるといきがきれる。", "I get out of breath climbing stairs.", K4D7)
V("息子", "むすこ", "Son", "息子は今年大学に入った。", "むすこはことしだいがくにはいった。", "My son entered university this year.", K4D7)
V("ぜん息", "ぜんそく", "Asthma", "娘はぜん息の発作で入院した。", "むすめはぜんそくのほっさでにゅういんした。", "My daughter was hospitalized for an asthma attack.", K4D7)
V("高血圧", "こうけつあつ", "High blood pressure", "父は高血圧で薬を飲んでいる。", "ちちはこうけつあつでくすりをのんでいる。", "My father takes medicine for high blood pressure.", K4D7)
V("血", "ち", "Blood", "指を切って血が出た。", "ゆびをきってちがでた。", "I cut my finger and it bled.", K4D7)
V("圧力", "あつりょく", "Pressure", "仕事の圧力でストレスを感じる。", "しごとのあつりょくでストレスをかんじる。", "I feel stressed from the pressure at work.", K4D7)
V("心臓", "しんぞう", "Heart", "運動すると心臓がどきどきする。", "うんどうするとしんぞうがどきどきする。", "My heart pounds when I exercise.", K4D7)
V("内臓", "ないぞう", "Internal organs", "検査で内臓の状態を調べた。", "けんさでないぞうのじょうたいをしらべた。", "The exam checked the state of my internal organs.", K4D7)
V("血液", "けつえき", "Blood", "血液型はA型です。", "けつえきがたはエーがたです。", "My blood type is A.", K4D7)
V("耳鼻科", "じびか", "Otorhinology (ENT)", "鼻水がひどいので耳鼻科に行った。", "はなみずがひどいのでじびかにいった。", "My runny nose was bad, so I went to the ENT.", K4D7)
V("鼻", "はな", "Nose", "花粉症で鼻がかゆい。", "かふんしょうではながかゆい。", "My nose is itchy from hay fever.", K4D7)
V("鼻水", "はなみず", "Nasal mucous", "風邪をひいて鼻水が止まらない。", "かぜをひいてはなみずがとまらない。", "I caught a cold and my runny nose won't stop.", K4D7)
V("呼吸", "こきゅう", "Respiration", "深く呼吸をして落ち着いた。", "ふかくこきゅうをしておちついた。", "I took a deep breath and calmed down.", K4D7)
V("吸収", "きゅうしゅう", "Absorption", "この薬は体に早く吸収される。", "このくすりはからだにはやくきゅうしゅうされる。", "This medicine is absorbed quickly into the body.", K4D7)
V("吸う", "すう", "Breathe/inhale", "新鮮な空気を吸った。", "しんせんなくうきをすった。", "I breathed in the fresh air.", K4D7)
V("睡眠", "すいみん", "Sleep", "睡眠不足で頭が痛い。", "すいみんぶそくであたまがいたい。", "I have a headache from lack of sleep.", K4D7)
V("眠い", "ねむい", "Sleepy", "昨夜眠れなくて今日はとても眠い。", "さくやねむれなくてきょうはとてもねむい。", "I couldn't sleep last night, so I'm very sleepy today.", K4D7)
V("眠る", "ねむる", "Sleep", "赤ちゃんはよく眠っている。", "あかちゃんはよくねむっている。", "The baby is sleeping soundly.", K4D7)
V("居眠り", "いねむり", "Doze", "授業中に居眠りをしてしまった。", "じゅぎょうちゅうにいねむりをしてしまった。", "I dozed off during class.", K4D7)
V("食欲", "しょくよく", "Appetite", "夏バテで食欲がない。", "なつばてでしょくよくがない。", "I have no appetite due to summer heat fatigue.", K4D7)
V("欲張り", "よくばり", "Greed", "彼は欲張りで、いつも人の分まで欲しがる。", "かれはよくばりで、いつもひとのぶんまでほしがる。", "He is greedy and always wants other people's share too.", K4D7)
V("欲しい", "ほしい", "Want", "新しいパソコンが欲しい。", "あたらしいパソコンがほしい。", "I want a new computer.", K4D7)
V("疲れる", "つかれる", "Get tired/exhaust", "長時間働いて疲れた。", "ちょうじかんはたらいてつかれた。", "I got tired from working long hours.", K4D7)
V("胃", "い", "Stomach", "食べ過ぎて胃が痛い。", "たべすぎていがいたい。", "My stomach hurts from eating too much.", K4D7)
V("胃腸", "いちょう", "Stomach and intestines", "胃腸の調子が悪い。", "いちょうのちょうしがわるい。", "My stomach and intestines are in bad shape.", K4D7)
V("胸", "むね", "Chest/breast", "緊張して胸がどきどきした。", "きんちょうしてむねがどきどきした。", "I was nervous and my chest was pounding.", K4D7)

# --- Vocabulary Day 1: なんとか覚えよう！ ---
VOC4D1 = "vocabulary::w4 vocabulary::w4d1 jlpt::n2"
V("必ずしも～とは限らない", "かならずしも～とはかぎらない", "Not necessarily", "お金持ちが必ずしも幸せだとは限らない。", "おかねもちがかならずしもしあわせだとはかぎらない。", "Rich people are not necessarily happy.", VOC4D1)
V("必ず", "かならず", "Always/without fail", "明日は必ず9時に来てください。", "あしたはかならず9じにきてください。", "Please come at 9 o'clock tomorrow without fail.", VOC4D1)
V("いつか", "いつか", "Someday/sometime", "いつかまた京都へ行きたい。", "いつかまたきょうとへいきたい。", "I want to go to Kyoto again someday.", VOC4D1)
V("いつまでも", "いつまでも", "Forever/always", "この思い出はいつまでも忘れない。", "このおもいではいつまでもわすれない。", "I will never forget this memory.", VOC4D1)
V("いつのまにか", "いつのまにか", "Before one knows it/unawares", "ゲームに夢中になっていたら、いつのまにか朝になっていた。", "ゲームにむちゅうになっていたら、いつのまにかあさになっていた。", "I was absorbed in the game, and before I knew it, it was morning.", VOC4D1)
V("つい", "つい", "Without meaning to/unintentionally", "疲れていて、つい寝てしまった。", "つかれていて、ついねてしまった。", "I was tired and unintentionally fell asleep.", VOC4D1)
V("ついに", "ついに", "Finally/at last", "お金を貯めて、ついに欲しい車を手に入れた。", "おかねをためて、ついにほしいくるまをてにいれた。", "I saved money and finally got the car I wanted.", VOC4D1)
V("どうしても", "どうしても", "No matter what/simply not possible", "彼のあの態度はどうしても許せない。", "かれのあのたいどはどうしてもゆるせない。", "I simply cannot forgive that attitude of his.", VOC4D1)
V("どうも", "どうも", "Somehow/really", "どうも風邪をひいてしまったらしい。", "どうもかぜをひいてしまったらしい。", "It seems I've somehow caught a cold.", VOC4D1)
V("なんとか／どうにか", "なんとか／どうにか", "Somehow/manage to do", "このごみをなんとかしないと、座るところもない。", "このごみをなんとかしないと、すわるところもない。", "If we don't do something about this trash, there won't even be anywhere to sit.", VOC4D1)
V("なんとなく", "なんとなく", "Sort of/somehow", "なんとなく今日は嫌な予感がする。", "なんとなくきょうはいやなよかんがする。", "Somehow I have a bad feeling about today.", VOC4D1)
V("なんとも～ない", "なんとも～ない", "Not care about/think nothing of", "彼に何を言われてもなんとも思わない。", "かれになにをいわれてもなんともおもわない。", "I don't care no matter what he says to me.", VOC4D1)
V("もし（も）", "もし（も）", "If", "もし雨が降ったら、試合は中止です。", "もしあめがふったら、しあいはちゅうしです。", "If it rains, the game will be cancelled.", VOC4D1)
V("もしかしたら／もしかすると", "もしかしたら／もしかすると", "Perhaps/possibly/could be", "もしかしたら明日は雪が降るかもしれない。", "もしかしたらあしたはゆきがふるかもしれない。", "Perhaps it might snow tomorrow.", VOC4D1)
V("なるべく", "なるべく", "As much as possible/if you can", "なるべく早く返事をください。", "なるべくはやくへんじをください。", "Please reply as soon as possible.", VOC4D1)
V("なるほど", "なるほど", "I see/certainly/indeed", "「なるほど、そういうことか」と彼は言った。", "「なるほど、そういうことか」とかれはいった。", "\"I see, so that's how it is,\" he said.", VOC4D1)
V("確か", "たしか", "Probably/I think/if I remember correctly", "確か、彼女は結婚したはずだけど……。", "たしか、かのじょはけっこんしたはずだけど……。", "If I remember correctly, she should be married...", VOC4D1)
V("確かに", "たしかに", "Definitely/certainly/surely", "確かに私は、昨日、5時まで会社にいました。", "たしかにわたしは、きのう、5じまでかいしゃにいました。", "I was definitely at the office until 5 yesterday.", VOC4D1)

# --- Vocabulary Day 2: いずれ覚えられる！ ---
VOC4D2 = "vocabulary::w4 vocabulary::w4d2 jlpt::n2"
V("まもなく", "まもなく", "Soon/shortly after", "電車はまもなく到着します。", "でんしゃはまもなくとうちゃくします。", "The train will arrive shortly.", VOC4D2)
V("近々", "ちかぢか", "Sometime soon/in the near future", "近々、引っ越す予定だ。", "ちかぢか、ひっこすよていだ。", "I plan to move sometime soon.", VOC4D2)
V("そのうち", "そのうち", "Someday/before long", "そのうち慣れるだろう。", "そのうちなれるだろう。", "I'll get used to it before long.", VOC4D2)
V("やがて", "やがて", "Soon/eventually", "やがて桜の季節がやってくる。", "やがてさくらのきせつがやってくる。", "The cherry blossom season will soon arrive.", VOC4D2)
V("ようやく", "ようやく", "Finally/at last", "長い梅雨がようやく終わった。", "ながいつゆがようやくおわった。", "The long rainy season finally ended.", VOC4D2)
V("いずれ", "いずれ", "Eventually/someday", "いずれ本当のことがわかるだろう。", "いずれほんとうのことがわかるだろう。", "Eventually the truth will be known.", VOC4D2)
V("たちまち", "たちまち", "Immediately/instantly", "そのうわさはたちまち広がった。", "そのうわさはたちまちひろがった。", "That rumor spread instantly.", VOC4D2)
V("ただちに", "ただちに", "Right away/immediately", "危険を感じたらただちに逃げてください。", "きけんをかんじたらただちににげてください。", "If you sense danger, flee immediately.", VOC4D2)
V("にわかに", "にわかに", "Suddenly/abruptly", "空がにわかに暗くなった。", "そらがにわかにくらくなった。", "The sky suddenly turned dark.", VOC4D2)
V("絶えず", "たえず", "Constantly", "その家からは絶えず笑い声が聞こえてくる。", "そのいえからはたえずわらいごえがきこえてくる。", "Laughter is constantly heard from that house.", VOC4D2)
V("つねに", "つねに", "Always", "彼はつねに冷静な判断をする。", "かれはつねにれいせいなはんだんをする。", "He always makes calm judgments.", VOC4D2)
V("しきりに", "しきりに", "Repeatedly/frequently", "子どもがしきりに公園に行きたがっている。", "こどもがしきりにこうえんにいきたがっている。", "The child keeps repeatedly asking to go to the park.", VOC4D2)
V("しょっちゅう", "しょっちゅう", "Often/frequently", "彼はしょっちゅう遅刻する。", "かれはしょっちゅうちこくする。", "He is often late.", VOC4D2)
V("（もう）すでに", "（もう）すでに", "Already", "映画はもうすでに始まっていた。", "えいがはもうすでにはじまっていた。", "The movie had already started.", VOC4D2)
V("とっくに", "とっくに", "Long ago/already", "申し込みの期限はとっくに過ぎてしまった。", "もうしこみのきげんはとっくにすぎてしまった。", "The application deadline passed long ago.", VOC4D2)
V("前もって", "まえもって", "In advance", "前もって予約しておいた。", "まえもってよやくしておいた。", "I made a reservation in advance.", VOC4D2)
V("ほぼ", "ほぼ", "Approximately/almost", "建物はほぼ完成した。", "たてものはほぼかんせいした。", "The building is almost complete.", VOC4D2)
V("お（お）よそ", "お（お）よそ", "Approximately/roughly", "会場にはおよそ300人が集まった。", "かいじょうにはおよそ300にんがあつまった。", "Roughly 300 people gathered at the venue.", VOC4D2)
V("ほんの", "ほんの", "A tiny bit/just", "ほんの少しだけ味見をした。", "ほんのすこしだけあじみをした。", "I tasted just a tiny bit.", VOC4D2)
V("たった", "たった", "Only/merely", "その子はたった一人でこんなに遠くまで来た。", "そのこはたったひとりでこんなにとおくまできた。", "That child came this far all alone.", VOC4D2)
V("せいぜい", "せいぜい", "At most/only about", "このイベントに参加するのはせいぜい20人だろう。", "このイベントにさんかするのはせいぜい20にんだろう。", "At most, only about 20 people will join this event.", VOC4D2)
V("少なくとも", "すくなくとも", "At least", "少なくとも一週間は休みが必要だ。", "すくなくともいっしゅうかんはやすみがひつようだ。", "I need at least a week off.", VOC4D2)
V("せめて", "せめて", "At least/if only", "せめて70点は取りたいなあ。", "せめて70てんはとりたいなあ。", "I want to get at least 70 points.", VOC4D2)

# --- Vocabulary Day 3: せっせと覚えよう！ ---
VOC4D3 = "vocabulary::w4 vocabulary::w4d3 jlpt::n2"
V("たびたび／しばしば", "たびたび／しばしば", "Frequently/many times", "このパソコンはしばしばフリーズする。", "このパソコンはしばしばフリーズする。", "This computer often freezes.", VOC4D3)
V("いよいよ", "いよいよ", "Finally/at last", "いよいよ試合の日がやってきた。", "いよいよしあいのひがやってきた。", "The day of the match has finally arrived.", VOC4D3)
V("いちいち", "いちいち", "One by one/every single thing", "いちいち文句を言わないでください。", "いちいちもんくをいわないでください。", "Please don't complain about every little thing.", VOC4D3)
V("ふわふわ（する）", "ふわふわ（する）", "Soft/floating", "新しい枕はふわふわしていて気持ちいい。", "あたらしいまくらはふわふわしていてきもちいい。", "The new pillow is soft and fluffy and feels nice.", VOC4D3)
V("まごまご（する）", "まごまご（する）", "Be at a loss/confused", "道に迷ってまごまごしてしまった。", "みちにまよってまごまごしてしまった。", "I got lost and was at a loss what to do.", VOC4D3)
V("それぞれ／めいめい／ひとりひとり／各々", "それぞれ／めいめい／ひとりひとり／おのおの", "Each/respectively", "学生はそれぞれ好きなテーマを選んだ。", "がくせいはそれぞれすきなテーマをえらんだ。", "Each student chose their own favorite theme.", VOC4D3)
V("ばったり", "ばったり", "Bump into (someone) unexpectedly", "駅で昔の同僚にばったり会った。", "えきでむかしのどうりょうにばったりあった。", "I unexpectedly ran into an old coworker at the station.", VOC4D3)
V("こっそり", "こっそり", "Secretly/sneaking", "おなかがすいたので夜中にこっそりお菓子を食べてしまった。", "おなかがすいたのでよなかにこっそりおかしをたべてしまった。", "I was hungry, so I secretly ate snacks in the middle of the night.", VOC4D3)
V("ぴったり", "ぴったり", "Exactly/tightly", "手と手をぴったり合わせる。", "てとてをぴったりあわせる。", "Press your hands together exactly.", VOC4D3)
V("ぎっしり", "ぎっしり", "Tightly packed/cramped", "本棚に本がぎっしり詰まっている。", "ほんだなにほんがぎっしりつまっている。", "The bookshelf is packed tightly with books.", VOC4D3)
V("じっくり", "じっくり", "Slowly and carefully", "じっくり考えて結論を出そう。", "じっくりかんがえてけつろんをだそう。", "Let's think it over carefully and reach a conclusion.", VOC4D3)
V("ちらっと／ちらりと", "ちらっと／ちらりと", "At a glance", "彼は時計をちらっと見た。", "かれはとけいをちらっとみた。", "He glanced at the clock.", VOC4D3)
V("うんざり（する）", "うんざり（する）", "Get fed up with/disgusted", "毎日こんなに暑くて、本当にうんざりする。", "まいにちこんなにあつくて、ほんとうにうんざりする。", "It's so hot every day, I'm really fed up.", VOC4D3)
V("びっしょり／びしょびしょ", "びっしょり／びしょびしょ", "Soaked/drenched", "突然の雨で服がびっしょりぬれた。", "とつぜんのあめでふくがびっしょりぬれた。", "My clothes got completely soaked in the sudden rain.", VOC4D3)
V("しいんと（する）／シーンと（する）", "しいんと（する）／シーンと（する）", "Fall silent/quiet", "先生が入ってくると教室がしいんとなった。", "せんせいがはいってくるときょうしつがしいんとなった。", "The classroom fell silent when the teacher came in.", VOC4D3)
V("ずらりと／ずらっと", "ずらりと／ずらっと", "Lined up", "店の前に人がずらりと並んでいる。", "みせのまえにひとがずらりとならんでいる。", "People are lined up in a row in front of the store.", VOC4D3)
V("さっさと", "さっさと", "At once/quickly", "宿題をさっさと終わらせよう。", "しゅくだいをさっさとおわらせよう。", "Let's finish the homework quickly.", VOC4D3)
V("せっせと", "せっせと", "Diligently/steadily", "妻と子どものためにせっせと働く。", "つまとこどものためにせっせとはたらく。", "I work diligently for my wife and children.", VOC4D3)
V("どっと", "どっと", "Pouring in/all of a sudden", "家に着いたらどっと疲れが出た。", "いえについたらどっとつかれがでた。", "Once I got home, exhaustion hit me all at once.", VOC4D3)
V("すっと（する）", "すっと（する）", "Abruptly/feel refreshed", "悩みを話したら気持ちがすっとした。", "なやみをはなしたらきもちがすっとした。", "Talking about my worries made me feel refreshed.", VOC4D3)
V("ひとりでに", "ひとりでに", "By itself/automatically", "ドアがひとりでに開いた。", "ドアがひとりでにひらいた。", "The door opened by itself.", VOC4D3)
V("いっせいに", "いっせいに", "Simultaneously/all at once", "桜がいっせいに開花した。", "さくらがいっせいにかいかした。", "The cherry blossoms all bloomed at once.", VOC4D3)

# --- Vocabulary Day 4: さらに覚えよう！ ---
VOC4D4 = "vocabulary::w4 vocabulary::w4d4 jlpt::n2"
V("相当／かなり", "そうとう／かなり", "Very/considerably", "改良されたソフトは前よりかなり使いやすい。", "かいりょうされたソフトはまえよりかなりつかいやすい。", "The improved software is considerably easier to use than before.", VOC4D4)
V("大いに", "おおいに", "Highly/greatly/very much", "今夜のパーティーは大いに楽しもう。", "こんやのパーティーはおおいにたのしもう。", "Let's greatly enjoy tonight's party.", VOC4D4)
V("うんと", "うんと", "A lot/extremely", "ごはんをうんと食べて早く大きくなってね。", "ごはんをうんとたべてはやくおおきくなってね。", "Eat a lot of rice and grow up quickly.", VOC4D4)
V("たっぷり", "たっぷり", "Ample/fully", "休みの日は睡眠をたっぷり取る。", "やすみのひはすいみんをたっぷりとる。", "I get plenty of sleep on my days off.", VOC4D4)
V("あまりにも", "あまりにも", "Too much/excessively", "あの政治家の発言はあまりにも無責任だ。", "あのせいじかのはつげんはあまりにもむせきにんだ。", "That politician's remarks are far too irresponsible.", VOC4D4)
V("やや", "やや", "A little/somewhat", "今日は昨日よりやや涼しい。", "きょうはきのうよりややすずしい。", "Today is a bit cooler than yesterday.", VOC4D4)
V("多少", "たしょう", "Somewhat/a little", "多少の失敗は気にしないほうがいい。", "たしょうのしっぱいはきにしないほうがいい。", "It's better not to worry about minor failures.", VOC4D4)
V("いくぶん／いくらか", "いくぶん／いくらか", "A little/to some extent", "痛みはさっきよりいくらかましになった。", "いたみはさっきよりいくらかましになった。", "The pain is somewhat better than before.", VOC4D4)
V("わりに／わりと／割合（に）", "わりに／わりと／わりあいに", "Relatively/unexpectedly", "今日のテストはわりと簡単だった。", "きょうのテストはわりとかんたんだった。", "Today's test was relatively easy.", VOC4D4)
V("なお（いっそう）", "なお（いっそう）", "Even more/furthermore", "今後もなお一層努力していきたい。", "こんごもなおいっそうどりょくしていきたい。", "I want to make even more effort going forward.", VOC4D4)
V("より（いっそう）", "より（いっそう）", "Much more", "より一層の努力が必要だ。", "よりいっそうのどりょくがひつようだ。", "Even greater effort is necessary.", VOC4D4)
V("むしろ", "むしろ", "Rather/preferably", "忙しいというより、むしろ暇なほうだ。", "いそがしいというより、むしろひまなほうだ。", "Rather than busy, I'm actually more on the free side.", VOC4D4)
V("余計（に）", "よけいに", "Excessively/rather (more)", "心配すると余計に眠れなくなる。", "しんぱいするとよけいにねむれなくなる。", "Worrying makes it even harder to sleep.", VOC4D4)
V("じょじょに", "じょじょに", "Gradually/little by little", "体調はじょじょに回復している。", "たいちょうはじょじょにかいふくしている。", "My health is gradually recovering.", VOC4D4)
V("次第に", "しだいに", "Gradually", "空が次第に明るくなってきた。", "そらがしだいにあかるくなってきた。", "The sky gradually got brighter.", VOC4D4)
V("さらに", "さらに", "Furthermore/even more", "国の借金は前年よりさらに増えた。", "くにのしゃっきんはぜんねんよりさらにふえた。", "The national debt increased even further compared to the previous year.", VOC4D4)
V("一段と", "いちだんと", "Much more/a lot", "最近の女性は一段と強くなったと言われている。", "さいきんのじょせいはいちだんとつよくなったといわれている。", "It's said that women recently have become even stronger.", VOC4D4)
V("ぐっと", "ぐっと", "Significantly/much (better)", "塩を入れたら味がぐっとよくなった。", "しおをいれたらあじがぐっとよくなった。", "Adding salt made the taste much better.", VOC4D4)
V("めっきり", "めっきり", "Noticeably/remarkably", "彼女からのメールがめっきり減ってしまった。", "かのじょからのメールがめっきりへってしまった。", "Emails from her have noticeably decreased.", VOC4D4)
V("主に", "おもに", "Mainly", "この店では主に日本の野菜を売っている。", "このみせではおもににほんのやさいをうっている。", "This store mainly sells Japanese vegetables.", VOC4D4)
V("くれぐれも", "くれぐれも", "Earnestly/repeatedly", "くれぐれもお体に気をつけてください。", "くれぐれもおからだにきをつけてください。", "Please take good care of your health.", VOC4D4)
V("一応", "いちおう", "More or less/tentatively", "一応、計画は立てておいた。", "いちおう、けいかくはたてておいた。", "I made a plan, just in case.", VOC4D4)
V("一般に", "いっぱんに", "Generally", "一般に、夏は電気代が高くなる。", "いっぱんに、なつはでんきだいがたかくなる。", "Generally, electricity bills go up in summer.", VOC4D4)
V("明らかに", "あきらかに", "Obviously/clearly", "これは明らかに彼のミスだ。", "これはあきらかにかれのミスだ。", "This is clearly his mistake.", VOC4D4)

# --- Vocabulary Day 5: 取りあえず覚えよう！ ---
VOC4D5 = "vocabulary::w4 vocabulary::w4d5 jlpt::n2"
V("いわば", "いわば", "So to speak/as it were", "年賀状はいわば、クリスマスカードのようなものです。", "ねんがじょうはいわば、クリスマスカードのようなものです。", "New Year's cards are, so to speak, like Christmas cards.", VOC4D5)
V("いわゆる", "いわゆる", "So-called", "彼はいわゆる天才タイプだ。", "かれはいわゆるてんさいタイプだ。", "He's what you'd call a genius type.", VOC4D5)
V("まさか", "まさか", "Never/by no means", "まさか彼が犯人だとは思わなかった。", "まさかかれがはんにんだとはおもわなかった。", "I never imagined he was the culprit.", VOC4D5)
V("まさに", "まさに", "Exactly/surely/just now", "こんなにうすく皮をむくとは、まさにプロですね。", "こんなにうすくかわをむくとは、まさにプロですね。", "Peeling this thin - you're truly a professional.", VOC4D5)
V("一度に／いっぺんに", "いちどに／いっぺんに", "All at once/at one time", "質問を一度にしないでください。", "しつもんをいちどにしないでください。", "Please don't ask questions all at once.", VOC4D5)
V("一気に", "いっきに", "In one breath/at a stroke", "レポートを一気に書き上げた。", "レポートをいっきにかきあげた。", "I wrote the whole report in one go.", VOC4D5)
V("思い切り", "おもいきり", "With all one's might/to one's heart's content", "休みの日は思い切り遊びたい。", "やすみのひはおもいきりあそびたい。", "I want to play to my heart's content on my day off.", VOC4D5)
V("思い切って", "おもいきって", "Boldly/daringly", "思い切ってマンションを買った。", "おもいきってマンションをかった。", "I boldly decided to buy a condo.", VOC4D5)
V("思わず", "おもわず", "Unintentionally/instinctively", "面白くて思わず笑ってしまった。", "おもしろくておもわずわらってしまった。", "It was so funny I laughed without meaning to.", VOC4D5)
V("思いがけず／思いがけなく", "おもいがけず／おもいがけなく", "Unexpectedly", "思いがけず古い友人に再会した。", "おもいがけずふるいゆうじんにさいかいした。", "I unexpectedly reunited with an old friend.", VOC4D5)
V("なにしろ／とにかく", "なにしろ／とにかく", "At any rate/anyhow", "なにしろ時間がないので急ぎましょう。", "なにしろじかんがないのでいそぎましょう。", "Anyhow, there's no time, so let's hurry.", VOC4D5)
V("なにかと", "なにかと", "One way or another/with this and that", "引っ越しはなにかと物入りだ。", "ひっこしはなにかとものいりだ。", "Moving costs money one way or another.", VOC4D5)
V("相変わらず", "あいかわらず", "As ever/as usual", "この店は相変わらず客の入りが悪い。", "このみせはあいかわらずきゃくのいりがわるい。", "This shop still has poor customer traffic, as usual.", VOC4D5)
V("取りあえず", "とりあえず", "For the time being/first of all", "取りあえずお茶でも飲みましょう。", "とりあえずおちゃでものみましょう。", "Let's have some tea for now, first of all.", VOC4D5)
V("わざと", "わざと", "Intentionally/on purpose", "彼はわざと知らないふりをした。", "かれはわざとしらないふりをした。", "He pretended not to know on purpose.", VOC4D5)
V("わざわざ", "わざわざ", "Taking the trouble to do/expressly", "わざわざ空港まで迎えに来てくれた。", "わざわざくうこうまでむかえにきてくれた。", "They took the trouble to come pick me up at the airport.", VOC4D5)
V("いっそう", "いっそう", "Much more/still more", "カレーにチーズを入れたらいっそうおいしくなりました。", "カレーにチーズをいれたらいっそうおいしくなりました。", "Adding cheese to the curry made it even more delicious.", VOC4D5)
V("いっそ", "いっそ", "Rather/preferably", "こんなに苦労するなら、いっそ辞めてしまいたい。", "こんなにくろうするなら、いっそやめてしまいたい。", "If it's this much trouble, I'd rather just quit.", VOC4D5)
V("今に", "いまに", "Before long/eventually", "今に彼も後悔するだろう。", "いまにかれもこうかいするだろう。", "He'll regret it eventually.", VOC4D5)
V("今にも", "いまにも", "At any moment", "その子どもは今にも泣き出しそうだ。", "そのこどもはいまにもなきだしそうだ。", "That child looks like they're about to cry any moment.", VOC4D5)
V("今さら", "いまさら", "Now/at this late hour", "今さらやめるわけにはいかない。", "いまさらやめるわけにはいかない。", "At this point, I can't just quit.", VOC4D5)
V("未だに", "いまだに", "Still/even now", "彼は未だに独身だ。", "かれはいまだにどくしんだ。", "He is still single even now.", VOC4D5)
V("ただ今", "ただいま", "Right now/presently", "ただ今、担当者が参ります。", "ただいま、たんとうしゃがまいります。", "The person in charge will be with you right now.", VOC4D5)
V("たった今", "たったいま", "Just now", "たった今、駅に着いたところです。", "たったいま、えきについたところです。", "I just arrived at the station.", VOC4D5)

# --- Vocabulary Day 6: いったん覚えたら忘れない！ ---
VOC4D6 = "vocabulary::w4 vocabulary::w4d6 jlpt::n2"
V("別に～ない", "べつに～ない", "Not particularly", "別に不満はない。", "べつにふまんはない。", "I have no particular complaints.", VOC4D6)
V("そう～ない", "そう～ない", "Not so much/not that", "比較するとそう差はなかった。", "ひかくするとそうさはなかった。", "When compared, there wasn't that much of a difference.", VOC4D6)
V("大して～ない", "たいして～ない", "Not much/not very", "今日のテストは大して難しくなかった。", "きょうのテストはたいしてむずかしくなかった。", "Today's test wasn't very difficult.", VOC4D6)
V("一切～ない", "いっさい～ない", "Absolutely not/none at all", "彼はその件について一切話さなかった。", "かれはそのけんについていっさいはなさなかった。", "He didn't talk about that matter at all.", VOC4D6)
V("とても～ない", "とても～ない", "Hardly/by no means", "私のピアノは下手なのでとても人の前では演奏できません。", "わたしのピアノはへたなのでとてもひとのまえではえんそうできません。", "My piano playing is so bad that I simply cannot perform in front of people.", VOC4D6)
V("おそらく～だろう", "おそらく～だろう", "Probably", "30年後の自動車はおそらくすべて電動になっているだろう。", "30ねんごのじどうしゃはおそらくすべてでんどうになっているだろう。", "Cars 30 years from now will probably all be electric.", VOC4D6)
V("どうやら～そうだ／ようだ", "どうやら～そうだ／ようだ", "Seemingly/it looks like", "どうやら道に迷ったようだ。", "どうやらみちにまよったようだ。", "It looks like we've gotten lost.", VOC4D6)
V("果たして～だろうか", "はたして～だろうか", "Really?/is it true that?", "この計画は果たして成功するだろうか。", "このけいかくははたしてせいこうするだろうか。", "Will this plan really succeed?", VOC4D6)
V("どうせ～だろう", "どうせ～だろう", "Anyway/anyhow", "どうせ失敗するだろうとみんなが思っていた。", "どうせしっぱいするだろうとみんながおもっていた。", "Everyone thought it would probably fail anyway.", VOC4D6)
V("せっかく～のに／から", "せっかく～のに／から", "Despite taking the trouble to", "せっかく作ったのに、誰も食べてくれなかった。", "せっかくつくったのに、だれもたべてくれなかった。", "Despite the trouble I went to make it, nobody ate it.", VOC4D6)
V("いったん／一度／ひとたび～したら", "いったん／いちど／ひとたび～したら", "Once (you do something)", "いったん始めたら最後までやり通す。", "いったんはじめたらさいごまでやりとおす。", "Once I start, I see it through to the end.", VOC4D6)
V("いったん／ひとまず", "いったん／ひとまず", "For now/for the time being", "これでひとまず安心です。", "これでひとまずあんしんです。", "This puts my mind at ease for now.", VOC4D6)
V("かえって", "かえって", "On the contrary/rather", "薬を飲んだら、かえって具合が悪くなった。", "くすりをのんだら、かえってぐあいがわるくなった。", "Taking the medicine actually made me feel worse.", VOC4D6)
V("さっそく", "さっそく", "Immediately/right away", "もらったケーキをさっそく食べた。", "もらったケーキをさっそくたべた。", "I ate the cake I received right away.", VOC4D6)
V("さすが（に）", "さすが（に）", "As expected/truly", "さすがにプロは仕事が速い。", "さすがにプロはしごとがはやい。", "As expected of a professional, the work is fast.", VOC4D6)
V("あいにく", "あいにく", "Unfortunately", "ハイキングへ行くつもりだったがあいにく雨が降ってしまった。", "ハイキングへいくつもりだったがあいにくあめがふってしまった。", "I was planning to go hiking, but unfortunately it rained.", VOC4D6)
V("あくまで（も）", "あくまで（も）", "To the bitter end/persistently", "彼はあくまでも自分の意見を主張した。", "かれはあくまでもじぶんのいけんをしゅちょうした。", "He persistently asserted his own opinion to the end.", VOC4D6)
V("なんだか／なんとなく／なぜか", "なんだか／なんとなく／なぜか", "For some reason/somewhat", "今日はなんだか蒸し暑い。", "きょうはなんだかむしあつい。", "Today is somehow muggy.", VOC4D6)
V("なんと／なんて", "なんと／なんて", "What a/how", "なんときれいな景色だろう。", "なんときれいなけしきだろう。", "What a beautiful view!", VOC4D6)

# --- Reading extraction (annotated/glossary vocabulary from reading-w4.md passages) ---
R4D1 = "reading::w4 reading::w4d1 jlpt::n2"
V("必要にせまられて", "ひつようにせまられて", "Out of necessity/impelled by necessity", "必要にせまられて、資格の勉強を始めた。", "ひつようにせまられて、しかくのべんきょうをはじめた。", "Out of necessity, I started studying for a certification.", R4D1)
V("仕事がらみ", "しごとがらみ", "Work-related", "最近、仕事がらみの飲み会が多い。", "さいきん、しごとがらみののみかいがおおい。", "Recently there have been a lot of work-related drinking parties.", R4D1)

R4D2 = "reading::w4 reading::w4d2 jlpt::n2"
V("言い伝え", "いいつたえ", "A tradition/legend", "この村には昔からの言い伝えがある。", "このむらにはむかしからのいいつたえがある。", "This village has a tradition passed down from long ago.", R4D2)
V("唱える", "となえる", "To chant/recite", "くしゃみをしたときに「くさめくさめ」と唱える。", "くしゃみをしたときに「くさめくさめ」ととなえる。", "When you sneeze, you chant \"kusame kusame.\"", R4D2)

R4D3 = "reading::w4 reading::w4d3 jlpt::n2"
V("振り込み", "ふりこみ", "A transfer", "同じ銀行間の振り込みは無料だった。", "おなじぎんこうかんのふりこみはむりょうだった。", "Transfers between the same bank used to be free.", R4D3)
V("残高", "ざんだか", "A bank balance", "通帳の残高を確認した。", "つうちょうのざんだかをかくにんした。", "I checked the balance in my bankbook.", R4D3)

R4D4 = "reading::w4 reading::w4d4 jlpt::n2"
V("美術部", "びじゅつぶ", "Art club", "姉は高校で美術部に入っていた。", "あねはこうこうでびじゅつぶにはいっていた。", "My older sister was in the art club in high school.", R4D4)
V("手作り", "てづくり", "Hand-made", "これは母が作った手作りのケーキです。", "これははははつくったてづくりのケーキです。", "This is a hand-made cake my mother made.", R4D4)
V("吸いがら", "すいがら", "A cigarette butt", "道に吸いがらを捨ててはいけない。", "みちにすいがらをすててはいけない。", "You must not throw cigarette butts on the street.", R4D4)

R4D5 = "reading::w4 reading::w4d5 jlpt::n2"
V("乗り合い自動車", "のりあいじどうしゃ", "Bus (old term)", "昔は乗り合い自動車と呼ばれていた乗り物が、今のバスだ。", "むかしはのりあいじどうしゃとよばれていたのりものが、いまのバスだ。", "What used to be called a \"noriai jidousha\" is today's bus.", R4D5)

R4D6 = "reading::w4 reading::w4d6 jlpt::n2"
V("銀河", "ぎんが", "A galaxy", "夜空に美しい銀河が見えた。", "よぞらにうつくしいぎんががみえた。", "A beautiful galaxy could be seen in the night sky.", R4D6)

R4D7 = "reading::w4 reading::w4d7 jlpt::n2"
V("人並みに", "ひとなみに", "Like an ordinary person, same as others", "彼も人並みに恋愛や結婚について悩んでいる。", "かれもひとなみにれんあいやけっこんについてなやんでいる。", "He too worries about love and marriage, just like everyone else.", R4D7)
V("身が入らない", "みがはいらない", "Cannot concentrate/focus", "悩みがあると、仕事に身が入らない。", "なやみがあると、しごとにみがはいらない。", "When I have worries, I can't focus on my work.", R4D7)
V("打ち砕く", "うちくだく", "To smash/shatter", "その知らせは彼の希望を打ち砕いた。", "そのしらせはかれのきぼうをうちくだいた。", "That news shattered his hopes.", R4D7)
V("喫煙車両", "きつえんしゃりょう", "Smoking car/carriage", "昔の新幹線には喫煙車両があった。", "むかしのしんかんせんにはきつえんしゃりょうがあった。", "Old bullet trains used to have a smoking car.", R4D7)
V("体育会系", "たいいくかいけい", "Athletic/sports-club type", "彼は体育会系のクラブに入っていて、声が大きい。", "かれはたいいくかいけいのクラブにはいっていて、こえがおおきい。", "He's in an athletic-type club and has a loud voice.", R4D7)
V("途切れることなく", "とぎれることなく", "Without a break, continuously", "彼は途切れることなく話し続けた。", "かれはとぎれることなくはなしつづけた。", "He kept talking without a break.", R4D7)
V("気が気でなく", "きがきでなく", "Very worried, anxious", "娘の帰りが遅くて、気が気でなかった。", "むすめのかえりがおそくて、きがきでなかった。", "My daughter was late coming home and I was so worried.", R4D7)
V("暴力団", "ぼうりょくだん", "Gang/organized crime group", "警察は暴力団の活動を取り締まっている。", "けいさつはぼうりょくだんのかつどうをとりしまっている。", "The police crack down on organized crime activity.", R4D7)
V("陣取る", "じんどる", "To occupy/take up a position", "学生たちが図書館の一番いい席を陣取っていた。", "がくせいたちがとしょかんのいちばんいいせきをじんどっていた。", "The students had taken up the best seats in the library.", R4D7)

# --- Listening Section 1: 町で (plain vocab -> Deck 1) ---
L4D1 = "listening::w4 listening::w4d1 jlpt::n2"
V("運転を見合わせる", "うんてんをみあわせる", "To suspend (train) operation", "事故のため、電車は運転を見合わせている。", "じこのため、でんしゃはうんてんをみあわせている。", "Due to an accident, the train has suspended operation.", L4D1)
V("全線不通", "ぜんせんふつう", "Line stopped (entirely)", "台風で全線不通になった。", "たいふうでぜんせんふつうになった。", "The whole line was suspended due to the typhoon.", L4D1)
V("催し物会場", "もよおしものかいじょう", "Special event floor/venue", "7階の催し物会場で展示会が開かれている。", "7かいのもよおしものかいじょうでてんじかいがひらかれている。", "An exhibition is being held on the 7th-floor event venue.", L4D1)
V("新装開店", "しんそうかいてん", "Reopening of a store", "あの店は新装開店セールを行っている。", "あのみせはしんそうかいてんセールをおこなっている。", "That store is having a reopening sale.", L4D1)
V("正面玄関", "しょうめんげんかん", "Main entrance", "正面玄関でお待ちしております。", "しょうめんげんかんでおまちしております。", "I'll be waiting at the main entrance.", L4D1)
V("連絡通路", "れんらくつうろ", "Connecting corridor", "連絡通路を通って新館へ行けます。", "れんらくつうろをとおってしんかんへいけます。", "You can go to the new building via the connecting corridor.", L4D1)
V("寝具売り場", "しんぐうりば", "Bedding section", "寝具売り場で新しい枕を買った。", "しんぐうりばであたらしいまくらをかった。", "I bought a new pillow at the bedding section.", L4D1)
V("駆け込み乗車", "かけこみじょうしゃ", "Rushing onto a train as doors close", "駆け込み乗車は危ないのでやめましょう。", "かけこみじょうしゃはあぶないのでやめましょう。", "Rushing onto a train at the last moment is dangerous, so let's not do it.", L4D1)
V("終日", "しゅうじつ", "All day", "この店は終日禁煙です。", "このみせはしゅうじつきんえんです。", "This store is non-smoking all day.", L4D1)
V("人身事故", "じんしんじこ", "Accident involving injury/death to a person", "人身事故のため、電車が遅れている。", "じんしんじこのため、でんしゃがおくれている。", "The train is delayed due to an accident involving a person.", L4D1)

# --- Listening Section 2: 気象情報・交通情報 ---
L4D2 = "listening::w4 listening::w4d2 jlpt::n2"
V("明け方", "あけがた", "Dawn", "明け方に強い雨が降った。", "あけがたにつよいあめがふった。", "Heavy rain fell at dawn.", L4D2)
V("にわか雨", "にわかあめ", "Rain shower", "午後からにわか雨が降るでしょう。", "ごごからにわかあめがふるでしょう。", "There will likely be a rain shower in the afternoon.", L4D2)
V("雹", "ひょう", "Hail", "大きな雹が降って車が壊れた。", "おおきなひょうがふってくるまがこわれた。", "Large hail fell and damaged cars.", L4D2)
V("濃霧", "のうむ", "Dense fog", "濃霧のため、飛行機が欠航した。", "のうむのため、ひこうきがけっこうした。", "The flight was cancelled due to dense fog.", L4D2)
V("波浪", "はろう", "Strong ocean waves", "沿岸部に波浪注意報が出ている。", "えんがんぶにはろうちゅういほうがでている。", "A high-wave advisory has been issued for the coastal area.", L4D2)
V("津波", "つなみ", "Tsunami", "地震のあと、津波警報が出された。", "じしんのあと、つなみけいほうがだされた。", "A tsunami warning was issued after the earthquake.", L4D2)
V("洪水", "こうずい", "Flood", "大雨で川が洪水になった。", "おおあめでかわがこうずいになった。", "The river flooded due to heavy rain.", L4D2)
V("震度", "しんど", "Seismic intensity", "この地域は震度3を観測した。", "このちいきはしんど3をかんそくした。", "This area recorded a seismic intensity of 3.", L4D2)
V("規模", "きぼ", "Scale/size", "今回の地震はかなり規模が大きい。", "こんかいのじしんはかなりきぼがおおきい。", "This earthquake is quite large in scale.", L4D2)
V("震源", "しんげん", "Quake epicenter", "震源は海の底だった。", "しんげんはうみのそこだった。", "The epicenter was at the bottom of the sea.", L4D2)
V("欠航", "けっこう", "Flight cancellation", "台風で飛行機が欠航になった。", "たいふうでひこうきがけっこうになった。", "The flight was cancelled due to the typhoon.", L4D2)
V("出発を見合わせる", "しゅっぱつをみあわせる", "To postpone departure", "大雪のため、出発を見合わせています。", "おおゆきのため、しゅっぱつをみあわせています。", "Departure is being postponed due to heavy snow.", L4D2)
V("渋滞", "じゅうたい", "Traffic jam", "事故のため、高速道路が渋滞している。", "じこのため、こうそくどうろがじゅうたいしている。", "The highway is jammed due to an accident.", L4D2)
V("片側通行", "かたがわつうこう", "One-lane traffic", "工事中のため片側通行になっている。", "こうじちゅうのためかたがわつうこうになっている。", "It's one-lane traffic due to construction.", L4D2)
V("迂回", "うかい", "Detour", "この先、通行止めなので迂回してください。", "このさき、つうこうどめなのでうかいしてください。", "The road ahead is closed, so please take a detour.", L4D2)
V("揺れ", "ゆれ", "Shaking/swaying", "大きな揺れを感じてすぐに外に出た。", "おおきなゆれをかんじてすぐにそとにでた。", "I felt a big tremor and immediately went outside.", L4D2)
V("警戒する", "けいかいする", "To be on the alert for", "強い風に警戒してください。", "つよいかぜにけいかいしてください。", "Please be on alert for strong winds.", L4D2)
V("身の安全を確保する", "みのあんぜんをかくほする", "To take measures to ensure personal safety", "まず身の安全を確保することが大切だ。", "まずみのあんぜんをかくほすることがたいせつだ。", "First, it's important to ensure your own safety.", L4D2)
V("穏やかな", "おだやかな", "Peaceful, calm and gentle", "今日の海は穏やかだ。", "きょうのうみはおだやかだ。", "The sea is calm today.", L4D2)

# --- Listening Section 3: キャンパスで ---
L4D3 = "listening::w4 listening::w4d3 jlpt::n2"
V("新入生ガイダンス", "しんにゅうせいガイダンス", "New student orientation", "明日、新入生ガイダンスが行われる。", "あした、しんにゅうせいガイダンスがおこなわれる。", "New student orientation will be held tomorrow.", L4D3)
V("就職ガイダンス", "しゅうしょくガイダンス", "Career guidance counseling", "就職ガイダンスに参加して企業の話を聞いた。", "しゅうしょくガイダンスにさんかしてきぎょうのはなしをきいた。", "I attended career guidance and heard talks from companies.", L4D3)
V("健康診断", "けんこうしんだん", "Health check", "大学で毎年健康診断を受ける。", "だいがくでまいとしけんこうしんだんをうける。", "I get a health check every year at university.", L4D3)
V("避難訓練", "ひなんくんれん", "Evacuation drill", "今日は学校で避難訓練があった。", "きょうはがっこうでひなんくんれんがあった。", "There was an evacuation drill at school today.", L4D3)
V("受講する", "じゅこうする", "To take a course", "来学期は三つの授業を受講する予定だ。", "らいがっきはみっつのじゅぎょうをじゅこうするよていだ。", "I plan to take three classes next semester.", L4D3)
V("登録する", "とうろくする", "To register for a class/course", "授業をウェブサイトで登録した。", "じゅぎょうをウェブサイトでとうろくした。", "I registered for the class on the website.", L4D3)
V("延滞", "えんたい", "Overdue/late return", "本を延滞してしまい、罰則を受けた。", "ほんをえんたいしてしまい、ばっそくをうけた。", "I returned the book late and received a penalty.", L4D3)
V("聴講", "ちょうこう", "To attend/audit a lecture", "卒業生も授業を聴講できる。", "そつぎょうせいもじゅぎょうをちょうこうできる。", "Graduates can also audit classes.", L4D3)
V("締め切り", "しめきり", "Deadline, cut-off date", "レポートの締め切りは来週の月曜日だ。", "レポートのしめきりはらいしゅうのげつようびだ。", "The report deadline is next Monday.", L4D3)
V("学割", "がくわり", "Student discount", "学割で映画のチケットを買った。", "がくわりでえいがのチケットをかった。", "I bought a movie ticket with a student discount.", L4D3)
V("生協", "せいきょう", "Co-op (student cooperative association)", "お昼は生協でパンを買う。", "おひるはせいきょうでパンをかう。", "I buy bread at the co-op for lunch.", L4D3)
V("院生", "いんせい", "Graduate student", "彼は今、院生として研究を続けている。", "かれはいま、いんせいとしてけんきゅうをつづけている。", "He is now continuing his research as a graduate student.", L4D3)
V("卒論", "そつろん", "Graduation thesis", "卒論のテーマがまだ決まらない。", "そつろんのテーマがまだきまらない。", "I still haven't decided on my graduation thesis topic.", L4D3)
V("修論", "しゅうろん", "Master's thesis", "修論の提出まであと一か月だ。", "しゅうろんのていしゅつまであといっかげつだ。", "There's only one month left until my master's thesis is due.", L4D3)
V("博論", "はくろん", "Doctoral dissertation", "彼女は博論を書くのに5年かかった。", "かのじょははくろんをかくのに5ねんかかった。", "It took her five years to write her doctoral dissertation.", L4D3)
V("ふるって", "ふるって", "Actively/eagerly", "皆さん、ふるってご参加ください。", "みなさん、ふるってごさんかください。", "Everyone, please actively participate.", L4D3)

# --- Listening Section 4: いろいろな場面で ---
L4D4 = "listening::w4 listening::w4d4 jlpt::n2"
V("染みる", "しみる", "To sting/pierce, of pain", "冷たい水が虫歯に染みる。", "つめたいみずがむしばにしみる。", "Cold water stings my cavity.", L4D4)
V("麻酔", "ますい", "Anesthesia", "手術の前に麻酔をかけた。", "しゅじゅつのまえにますいをかけた。", "Anesthesia was administered before the surgery.", L4D4)
V("チクッとする", "チクッとする", "To feel a slight prick/tingling", "注射のとき、少しチクッとします。", "ちゅうしゃのとき、すこしチクッとします。", "You'll feel a slight prick when you get the injection.", L4D4)
V("口をすすぐ", "くちをすすぐ", "To rinse one's mouth", "歯を磨いたあと、口をすすいだ。", "はをみがいたあと、くちをすすいだ。", "I rinsed my mouth after brushing my teeth.", L4D4)
V("処方箋", "しょほうせん", "Prescription", "病院で処方箋をもらって薬局へ行った。", "びょういんでしょほうせんをもらってやっきょくへいった。", "I got a prescription at the hospital and went to the pharmacy.", L4D4)
V("お湯加減", "おゆかげん", "Temperature of the water", "お湯加減はいかがですか。", "おゆかげんはいかがですか。", "How is the water temperature?", L4D4)
V("メール便", "メールびん", "Mail service", "書類をメール便で送った。", "しょるいをメールびんでおくった。", "I sent the documents by mail service.", L4D4)
V("壊れ物", "こわれもの", "Fragile object", "この箱には壊れ物が入っている。", "このはこにはこわれものがはいっている。", "This box contains fragile items.", L4D4)
V("担当者", "たんとうしゃ", "The person in charge (e.g. delivery)", "荷物の担当者から電話があった。", "にもつのたんとうしゃからでんわがあった。", "I got a call from the person handling the delivery.", L4D4)
V("伝票", "でんぴょう", "Slip", "伝票番号を確認してください。", "でんぴょうばんごうをかくにんしてください。", "Please confirm the slip number.", L4D4)
V("代金引き換え", "だいきんひきかえ", "Cash on delivery", "この商品は代金引き換えで購入した。", "このしょうひんはだいきんひきかえでこうにゅうした。", "I purchased this item with cash on delivery.", L4D4)
V("着払い", "ちゃくばらい", "Cash on delivery (postage collect)", "荷物を着払いで送った。", "にもつをちゃくばらいでおくった。", "I sent the package with the recipient paying the shipping.", L4D4)
V("間取り", "まどり", "Room layout", "この部屋は間取りがいい。", "このへやはまどりがいい。", "This room has a good layout.", L4D4)
V("共益費", "きょうえきひ", "Common area charges", "家賃のほかに共益費がかかる。", "やちんのほかにきょうえきひがかかる。", "There's a common area charge in addition to the rent.", L4D4)
V("管理費", "かんりひ", "Maintenance fee", "マンションの管理費を毎月払っている。", "マンションのかんりひをまいつきはらっている。", "I pay the condo's maintenance fee every month.", L4D4)
V("築〜年", "ちく〜ねん", "Built ~ years ago", "このアパートは築10年だ。", "このアパートはちく10ねんだ。", "This apartment was built 10 years ago.", L4D4)
V("履歴書", "りれきしょ", "Resume", "履歴書に写真を貼った。", "りれきしょにしゃしんをはった。", "I attached a photo to my resume.", L4D4)
V("正社員", "せいしゃいん", "Regular employee", "彼は正社員として働いている。", "かれはせいしゃいんとしてはたらいている。", "He works as a regular employee.", L4D4)
V("時給", "じきゅう", "Hourly wage", "このバイトの時給は1200円だ。", "このバイトのじきゅうは1200えんだ。", "The hourly wage for this part-time job is 1200 yen.", L4D4)
V("代引き", "だいびき", "Cash on delivery (abbreviation)", "代引きで注文した。", "だいびきでちゅうもんした。", "I ordered with cash on delivery.", L4D4)
V("収納", "しゅうのう", "Storage", "この部屋は収納が多くて便利だ。", "このへやはしゅうのうがおおくてべんりだ。", "This room has a lot of storage and is convenient.", L4D4)
V("プレイガイド", "プレイガイド", "Ticket service", "コンサートのチケットをプレイガイドで買った。", "コンサートのチケットをプレイガイドでかった。", "I bought concert tickets through the ticket service.", L4D4)
V("敷金", "しききん", "Security deposit", "部屋を借りるとき敷金を払った。", "へやをかりるときしききんをはらった。", "I paid a security deposit when renting the room.", L4D4)
V("礼金", "れいきん", "Key money", "この物件は礼金なしで借りられる。", "このぶっけんはれいきんなしでかりられる。", "This property can be rented without key money.", L4D4)

# --- Listening Section 5: まとめ問題 ---
L4D5 = "listening::w4 listening::w4d5 jlpt::n2"
V("オルゴール", "オルゴール", "Music box", "誕生日にオルゴールをもらった。", "たんじょうびにオルゴールをもらった。", "I received a music box for my birthday.", L4D5)
V("却下する", "きゃっかする", "To reject, to dismiss", "提案は上司に却下された。", "ていあんはじょうしにきゃっかされた。", "The proposal was rejected by my boss.", L4D5)
V("交通の便がいい／悪い", "こうつうのべんがいい／わるい", "Convenient/inconvenient access", "この家は交通の便がいい。", "このいえはこうつうのべんがいい。", "This house has convenient access to transportation.", L4D5)
V("そうそうない", "そうそうない", "Rarely happens/hard to find", "こんなにいい物件はそうそうない。", "こんなにいいぶっけんはそうそうない。", "A property this good is hard to find.", L4D5)
V("申し分ない", "もうしぶんない", "Flawless/nothing to complain about", "このホテルのサービスは申し分ない。", "このホテルのサービスはもうしぶんない。", "This hotel's service is flawless.", L4D5)
V("視界が悪い", "しかいがわるい", "Poor visibility", "霧で視界が悪い。", "きりでしかいがわるい。", "Visibility is poor due to fog.", L4D5)
V("着陸", "ちゃくりく", "To land, to touch down", "飛行機は無事に着陸した。", "ひこうきはぶじにちゃくりくした。", "The plane landed safely.", L4D5)
V("展示即売会", "てんじそくばいかい", "Exhibition-and-sale event", "手作りの品物の展示即売会が開かれた。", "てづくりのしなもののてんじそくばいかいがひらかれた。", "An exhibition-and-sale of handmade goods was held.", L4D5)

# --- Grammar Day 1: できる上に ---
G4D1 = "grammar::w4 grammar::w4d1 jlpt::n2 type::grammar"
G("〜上に", "うえに", "explanation", "not only... but also...",
  [("彼は仕事ができる上に優しい。", "かれはしごとができるうえにやさしい。", "Not only is he good at his job but he's also a nice guy.")], G4D1)
G("〜上に", "うえに", "explanation", "not only... but also...",
  [("昨日は寒かった上に、風が強かった。", "きのうはさむかったうえに、かぜがつよかった。", "Yesterday it was cold and windy.")], G4D1)
G("〜上で", "うえで", "explanation", "after doing.../upon...",
  [("よく考えた上で決めます。", "よくかんがえたうえできめます。", "I will think well and then decide.")], G4D1)
G("〜上で", "うえで", "explanation", "after doing.../upon...",
  [("家族と相談の上、お返事します。", "かぞくとそうだんのうえ、おへんじします。", "I will reply after consulting my family.")], G4D1)
G("〜上は", "うえは", "explanation", "since.../now that... (must act accordingly)",
  [("キャプテンに選ばれた上は、がんばるしかない。", "キャプテンにえらばれたうえは、がんばるしかない。", "Since I was chosen as the captain, I must try my hardest.")], G4D1)
G("〜上は", "うえは", "explanation", "since.../now that... (must act accordingly)",
  [("入学する上は卒業したい。", "にゅうがくするうえはそつぎょうしたい。", "Now that I have entered school, I want to graduate.")], G4D1)
G("〜上で(は)", "うえで(は)", "explanation", "from the viewpoint of/in terms of",
  [("天気図の上では春なのに、実際はまだ寒い。", "てんきずのうえでははるなのに、じっさいはまださむい。", "On the weather map it looks like spring, but it is actually still cold.")], G4D1)
G("〜上で(は)", "うえで(は)", "explanation", "from the viewpoint of/in terms of",
  [("理論上はできるはずだったが、実験では失敗した。", "りろんじょうはできるはずだったが、じっけんではしっぱいした。", "Theoretically it should have been possible, but the experiment failed.")], G4D1)

# --- Grammar Day 2: 子ども向け ---
G4D2 = "grammar::w4 grammar::w4d2 jlpt::n2 type::grammar"
G("〜向け", "むけ", "explanation", "for/intended for",
  [("初心者向けの教科書です。", "しょしんしゃむけのきょうかしょです。", "It is a textbook for beginners.")], G4D2)
G("〜向け", "むけ", "explanation", "for/intended for",
  [("国内向けも、海外輸出向けも増加した。", "こくないむけも、かいがいゆしゅつむけもぞうかした。", "Manufacturing increased for both domestic and export markets.")], G4D2)
G("〜向き", "むき", "explanation", "suited for/fit for",
  [("この店の料理は見た目がきれいなので、女性向きだ。", "このみせのりょうりはみためがきれいなので、じょせいむきだ。", "The food at this restaurant looks nice, so it is suited for women.")], G4D2)
G("〜向き", "むき", "explanation", "suited for/fit for",
  [("この仕事は体力のある若い人向きだ。", "このしごとはたいりょくのあるわかいひとむきだ。", "This job is suited for young, physically fit people.")], G4D2)
G("〜次第で／〜次第だ", "しだいで／しだいだ", "explanation", "depending on",
  [("花火大会は天気次第で中止になる場合もあります。", "はなびたいかいはてんきしだいでちゅうしになるばあいもあります。", "The fireworks display may be cancelled depending on the weather.")], G4D2)
G("〜次第で／〜次第だ", "しだいで／しだいだ", "explanation", "depending on",
  [("うまくいくかどうかは本人次第だ。", "うまくいくかどうかはほんにんしだいだ。", "Whether it goes well or not depends on the person themselves.")], G4D2)
G("〜次第", "しだい", "explanation", "as soon as",
  [("田中が戻り次第、お電話させます。", "たなかがもどりしだい、おでんわさせます。", "As soon as Tanaka returns, I will have him call you.")], G4D2)
G("〜次第", "しだい", "explanation", "as soon as",
  [("決まり次第、ご連絡いたします。", "きまりしだい、ごれんらくいたします。", "I will contact you as soon as it is decided.")], G4D2)
G("〜次第です", "しだいです", "explanation", "that is the reason/that is why (formal)",
  [("このたび担当が替わりましたので、あいさつに伺った次第です。", "このたびたんとうがかわりましたので、あいさつにうかがったしだいです。", "I am here to greet you because I am the new person in charge.")], G4D2)
G("〜次第です", "しだいです", "explanation", "that is the reason/that is why (formal)",
  [("日時の変更について、改めてお知らせする次第です。", "にちじのへんこうについて、あらためておしらせするしだいです。", "I will inform you later of the change in the date and time.")], G4D2)

# --- Grammar Day 3: 期待にこたえて ---
G4D3 = "grammar::w4 grammar::w4d3 jlpt::n2 type::grammar"
G("〜にこたえて", "にこたえて", "explanation", "in response to/meeting a request",
  [("客の意見にこたえて、営業時間を延長する。", "きゃくのいけんにこたえて、えいぎょうじかんをえんちょうする。", "In response to customer requests, we are extending our business hours.")], G4D3)
G("〜にこたえて", "にこたえて", "explanation", "in response to/meeting a request",
  [("親の期待にこたえ、がんばった。", "おやのきたいにこたえ、がんばった。", "I worked hard to meet my parents' expectations.")], G4D3)
G("〜に対して", "にたいして", "explanation", "toward/in contrast to",
  [("目上の人に対して、そういう言い方は失礼ですよ。", "めうえのひとにたいして、そういういいかたはしつれいですよ。", "It is rude to speak to your superiors that way.")], G4D3)
G("〜に対して", "にたいして", "explanation", "toward/in contrast to",
  [("都市で人口が増えているのに対し、農村では減っている。", "としでじんこうがふえているのにたいし、のうそんではへっている。", "In contrast to the rising population in cities, it is falling in the countryside.")], G4D3)
G("〜により", "により", "explanation", "due to/by means of (formal)",
  [("未成年者の飲酒は、法律により禁じられている。", "みせいねんしゃのいんしゅは、ほうりつによりきんじられている。", "Minors' alcohol consumption is prohibited by law.")], G4D3)
G("〜により", "により", "explanation", "due to/by means of (formal)",
  [("その地震による被害は、過去最大だった。", "そのじしんによるひがいは、かこさいだいだった。", "The damage due to that earthquake was the largest in history.")], G4D3)
G("〜にかかわって", "にかかわって", "explanation", "concerning/involved in",
  [("彼は汚職事件にかかわって逮捕された。", "かれはおしょくじけんにかかわってたいほされた。", "He was arrested for being involved in a corruption case.")], G4D3)
G("〜にかかわって", "にかかわって", "explanation", "concerning/involved in",
  [("命にかかわる病気。", "いのちにかかわるびょうき。", "A life-threatening illness.")], G4D3)

# --- Grammar Day 4: 知りつつ ---
G4D4 = "grammar::w4 grammar::w4d4 jlpt::n2 type::grammar"
G("〜ながら(も)", "ながら(も)", "explanation", "while/although",
  [("悪いことと知りながら、盗みを繰り返した。", "わるいこととしりながら、ぬすみをくりかえした。", "While I knew it was wrong, I continued to steal.")], G4D4)
G("〜ながら(も)", "ながら(も)", "explanation", "while/although",
  [("「狭いながらも楽しいわが家」という言葉がある。", "「せまいながらもたのしいわがや」ということばがある。", "There is a saying, \"a small but happy home.\"")], G4D4)
G("〜つつ(も)", "つつ(も)", "explanation", "even though/while (also: doing two things at once)",
  [("彼女は忙しいと言いつつ、長電話をしている。", "かのじょはいそがしいといいつつ、ながでんわをしている。", "Though she says she's busy, she keeps having long phone calls.")], G4D4)
G("〜つつ(も)", "つつ(も)", "explanation", "even though/while (also: doing two things at once)",
  [("今日こそがんばろうと思いつつ、また勉強しなかった。", "きょうこそがんばろうとおもいつつ、またべんきょうしなかった。", "I was thinking I'd finally work hard today, but again I didn't study.")], G4D4)
G("〜つつ(も)", "つつ(も)", "explanation", "even though/while (also: doing two things at once)",
  [("先生と相談しつつ、進路を決めたいと思う。", "せんせいとそうだんしつつ、しんろをきめたいとおもう。", "I want to decide my career path while consulting with my teacher.")], G4D4)
G("〜つつある", "つつある", "explanation", "in the process of/progressively",
  [("医療はますます進歩しつつある。", "いりょうはますますしんぽしつつある。", "Medical care is progressing more and more.")], G4D4)
G("〜つつある", "つつある", "explanation", "in the process of/progressively",
  [("新種のウイルスによる被害は、全国に広がりつつある。", "しんしゅのウイルスによるひがいは、ぜんこくにひろがりつつある。", "Damage caused by the new virus is spreading across the nation.")], G4D4)
G("〜くせして", "くせして", "explanation", "although... (contemptuous)",
  [("知らないくせして、知っているようなことを言うな。", "しらないくせして、しっているようなことをいうな。", "Don't talk as if you know when you don't.")], G4D4)
G("〜くせして", "くせして", "explanation", "although... (contemptuous)",
  [("大学生のくせして、そんなことも知らないの？", "だいがくせいのくせして、そんなこともしらないの？", "You're a university student, and you don't even know that?")], G4D4)

# --- Grammar Day 5: せざるをえない ---
G4D5 = "grammar::w4 grammar::w4d5 jlpt::n2 type::grammar"
G("〜べき", "べき", "explanation", "should",
  [("そんなことをすべきではない。", "そんなことをすべきではない。", "You should not do that.")], G4D5)
G("〜べき", "べき", "explanation", "should",
  [("もっと勉強するべきだった。", "もっとべんきょうするべきだった。", "I should have studied more.")], G4D5)
G("〜ざるをえない", "ざるをえない", "explanation", "cannot help but/have no choice but to",
  [("いやな仕事でも、生活のためには続けざるをえない。", "いやなしごとでも、せいかつのためにはつづけざるをえない。", "Even if it's an unpleasant job, I have no choice but to continue it for the sake of my living.")], G4D5)
G("〜ざるをえない", "ざるをえない", "explanation", "cannot help but/have no choice but to",
  [("この戦争は間違いだったと言わざるをえない。", "このせんそうはまちがいだったといわざるをえない。", "I have no choice but to say this war was a mistake.")], G4D5)
G("〜ことになっている", "ことになっている", "explanation", "it is arranged/it is a rule",
  [("明日、ここで卒業式が行われることになっている。", "あした、ここでそつぎょうしきがおこなわれることになっている。", "The graduation ceremony is scheduled to be held here tomorrow.")], G4D5)
G("〜ことになっている", "ことになっている", "explanation", "it is arranged/it is a rule",
  [("60点以上が合格ということになっている。", "60てんいじょうがごうかくということになっている。", "The rule is that 60 points or more is a passing grade.")], G4D5)
G("〜にすぎない", "にすぎない", "explanation", "nothing more than/just",
  [("単なる言い間違いにすぎない。", "たんなるいいまちがいにすぎない。", "It is just a simple slip of the tongue.")], G4D5)
G("〜にすぎない", "にすぎない", "explanation", "nothing more than/just",
  [("簡単な日常英会話ができるにすぎない。", "かんたんなにちじょうえいかいわができるにすぎない。", "I can only have simple everyday conversations.")], G4D5)

# --- Grammar Day 6: 利用にあたり ---
G4D6 = "grammar::w4 grammar::w4d6 jlpt::n2 type::grammar"
G("〜にあたり", "にあたり", "explanation", "upon/when (formal, starting something official)",
  [("図書館の利用にあたり、図書カードが必要です。", "としょかんのりようにあたり、としょカードがひつようです。", "Upon using the library, a library card is necessary.")], G4D6)
G("〜にあたり", "にあたり", "explanation", "upon/when (formal, starting something official)",
  [("アルバイトをするにあたっては、学業に無理のないようにすること。", "アルバイトをするにあたっては、がくぎょうにむりのないようにすること。", "When working a part-time job, ensure it does not interfere with your studies.")], G4D6)
G("〜に沿って", "にそって", "explanation", "along/in accordance with",
  [("資料に沿って、ご説明いたします。", "しりょうにそって、ごせつめいいたします。", "I will explain based on the materials.")], G4D6)
G("〜に沿って", "にそって", "explanation", "along/in accordance with",
  [("お客様の希望に沿った旅行プランをお作りします。", "おきゃくさまのきぼうにそったりょこうプランをおつくりします。", "I will create a travel plan in accordance with the customer's wishes.")], G4D6)
G("〜に先立ち", "にさきだち", "explanation", "prior to (formal)",
  [("開店に先立ち、パーティーが行われた。", "かいてんにさきだち、パーティーがおこなわれた。", "A party was held prior to the opening.")], G4D6)
G("〜に先立ち", "にさきだち", "explanation", "prior to (formal)",
  [("新製品の開発に先立って、アンケート調査を行った。", "しんせいひんのかいはつにさきだって、アンケートちょうさをおこなった。", "We conducted a survey prior to developing the new product.")], G4D6)
G("〜にわたって", "にわたって", "explanation", "over a period/area",
  [("関東地方は広い範囲にわたって大雨となるでしょう。", "かんとうちほうはひろいはんいにわたっておおあめとなるでしょう。", "Heavy rain is expected over a wide area of the Kanto region.")], G4D6)
G("〜にわたって", "にわたって", "explanation", "over a period/area",
  [("20年間にわたり、この薬の研究をしてきた。", "20ねんかんにわたり、このくすりのけんきゅうをしてきた。", "We have conducted research on this drug for 20 years.")], G4D6)

# --- Grammar Bonus: 敬語 (Keigo) — お礼を言う① ---
G4KEIGO = "grammar::w4 grammar::w4dExtra jlpt::n2 type::keigo"
G("いただく／ちょうだいする", "いただく／ちょうだいする", "explanation", "keigo for もらう (to receive, humble)",
  [("ご意見をいただき、ありがとうございました。", "ごいけんをいただき、ありがとうございました。", "Thank you for your opinion."),
   ("意見をくれて、ありがとう。", "いけんをくれて、ありがとう。", "Thanks for the opinion.")], G4KEIGO)
G("ご覧いただく", "ごらんいただく", "explanation", "keigo for 見てもらう (to have someone look at, humble)",
  [("ご覧いただき、ありがとうございました。", "ごらんいただき、ありがとうございました。", "Thank you for viewing it."),
   ("見てくれて、ありがとう。", "みてくれて、ありがとう。", "Thanks for looking at it.")], G4KEIGO)

# --- Listening-derived Deck 2 items ---
G("上り線 ↔ 下り線", "のぼりせん ↔ くだりせん", "english", "inbound (to the city center) ↔ outbound (away from the city center)",
  [("上り線は事故のため止まっている。", "のぼりせんはじこのためとまっている。", "The inbound line is stopped due to an accident."),
   ("下り線はいつも通り動いている。", "くだりせんはいつもどおりうごいている。", "The outbound line is running as usual.")],
  "listening::w4 listening::w4d2 jlpt::n2 type::contrast")
G("承る", "うけたまわる", "explanation", "keigo for 受ける／引き受ける／聞く (to receive/accept/hear, humble)",
  [("ご予約は田中が承りました。", "ごよやくはたなかがうけたまわりました。", "Tanaka has taken your reservation."),
   ("予約は田中が受けました。", "よやくはたなかがうけました。", "Tanaka took the reservation.")],
  "listening::w4 listening::w4d4 jlpt::n2 type::keigo")

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
        "# Week 4 (Sou Matome N2) — Japanese vocabulary: Kanji/Vocabulary/Reading words",
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
        "# Week 4 (Sou Matome N2) — Japanese grammar and usage: Grammar/Listening patterns",
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
        # kanji-in-word-must-appear-in-sentence check (skip words with no kanji at all)
        kanji_chars = [ch for ch in re.sub(r'[（(].*?[)）]', '', word) if '一' <= ch <= '鿿']
        if kanji_chars and not any(ch in sentence for ch in kanji_chars):
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

    with open(os.path.join(base, "week4-v3-vocabulary.tsv"), "w", encoding="utf-8") as f:
        f.write(vocab_tsv)
    with open(os.path.join(base, "week4-v3-grammar-usage.tsv"), "w", encoding="utf-8") as f:
        f.write(grammar_tsv)
    print("Wrote TSVs.")

    if not errs:
        model1 = make_model(MODEL1_ID, "Japanese vocabulary")
        model2 = make_model(MODEL2_ID, "Japanese grammar and usage")
        n1 = build_apkg(vocab_tsv, DECK1_ID, "Japanese N2 Vocabulary", model1,
                         os.path.join(base, "week4-v3-vocabulary.apkg"))
        n2 = build_apkg(grammar_tsv, DECK2_ID, "Japanese N2 Grammar & Usage", model2,
                         os.path.join(base, "week4-v3-grammar-usage.apkg"))
        print(f"Wrote apkg: vocabulary={n1} notes, grammar-usage={n2} notes")
