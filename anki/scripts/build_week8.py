#!/usr/bin/env python3
"""Build Week 8 Anki TSV/apkg files (Deck 1 Vocabulary, Deck 2 Grammar & Usage).

Follows specs/anki-tsv-generation-process.md, specs/anki-note-type-vocabulary.md,
specs/anki-note-type-grammar-and-usage.md. Run from repo root:

    .venv/bin/python anki/scripts/build_week8.py

Note: Week 8 has no reading-w8.md or listening-w8.md (both source books stopped before
Week 7 already -- confirmed, not an oversight). This week's decks are built from
Kanji + Vocabulary + Grammar only.
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

# --- Kanji Day 1: 速報 ---
K8D1 = "kanji::w8 kanji::w8d1 jlpt::n2"
V("本州", "ほんしゅう", "Honshu (main island of Japan)", "本州は日本で一番大きい島だ。", "ほんしゅうはにほんでいちばんおおきいしまだ。", "Honshu is the largest island in Japan.", K8D1)
V("九州", "きゅうしゅう", "Kyushu", "夏休みに九州を旅行した。", "なつやすみにきゅうしゅうをりょこうした。", "I traveled around Kyushu during summer vacation.", K8D1)
V("電波", "でんぱ", "A radio wave", "この辺りは電波が弱い。", "このあたりはでんぱがよわい。", "The signal is weak around here.", K8D1)
V("波", "なみ", "A wave", "海で高い波が立っている。", "うみでたかいなみがたっている。", "There are high waves in the sea.", K8D1)
V("盗む", "ぬすむ", "Steal", "財布を盗まれた。", "さいふをぬすまれた。", "My wallet was stolen.", K8D1)
V("逃走", "とうそう", "An escape/flight", "犯人は逃走を続けている。", "はんにんはとうそうをつづけている。", "The culprit continues to be on the run.", K8D1)
V("逃げる", "にげる", "Escape", "犬が檻から逃げた。", "いぬがおりからにげた。", "The dog escaped from the cage.", K8D1)
V("逃がす", "にがす", "Release/let go", "捕まえた魚を逃がした。", "つかまえたさかなをにがした。", "I released the fish I caught.", K8D1)
V("逃す", "のがす", "Let slip", "絶好のチャンスを逃した。", "ぜっこうのチャンスをのがした。", "I let a great chance slip away.", K8D1)
V("疑問", "ぎもん", "A question/doubt", "その説明には疑問が残る。", "そのせつめいにはぎもんがのこる。", "That explanation leaves a question unanswered.", K8D1)
V("捕まる", "つかまる", "Be arrested/be caught", "泥棒が警察に捕まった。", "どろぼうがけいさつにつかまった。", "The thief was caught by the police.", K8D1)
V("捕る", "とる", "Take/catch (fish)", "川で魚を捕った。", "かわでさかなをとった。", "I caught fish in the river.", K8D1)
V("捕まえる", "つかまえる", "Arrest/catch", "警官が犯人を捕まえた。", "けいかんがはんにんをつかまえた。", "The police officer caught the criminal.", K8D1)
V("捕らえる", "とらえる", "Seize/grasp/arrest", "本質を捕らえた意見だ。", "ほんしつをとらえたいけんだ。", "It's an opinion that grasps the essence.", K8D1)
V("絶対に", "ぜったいに", "Absolutely/definitely", "絶対に遅刻しないでください。", "ぜったいにちこくしないでください。", "Please absolutely do not be late.", K8D1)
V("絶つ", "たつ", "Sever/cut off/suppress", "酒を絶つことにした。", "さけをたつことにした。", "I decided to give up alcohol.", K8D1)
V("政党", "せいとう", "A political party", "新しい政党が結成された。", "あたらしいせいとうがけっせいされた。", "A new political party was formed.", K8D1)
V("与党", "よとう", "The ruling party", "与党が予算案を可決した。", "よとうがよさんあんをかけつした。", "The ruling party passed the budget bill.", K8D1)
V("野党", "やとう", "The opposition party", "野党から首相の発言に対して批判の声が上がった。", "やとうからしゅしょうのはつげんにたいしてひはんのこえがあがった。", "Criticism of the prime minister's remarks arose from the opposition party.", K8D1)
V("候補者", "こうほしゃ", "A candidate", "私には支持政党はないが、支持する候補者はいる。", "わたしにはしじせいとうはないが、しじするこうほしゃはいる。", "I don't support any political party, but there is a candidate I support.", K8D1)
V("補助", "ほじょ", "Assistance/support", "政府から補助を受けた。", "せいふからほじょをうけた。", "We received assistance from the government.", K8D1)
V("補足", "ほそく", "Supplement/complement", "補足説明をさせて頂きます。", "ほそくせつめいをさせていただきます。", "Allow me to give a supplementary explanation.", K8D1)
V("補う", "おぎなう", "Compensate for/supplement", "この健康補助食品はカルシウムを補うのに最適です。", "このけんこうほじょしょくひんはカルシウムをおぎなうのにさいてきです。", "This health supplement is ideal for making up for calcium.", K8D1)
V("童話", "どうわ", "A fairy tale", "子どもに童話を読んで聞かせた。", "こどもにどうわをよんできかせた。", "I read a fairy tale to my child.", K8D1)
V("爆発", "ばくはつ", "An explosion", "昨夜、都心でガス爆発がありました。", "さくや、としんでガスばくはつがありました。", "There was a gas explosion in the city center last night.", K8D1)
V("暴走", "ぼうそう", "Running wildly", "トラックが暴走して事故を起こした。", "トラックがぼうそうしてじこをおこした。", "The truck ran out of control and caused an accident.", K8D1)
V("死亡", "しぼう", "Death", "事故で3人が死亡した。", "じこで3にんがしぼうした。", "Three people died in the accident.", K8D1)
V("亡くなる", "なくなる", "Die", "祖父が去年亡くなった。", "そふがきょねんなくなった。", "My grandfather passed away last year.", K8D1)
V("亡くす", "なくす", "Lose someone", "彼は若くして父を亡くした。", "かれはわかくしてちちをなくした。", "He lost his father while still young.", K8D1)
V("有罪", "ゆうざい", "Guilty", "被告は有罪判決を受けた。", "ひこくはゆうざいはんけつをうけた。", "The defendant received a guilty verdict.", K8D1)
V("無罪", "むざい", "Innocent", "彼は無罪を主張している。", "かれはむざいをしゅちょうしている。", "He is claiming innocence.", K8D1)
V("罪", "つみ", "A crime", "罪を犯した人でも更生できる。", "つみをおかしたひとでもこうせいできる。", "Even people who have committed crimes can be rehabilitated.", K8D1)

# --- Kanji Day 2: 見出し① ---
K8D2 = "kanji::w8 kanji::w8d2 jlpt::n2"
V("典型的", "てんけいてきな", "Typical/model/ideal", "母は典型的な古い日本の女性です。", "はははてんけいてきなふるいにほんのじょせいです。", "My mother is a typical old-fashioned Japanese woman.", K8D2)
V("大型", "おおがた", "A large/jumbo size", "大型台風が接近している。", "おおがたたいふうがせっきんしている。", "A large typhoon is approaching.", K8D2)
V("型", "かた", "Model/style", "この型の車は人気がある。", "このかたのくるまはにんきがある。", "This model of car is popular.", K8D2)
V("欧州", "おうしゅう", "Europe", "欧州を旅行する計画を立てた。", "おうしゅうをりょこうするけいかくをたてた。", "I made plans to travel around Europe.", K8D2)
V("苦労", "くろう", "Troubles/hardships", "彼は若い頃、苦労した。", "かれはわかいころ、くろうした。", "He went through hardships when he was young.", K8D2)
V("ご苦労様", "ごくろうさま", "Thank you for your work", "ご苦労様でした、気をつけて帰ってください。", "ごくろうさまでした、きをつけてかえってください。", "Thanks for your hard work, please get home safely.", K8D2)
V("兆", "ちょう", "Trillion (a sign/omen)", "文部科学省の前年度予算は6兆円を超えている。", "もんぶかがくしょうのぜんねんどよさんは6ちょうえんをこえている。", "The previous fiscal year's budget for the Ministry of Education exceeds 6 trillion yen.", K8D2)
V("貿易", "ぼうえき", "Foreign trade", "あなたの国と日本は昔から貿易をしています。", "あなたのくにとにほんはむかしからぼうえきをしています。", "Your country and Japan have traded with each other since long ago.", K8D2)
V("容易", "ようい", "Easy/plain/simple", "この問題を解決するのは容易ではない。", "このもんだいをかいけつするのはよういではない。", "Solving this problem is not easy.", K8D2)
V("安易", "あんいな", "Easy-going", "安易な考えでは成功しない。", "あんいなかんがえではせいこうしない。", "You won't succeed with an easy-going mindset.", K8D2)
V("易しい", "やさしい", "Easy/plain/simple", "まず、易しい問題から解いてみましょう。", "まず、やさしいもんだいからといてみましょう。", "First, let's try solving the easy problems.", K8D2)
V("農業", "のうぎょう", "Agriculture", "私のふるさとは農業がさかんです。", "わたしのふるさとはのうぎょうがさかんです。", "My hometown is thriving in agriculture.", K8D2)
V("農産物", "のうさんぶつ", "Agricultural produce", "この地域は農産物が豊富だ。", "このちいきはのうさんぶつがほうふだ。", "This region is rich in agricultural produce.", K8D2)
V("農家", "のうか", "A farmer/farm family", "祖父母は農家を営んでいる。", "そふぼはのうかをいとなんでいる。", "My grandparents run a farm.", K8D2)
V("命じる", "めいじる", "Order/command", "上司に出張を命じられた。", "じょうしにしゅっちょうをめいじられた。", "I was ordered by my boss to go on a business trip.", K8D2)
V("生命", "せいめい", "Life/existence", "生命の大切さを学んだ。", "せいめいのたいせつさをまなんだ。", "I learned the importance of life.", K8D2)
V("一生懸命", "いっしょうけんめい", "Very hard/with utmost effort", "一生懸命勉強している。", "いっしょうけんめいべんきょうしている。", "I am studying very hard.", K8D2)
V("命", "いのち", "Life", "一度しかない人生、命は大切にしましょう。", "いちどしかないじんせい、いのちはたいせつにしましょう。", "Life happens only once, so let's cherish it.", K8D2)
V("命令", "めいれい", "An order/command", "上司の命令に従った。", "じょうしのめいれいにしたがった。", "I followed my boss's order.", K8D2)
V("被害", "ひがい", "Damage", "大型台風により、各地で被害が出ています。", "おおがたたいふうにより、かくちでひがいがでています。", "Damage is occurring in various places due to the large typhoon.", K8D2)
V("被害者", "ひがいしゃ", "A victim", "被害者の人権を守ろう。", "ひがいしゃのじんけんをまもろう。", "Let's protect the victim's human rights.", K8D2)
V("害", "がい", "Injury/harm/damage", "この虫は農作物に害を与える。", "このむしはのうさくぶつにがいをあたえる。", "This insect causes harm to crops.", K8D2)
V("公害", "こうがい", "Public nuisance/pollution", "大型台風により、各地で公害などの被害が出ています。", "おおがたたいふうにより、かくちでこうがいなどのひがいがでています。", "Damage such as pollution is occurring in various places due to the large typhoon.", K8D2)
V("水害", "すいがい", "Water damage/flood disaster", "大雨のため、各地で水害が起きている。", "おおあめのため、かくちですいがいがおきている。", "Flood damage is occurring in various places due to heavy rain.", K8D2)
V("殺害", "さつがい", "A murder", "その事件では2人が殺害された。", "そのじけんでは2にんがさつがいされた。", "Two people were murdered in that incident.", K8D2)
V("権利", "けんり", "A right/privilege", "労働者には休む権利がある。", "ろうどうしゃにはやすむけんりがある。", "Workers have the right to rest.", K8D2)
V("人権", "じんけん", "Human rights/civil liberties", "被害者の人権を守ろう。", "ひがいしゃのじんけんをまもろう。", "Let's protect the victim's human rights.", K8D2)
V("億", "おく", "A hundred million", "日本の人口は約1億3千万人です。", "にほんのじんこうはやく1おく3ぜんまんにんです。", "Japan's population is about 130 million.", K8D2)
V("星座", "せいざ", "A constellation", "冬の星座を観察した。", "ふゆのせいざをかんさつした。", "I observed the winter constellations.", K8D2)
V("星", "ほし", "A star", "山の上では星がよく見える。", "やまのうえではほしがよくみえる。", "You can see the stars well from the mountain.", K8D2)
V("星印", "ほしじるし", "A star/an asterisk", "重要な項目に星印をつけた。", "じゅうようなこうもくにほしじるしをつけた。", "I put an asterisk on the important items.", K8D2)

# --- Kanji Day 3: 見出し② ---
K8D3 = "kanji::w8 kanji::w8d3 jlpt::n2"
V("武器", "ぶき", "A weapon/arms", "武器ではなく、話し合いで解決したい。", "ぶきではなく、はなしあいでかいけつしたい。", "I want to resolve this through discussion, not weapons.", K8D3)
V("武士", "ぶし", "A warrior/samurai", "あの娘さんは有名な武士の子孫だそうです。", "あのむすめさんはゆうめいなぶしのしそんだそうです。", "I hear that young lady is a descendant of a famous samurai.", K8D3)
V("武力", "ぶりょく", "Military power", "武力ではなく、話し合いで解決したい。", "ぶりょくではなく、はなしあいでかいけつしたい。", "I want to resolve this through discussion, not military force.", K8D3)
V("巨大", "きょだいな", "Huge/gigantic", "巨大魚がどこかの海岸で捕れたそうだ。", "きょだいぎょがどこかのかいがんでとれたそうだ。", "I heard a huge fish was caught on a beach somewhere.", K8D3)
V("巨額", "きょがく", "A great sum", "国は巨額の借金があります。", "くにはきょがくのしゃっきんがあります。", "The country has a huge debt.", K8D3)
V("競う", "きそう", "Emulate/compete with", "各国の選手たちは技を競い合った。", "かっこくのせんしゅたちはわざをきそいあった。", "Athletes from each country competed in their skills.", K8D3)
V("競馬", "けいば", "Horse racing", "父は競馬が趣味だ。", "ちちはけいばがしゅみだ。", "My father's hobby is horse racing.", K8D3)
V("失敗", "しっぱい", "A failure/mistake", "彼の実験は失敗に終わった。", "かれのじっけんはしっぱいにおわった。", "His experiment ended in failure.", K8D3)
V("敗れる", "やぶれる", "Be defeated", "日本チームは決勝で敗れた。", "にほんチームはけっしょうでやぶれた。", "The Japanese team was defeated in the finals.", K8D3)
V("連敗", "れんぱい", "A series of defeats", "そのチームは今シーズン連敗が続いている。", "そのチームはこんシーズンれんぱいがつづいている。", "That team has continued a losing streak this season.", K8D3)
V("逆", "ぎゃく", "The reverse/opposite", "それは私の考えとは逆だ。", "それはわたしのかんがえとはぎゃくだ。", "That is the opposite of what I think.", K8D3)
V("逆さ", "さかさ", "Upside down/inversion", "絵を逆さに掛けてしまった。", "えをさかさにかけてしまった。", "I accidentally hung the picture upside down.", K8D3)
V("逆転", "ぎゃくてん", "A sudden change/reversal", "9回に逆転で勝った。", "9かいにぎゃくてんでかった。", "We won with a reversal in the 9th inning.", K8D3)
V("優勝", "ゆうしょう", "A victory/championship", "彼のチームが大会で優勝した。", "かれのチームがたいかいでゆうしょうした。", "His team won the championship in the tournament.", K8D3)
V("勝敗", "しょうはい", "Victory or defeat", "最後まで勝敗はわからなかった。", "さいごまでしょうはいはわからなかった。", "The outcome remained uncertain until the very end.", K8D3)
V("勝つ", "かつ", "Win", "試合に勝つために練習を重ねた。", "しあいにかつためにれんしゅうをかさねた。", "I practiced repeatedly in order to win the match.", K8D3)
V("投手", "とうしゅ", "A baseball pitcher", "彼はチームのエース投手だ。", "かれはチームのエースとうしゅだ。", "He is the team's ace pitcher.", K8D3)
V("投資", "とうし", "An investment", "株に投資することにした。", "かぶにとうしすることにした。", "I decided to invest in stocks.", K8D3)
V("投書", "とうしょ", "A letter to the editor", "新聞に意見を投書する。", "しんぶんにいけんをとうしょする。", "I'll write a letter to the editor of the newspaper.", K8D3)
V("投げる", "なげる", "Throw", "子どもにボールを投げた。", "こどもにボールをなげた。", "I threw the ball to the child.", K8D3)
V("軍", "ぐん", "Army/troops", "軍が国境に配備された。", "ぐんがこっきょうにはいびされた。", "Troops were deployed to the border.", K8D3)
V("軍隊", "ぐんたい", "Army/troops", "軍隊に入隊した。", "ぐんたいににゅうたいした。", "He enlisted in the army.", K8D3)
V("兵士", "へいし", "A soldier", "兵士たちが戦地に向かった。", "へいしたちがせんちにむかった。", "The soldiers headed to the battlefield.", K8D3)
V("兵隊", "へいたい", "A soldier/an army", "祖父は兵隊として戦争に行った。", "そふはへいたいとしてせんそうにいった。", "My grandfather went to war as a soldier.", K8D3)
V("捜査", "そうさ", "A search/investigation", "警察は事件の捜査を進めている。", "けいさつはじけんのそうさをすすめている。", "The police are proceeding with the investigation of the case.", K8D3)
V("捜す", "さがす", "Search/seek", "行方不明の子どもを捜した。", "ゆくえふめいのこどもをさがした。", "We searched for the missing child.", K8D3)
V("転倒", "てんとう", "Falling down/upset", "雪道で転倒してけがをした。", "ゆきみちでてんとうしてけがをした。", "I fell down on the snowy road and got injured.", K8D3)
V("倒れる", "たおれる", "Collapse/break down", "強風で看板が倒れた。", "きょうふうでかんばんがたおれた。", "The signboard fell down due to strong wind.", K8D3)
V("倒す", "たおす", "Throw down/beat", "チャンピオンを倒して優勝した。", "チャンピオンをたおしてゆうしょうした。", "He won the championship by beating the champion.", K8D3)
V("骨", "ほね", "A bone", "この魚は頭も骨も全部食べられます。", "このさかなはあたまもほねもぜんぶたべられます。", "You can eat this fish's head and bones and everything.", K8D3)
V("方針", "ほうしん", "A principle/policy", "会社の方針が変わった。", "かいしゃのほうしんがかわった。", "The company's policy changed.", K8D3)
V("針", "はり", "A needle", "針に糸を通した。", "はりにいとをとおした。", "I threaded a needle.", K8D3)
V("針路", "しんろ", "A course/direction", "船は北へ針路を取った。", "ふねはきたへしんろをとった。", "The ship set its course to the north.", K8D3)
V("針金", "はりがね", "A wire", "針金で花を固定した。", "はりがねではなをこていした。", "I secured the flower with wire.", K8D3)
V("叫び", "さけび", "A shout/scream", "遠くから叫び声が聞こえた。", "とおくからさけびごえがきこえた。", "I heard a shout from far away.", K8D3)
V("叫ぶ", "さけぶ", "Shout/cry out", "救急車を呼んでと叫んだ。", "きゅうきゅうしゃをよんでとさけんだ。", "I shouted for someone to call an ambulance.", K8D3)

# --- Kanji Day 4: 記事① ---
K8D4 = "kanji::w8 kanji::w8d4 jlpt::n2"
V("頭脳", "ずのう", "A brain/intellect", "あの双子は兄弟そろって素晴らしい頭脳を持っている。", "あのふたごはきょうだいそろってすばらしいずのうをもっている。", "Both of those twin brothers have wonderful minds.", K8D4)
V("首脳", "しゅのう", "Head(s)/brains of a group", "各国の首脳が会議に集まった。", "かっこくのしゅのうがかいぎにあつまった。", "Leaders from each country gathered for the meeting.", K8D4)
V("抱く", "だく", "Embrace/hold", "赤ちゃんを優しく抱いた。", "あかちゃんをやさしくだいた。", "I gently held the baby.", K8D4)
V("抱く", "いだく", "Embrace/entertain (a hope/doubt)", "彼は将来への希望を抱いている。", "かれはしょうらいへのきぼうをいだいている。", "He holds hope for the future.", K8D4)
V("双方", "そうほう", "Both parties", "双方の意見を聞いてから決めよう。", "そうほうのいけんをきいてからきめよう。", "Let's decide after hearing both sides' opinions.", K8D4)
V("双子", "ふたご", "Twins", "あの双子は兄弟そろって素晴らしい頭脳を持っている。", "あのふたごはきょうだいそろってすばらしいずのうをもっている。", "Both of those twin brothers have wonderful minds.", K8D4)
V("尊重", "そんちょう", "Respect/esteem", "子どもの意志も尊重すべきです。", "こどものいしもそんちょうすべきです。", "Children's own will should also be respected.", K8D4)
V("尊敬", "そんけい", "Respect/esteem/reverence", "彼を心から尊敬している。", "かれをこころからそんけいしている。", "I respect him from the bottom of my heart.", K8D4)
V("雇用", "こよう", "Employment (long term)/hire", "会社は雇用を守ることを約束した。", "かいしゃはこようをまもることをやくそくした。", "The company promised to protect employment.", K8D4)
V("解雇", "かいこ", "A dismissal", "不況のため社員の半数が解雇された。", "ふきょうのためしゃいんのはんすうがかいこされた。", "Half of the employees were laid off due to the recession.", K8D4)
V("条件", "じょうけん", "Conditions/terms", "多少条件が悪くても、雇ってほしいと思っている。", "たしょうじょうけんがわるくても、やとってほしいとおもっている。", "Even if the conditions are a bit bad, I hope to be hired.", K8D4)
V("条約", "じょうやく", "A treaty", "両国は平和条約を結んだ。", "りょうこくはへいわじょうやくをむすんだ。", "The two countries concluded a peace treaty.", K8D4)
V("改善", "かいぜん", "An improvement", "作業環境の改善に努めている。", "さぎょうかんきょうのかいぜんにつとめている。", "We are working to improve the work environment.", K8D4)
V("親善", "しんぜん", "Friendship/goodwill", "国際親善を目的とした試合が行われる。", "こくさいしんぜんをもくてきとしたしあいがおこなわれる。", "A match is held with the aim of international friendship.", K8D4)
V("善悪", "ぜんあく", "Good and evil/right and wrong", "子どもに善悪の区別を教える。", "こどもにぜんあくのくべつをおしえる。", "I teach children the difference between good and evil.", K8D4)
V("法律", "ほうりつ", "Law/legislation", "新しい法律が施行された。", "あたらしいほうりつがしこうされた。", "A new law came into effect.", K8D4)
V("規律", "きりつ", "Order/discipline/rule", "寮では規律正しい生活をしている。", "りょうではきりつただしいせいかつをしている。", "I live a disciplined life in the dormitory.", K8D4)
V("情勢", "じょうせい", "Condition/situation", "経済の情勢が不安定だ。", "けいざいのじょうせいがふあんていだ。", "The economic situation is unstable.", K8D4)
V("姿勢", "しせい", "Posture/attitude", "正しい姿勢で座る。", "ただしいしせいですわる。", "Sit with correct posture.", K8D4)
V("大勢", "おおぜい", "A crowd/a great number of people", "コンサート会場は大勢のファンで超満員になった。", "コンサートかいじょうはおおぜいのファンでちょうまんいんになった。", "The concert venue was packed with a huge crowd of fans.", K8D4)
V("勢い", "いきおい", "Momentum/force/might", "優勝したチームは今回とても勢いがあった。", "ゆうしょうしたチームはこんかいとてもいきおいがあった。", "The team that won had a lot of momentum this time.", K8D4)
V("怖い", "こわい", "Scary", "夜道を一人で歩くのは怖い。", "よみちをひとりであるくのはこわい。", "It's scary to walk alone on a dark road at night.", K8D4)
V("荒い", "あらい", "Rough/rude/wild", "この馬は気が荒い。", "このうまはきがあらい。", "This horse has a rough temperament.", K8D4)
V("荒れる", "あれる", "Be stormy/be rough", "海が荒れていて船が出せない。", "うみがあれていてふねがだせない。", "The sea is rough, so the boat can't sail.", K8D4)
V("荒らす", "あらす", "Devastate/damage", "台風が畑を荒らした。", "たいふうがはたけをあらした。", "The typhoon devastated the fields.", K8D4)
V("耕地", "こうち", "Arable land", "この地域は耕地が広い。", "このちいきはこうちがひろい。", "This region has a lot of arable land.", K8D4)
V("休耕地", "きゅうこうち", "Land out of cultivation", "休耕地を再び活用する計画がある。", "きゅうこうちをふたたびかつようするけいかくがある。", "There is a plan to make use of fallow land again.", K8D4)
V("耕す", "たがやす", "Farm/till/cultivate", "祖父は毎朝畑を耕す。", "そふはまいあさはたけをたがやす。", "My grandfather tills the field every morning.", K8D4)
V("風景", "ふうけい", "Scenery", "山の上から美しい風景を眺めた。", "やまのうえからうつくしいふうけいをながめた。", "I gazed at the beautiful scenery from the top of the mountain.", K8D4)
V("景気", "けいき", "Business climate/condition", "最近、景気が回復してきた。", "さいきん、けいきがかいふくしてきた。", "Recently, the economy has been recovering.", K8D4)
V("光景", "こうけい", "A scene/spectacle", "感動的な光景を目にした。", "かんどうてきなこうけいをめにした。", "I witnessed a moving scene.", K8D4)
V("景色", "けしき", "A scene/landscape", "窓から美しい景色が見える。", "まどからうつくしいけしきがみえる。", "You can see beautiful scenery from the window.", K8D4)
V("掘る", "ほる", "Dig", "犬が庭の土を掘って何かを隠した。", "いぬがにわのつちをほってなにかをかくした。", "The dog dug up the garden soil and hid something.", K8D4)
V("掘り返す", "ほりかえす", "Dig up (something buried)", "工事で道路を掘り返している。", "こうじでどうろをほりかえしている。", "The road is being dug up for construction.", K8D4)

# --- Kanji Day 5: 記事② ---
K8D5 = "kanji::w8 kanji::w8d5 jlpt::n2"
V("批判", "ひはん", "Criticism/judgment", "大臣の発言を国民は批判的に受けとめた。", "だいじんのはつげんをこくみんはひはんてきにうけとめた。", "The public received the minister's remarks critically.", K8D5)
V("批評", "ひひょう", "A criticism/review/commentary", "映画の批評を読んだ。", "えいがのひひょうをよんだ。", "I read a review of the movie.", K8D5)
V("判断", "はんだん", "Judgment/decision", "人間だから、賢い人でも判断を誤ることがある。", "にんげんだから、かしこいひとでもはんだんをあやまることがある。", "Since we're human, even wise people can make wrong judgments.", K8D5)
V("裁判", "さいばん", "A trial", "その事件は裁判で争われた。", "そのじけんはさいばんであらそわれた。", "The case was contested in court.", K8D5)
V("評判", "ひょうばん", "Fame/reputation", "あの店は安くておいしいと評判だ。", "あのみせはやすくておいしいとひょうばんだ。", "That shop has a reputation for being cheap and delicious.", K8D5)
V("大臣", "だいじん", "A cabinet minister", "大臣の発言を国民は批判的に受けとめた。", "だいじんのはつげんをこくみんはひはんてきにうけとめた。", "The public received the minister's remarks critically.", K8D5)
V("外務大臣", "がいむだいじん", "Minister of Foreign Affairs", "外務大臣が海外を訪問した。", "がいむだいじんがかいがいをほうもんした。", "The Minister of Foreign Affairs visited abroad.", K8D5)
V("総理大臣", "そうりだいじん", "Prime Minister", "新しい総理大臣が選ばれた。", "あたらしいそうりだいじんがえらばれた。", "A new Prime Minister was selected.", K8D5)
V("賢明", "けんめいな", "Wise/prudent", "彼の判断は賢明だった。", "かれのはんだんはけんめいだった。", "His judgment was wise.", K8D5)
V("賢い", "かしこい", "Wise/clever/smart", "人間だから、賢い人でも判断を誤ることがある。", "にんげんだから、かしこいひとでもはんだんをあやまることがある。", "Since we're human, even wise people can make wrong judgments.", K8D5)
V("勇気", "ゆうき", "Courage/bravery", "彼に真実を話す勇気がなかった。", "かれにしんじつをはなすゆうきがなかった。", "I didn't have the courage to tell him the truth.", K8D5)
V("勇ましい", "いさましい", "Brave/valiant", "人間だから、勇ましい人でも判断を誤ることがある。", "にんげんだから、いさましいひとでもはんだんをあやまることがある。", "Since we're human, even brave people can make wrong judgments.", K8D5)
V("敬意", "けいい", "Respect/honor", "先輩に敬意を払う。", "せんぱいにけいいをはらう。", "I show respect to my senior.", K8D5)
V("敬う", "うやまう", "Show respect/honor", "現代人は他人を敬う気持ちに欠けているのではないだろうか。", "げんだいじんはたにんをうやまうきもちにかけているのではないだろうか。", "I wonder if modern people lack the feeling of respecting others.", K8D5)
V("敬語", "けいご", "Honorific style of speech", "敬語を正しく使うのはなかなか難しい。", "けいごをただしくつかうのはなかなかむずかしい。", "It's quite difficult to use honorific speech correctly.", K8D5)
V("評価", "ひょうか", "Valuation/estimation", "彼の仕事は高く評価されている。", "かれのしごとはたかくひょうかされている。", "His work is highly valued.", K8D5)
V("評論", "ひょうろん", "A criticism/critique", "彼は映画評論を書いている。", "かれはえいがひょうろんをかいている。", "He writes film critiques.", K8D5)
V("似る", "にる", "Resemble", "彼は父親によく似ている。", "かれはちちおやによくにている。", "He closely resembles his father.", K8D5)
V("似顔絵", "にがおえ", "A portrait", "駅前で似顔絵を描いてもらった。", "えきまえでにがおえをかいてもらった。", "I had my portrait drawn near the station.", K8D5)
V("似合う", "にあう", "Suit/match", "その帽子、あなたによく似合っていますよ。", "そのぼうし、あなたによくにあっていますよ。", "That hat suits you very well.", K8D5)
V("犯人", "はんにん", "An offender/a criminal", "犯人の顔や服装を覚えていますか。", "はんにんのかおやふくそうをおぼえていますか。", "Do you remember the criminal's face and clothing?", K8D5)
V("犯す", "おかす", "Commit (a crime)", "犯した罪をつぐなってほしい。", "おかしたつみをつぐなってほしい。", "I want him to atone for the crime he committed.", K8D5)
V("犯罪", "はんざい", "A crime", "この地域は犯罪が少ない。", "このちいきははんざいがすくない。", "This area has little crime.", K8D5)
V("子孫", "しそん", "Descendants/posterity", "あの娘さんは有名な武士の子孫だそうです。", "あのむすめさんはゆうめいなぶしのしそんだそうです。", "I hear that young lady is a descendant of a famous samurai.", K8D5)
V("孫", "まご", "A grandchild", "祖母は孫の成長を楽しみにしている。", "そぼはまごのせいちょうをたのしみにしている。", "My grandmother looks forward to her grandchild's growth.", K8D5)
V("娘", "むすめ", "A daughter", "娘は来年大学を卒業する。", "むすめはらいねんだいがくをそつぎょうする。", "My daughter will graduate from university next year.", K8D5)
V("孫娘", "まごむすめ", "A granddaughter", "孫娘が遊びに来てくれた。", "まごむすめがあそびにきてくれた。", "My granddaughter came to visit.", K8D5)
V("感覚", "かんかく", "A sense/sensation", "寒さで足の感覚がなくなった。", "さむさであしのかんかくがなくなった。", "My feet went numb from the cold.", K8D5)
V("覚ます", "さます", "Awaken", "大きな音で目を覚ました。", "おおきなおとでめをさました。", "I woke up to a loud noise.", K8D5)
V("覚える", "おぼえる", "Remember", "新しい単語を覚える。", "あたらしいたんごをおぼえる。", "I memorize new vocabulary.", K8D5)
V("覚める", "さめる", "Wake up", "朝早く目が覚めたのに、起きられなかった。", "あさはやくめがさめたのに、おきられなかった。", "I woke up early, but couldn't get out of bed.", K8D5)
V("目覚まし時計", "めざましどけい", "An alarm clock", "目覚まし時計が鳴らなかった。", "めざましどけいがならなかった。", "The alarm clock didn't go off.", K8D5)
V("帽子", "ぼうし", "A hat", "その帽子、あなたによく似合っていますよ。", "そのぼうし、あなたによくにあっていますよ。", "That hat suits you very well.", K8D5)

# --- Kanji Day 6: 記事③ ---
# 政党 is listed again under 政 here but was already carded under Day 1's 党 group -- kept there,
# skipped here (within-week cross-day Kanji-Kanji duplicate). 宙's only listed word, 宇宙, is a
# cross-week duplicate of week7's already-carded 宇宙 -- 宙 contributes no card of its own this
# week, same "kanji whose only compound lives elsewhere" shape as week5's 棒 and week7's 業.
K8D6 = "kanji::w8 kanji::w8d6 jlpt::n2"
V("環境", "かんきょう", "Environment/circumstance", "地球環境について考える。", "ちきゅうかんきょうについてかんがえる。", "Let's think about the global environment.", K8D6)
V("環状線", "かんじょうせん", "A belt line/loop line", "この電車は環状線なので乗り越してもまた戻ってきます。", "このでんしゃはかんじょうせんなのでのりこしてもまたもどってきます。", "This train is a loop line, so even if you go past your stop, it'll come back around.", K8D6)
V("境界", "きょうかい", "A boundary/limit", "二つの町の境界がはっきりしない。", "ふたつのまちのきょうかいがはっきりしない。", "The boundary between the two towns isn't clear.", K8D6)
V("境", "さかい", "A border/boundary", "この川が二つの県の境になっている。", "このかわがふたつのけんのさかいになっている。", "This river forms the border between the two prefectures.", K8D6)
V("国境", "こっきょう", "A national or state border", "ボランティア活動に国境はない。", "ボランティアかつどうにこっきょうはない。", "Volunteer activities know no borders.", K8D6)
V("県境", "けんざかい", "A prefectural border", "その村は県境に位置している。", "そのむらはけんざかいにいちしている。", "That village is located on the prefectural border.", K8D6)
V("削減", "さくげん", "A cut/reduction", "経費の削減に取り組んでいる。", "けいひのさくげんにとりくんでいる。", "We are working on cutting expenses.", K8D6)
V("加減", "かげん", "An adjustment/modification/extent", "湯加減はいかがですか。", "ゆかげんはいかがですか。", "How is the temperature of the bath water?", K8D6)
V("増減", "ぞうげん", "Increase and decrease", "これはこの町の人口の増減を表したグラフです。", "これはこのまちのじんこうのぞうげんをあらわしたグラフです。", "This is a graph showing the increase and decrease of this town's population.", K8D6)
V("減る", "へる", "Decrease", "貯金がだんだん減ってきた。", "ちょきんがだんだんへってきた。", "My savings have gradually decreased.", K8D6)
V("減らす", "へらす", "Decrease/reduce", "体重を減らすために運動している。", "たいじゅうをへらすためにうんどうしている。", "I exercise to lose weight.", K8D6)
V("努力", "どりょく", "Effort", "合格するために努力を続けた。", "ごうかくするためにどりょくをつづけた。", "I kept making efforts in order to pass.", K8D6)
V("努める", "つとめる", "Try hard/make efforts", "不況に負けずに景気回復に努めよう。", "ふきょうにまけずにけいきかいふくにつとめよう。", "Let's not lose to the recession and strive for economic recovery.", K8D6)
V("社会保険庁", "しゃかいほけんちょう", "Social Insurance Agency", "社会保険庁に問い合わせた。", "しゃかいほけんちょうにといあわせた。", "I made an inquiry to the Social Insurance Agency.", K8D6)
V("県庁", "けんちょう", "A prefectural office", "兄は県庁で職員として働いています。", "あにはけんちょうでしょくいんとしてはたらいています。", "My older brother works as a staff member at the prefectural office.", K8D6)
V("長官", "ちょうかん", "A director/chief", "あの方は気象庁長官です。", "あのかたはきしょうちょうちょうかんです。", "That person is the Director-General of the Japan Meteorological Agency.", K8D6)
V("独自", "どくじ", "Original/peculiar", "それは日本独自の考え方だと思う。", "それはにほんどくじのかんがえかただとおもう。", "I think that's a way of thinking unique to Japan.", K8D6)
V("日独", "にちどく", "Japan and Germany", "日独の関係は良好だ。", "にちどくのかんけいはりょうこうだ。", "Relations between Japan and Germany are good.", K8D6)
V("独身", "どくしん", "Single/unmarried", "彼は40歳になるまで独身だった。", "かれは40さいになるまでどくしんだった。", "He was single until he turned 40.", K8D6)
V("独り言", "ひとりごと", "Speaking to oneself/a monologue", "彼はよく独り言を言う。", "かれはよくひとりごとをいう。", "He often talks to himself.", K8D6)
V("競技", "きょうぎ", "A game/match/contest", "陸上競技の大会に出場した。", "りくじょうきょうぎのたいかいにしゅつじょうした。", "I competed in a track and field competition.", K8D6)
V("技", "わざ", "An art/technique", "柔道の色々な技を習う。", "じゅうどうのいろいろなわざをならう。", "I learn various judo techniques.", K8D6)
V("財政", "ざいせい", "Fiscal and financial affairs", "国の財政が悪化している。", "くにのざいせいがあっかしている。", "The nation's finances are deteriorating.", K8D6)
V("政府", "せいふ", "Government/administration", "政府が新しい政策を発表した。", "せいふがあたらしいせいさくをはっぴょうした。", "The government announced a new policy.", K8D6)
V("状況", "じょうきょう", "A situation/circumstances", "現場の状況を確認した。", "げんばのじょうきょうをかくにんした。", "I confirmed the situation at the site.", K8D6)
V("不況", "ふきょう", "Recession/depression", "不況に負けずに景気回復に努めよう。", "ふきょうにまけずにけいきかいふくにつとめよう。", "Let's not lose to the recession and strive for economic recovery.", K8D6)
V("腕力", "わんりょく", "Physical strength", "彼は腕力に自信がある。", "かれはわんりょくにじしんがある。", "He is confident in his physical strength.", K8D6)
V("腕", "うで", "Arm/skill", "相撲は相撲でも指や腕でする相撲もあります。", "すもうはすもうでもゆびやうででするすもうもあります。", "There's also a kind of sumo you do with your fingers or arms.", K8D6)
V("腕前", "うでまえ", "Ability/skill", "奥さんの料理の腕前はすごいですね。", "おくさんのりょうりのうでまえはすごいですね。", "Your wife's cooking skill is amazing, isn't it.", K8D6)

# --- Kanji Day 7 Extra: 上回る・下回る (bonus vocabulary for reading graphs, kanji 733-739) ---
K8DE = "kanji::w8 kanji::w8dExtra jlpt::n2"
V("上昇", "じょうしょう", "Rising/ascending", "気温が上昇している。", "きおんがじょうしょうしている。", "The temperature is rising.", K8DE)
V("昇る", "のぼる", "Rise", "太陽が東から昇る。", "たいようがひがしからのぼる。", "The sun rises in the east.", K8DE)
V("幅", "はば", "Width/breadth", "この道路は幅が狭い。", "このどうろははばがせまい。", "This road is narrow.", K8DE)
V("大幅", "おおはばな", "Substantial/large-scale", "大幅な値上げが発表された。", "おおはばなねあげがはっぴょうされた。", "A substantial price increase was announced.", K8DE)
V("著者", "ちょしゃ", "An author/writer", "この本の著者は有名な学者だ。", "このほんのちょしゃはゆうめいながくしゃだ。", "The author of this book is a famous scholar.", K8DE)
V("著す", "あらわす", "Write/publish", "彼は新しい理論を本に著した。", "かれはあたらしいりろんをほんにあらわした。", "He published a new theory in a book.", K8DE)
V("著しい", "いちじるしい", "Remarkable/considerable", "この地域は著しい発展を遂げた。", "このちいきはいちじるしいはってんをとげた。", "This region achieved remarkable development.", K8DE)
V("占める", "しめる", "Occupy", "AはBを上回り、Aが1位を占める。", "エーはビーをうわまわり、エーが1いをしめる。", "A exceeds B, and A occupies first place.", K8DE)
V("占う", "うらなう", "Tell a person's fortune", "占い師に将来を占ってもらった。", "うらないしにしょうらいをうらなってもらった。", "I had a fortune teller tell my future.", K8DE)
V("比較", "ひかく", "A comparison", "去年と今年の売り上げを比較した。", "きょねんとことしのうりあげをひかくした。", "I compared last year's and this year's sales.", K8DE)
V("比べる", "くらべる", "Compare", "兄と弟を比べるのはよくない。", "あにとおとうとをくらべるのはよくない。", "It's not good to compare an older and younger brother.", K8DE)
V("比較的", "ひかくてき", "Comparatively", "今日は比較的涼しい。", "きょうはひかくてきすずしい。", "Today is comparatively cool.", K8DE)
V("平年並み", "へいねんなみ", "An average year", "今年の降水量は平年並みだ。", "ことしのこうすいりょうはへいねんなみだ。", "This year's rainfall is about average.", K8DE)
V("並木", "なみき", "A row of trees", "駅前の並木道を歩いた。", "えきまえのなみきみちをあるいた。", "I walked along the tree-lined street near the station.", K8DE)
V("並ぶ", "ならぶ", "Stand in a line", "レジの前に人が並んでいる。", "レジのまえにひとがならんでいる。", "People are lining up in front of the register.", K8DE)
V("並べる", "ならべる", "Line up/set out", "テーブルに料理を並べた。", "テーブルにりょうりをならべた。", "I set the dishes out on the table.", K8DE)

# --- Vocabulary Day 1: 組み合わせの言葉① (combining verbs) ---
VOC8D1 = "vocabulary::w8 vocabulary::w8d1 jlpt::n2"
V("組み合わせる", "くみあわせる", "Put two together / combine", "映像と音楽を組み合わせて映画を製作します。", "えいぞうとおんがくをくみあわせてえいがをせいさくします。", "We will produce a movie by combining video and music.", VOC8D1)
V("組み立てる", "くみたてる", "Assemble (e.g. parts)", "説明書を見ながら家具を組み立てた。", "せつめいしょをみながらかぐをくみたてた。", "I assembled the furniture while looking at the instructions.", VOC8D1)
V("引き受ける", "ひきうける", "Take up / accept (e.g. a job)", "彼は難しい仕事を引き受けた。", "かれはむずかしいしごとをひきうけた。", "He took on a difficult job.", VOC8D1)
V("引き止める", "ひきとめる", "Keep (someone) from leaving / detain", "辞めようとする社員を引き止めた。", "やめようとするしゃいんをひきとめた。", "I tried to keep the employee who wanted to quit from leaving.", VOC8D1)
V("引き返す", "ひきかえす", "Return / turn back", "忘れ物に気づいて会社に引き返した。", "わすれものにきづいてかいしゃにひきかえした。", "I noticed I'd forgotten something and turned back to the office.", VOC8D1)
V("受け取る", "うけとる", "Receive (e.g. a parcel)", "荷物を受け取った。", "にもつをうけとった。", "I received the package.", VOC8D1)
V("受け取り", "うけとり", "A receipt", "受け取りのサインをお願いします。", "うけとりのサインをおねがいします。", "Please sign for the receipt.", VOC8D1)
V("受け持つ", "うけもつ", "Take charge of / teach", "彼女は私が先生として初めて受け持った生徒です。", "かのじょはわたしがせんせいとしてはじめてうけもったせいとです。", "She is the first student I taught as a teacher.", VOC8D1)
V("受け持ち", "うけもち", "Charge / taking care of", "このクラスの受け持ちは山田先生だ。", "このクラスのうけもちはやまだせんせいだ。", "Ms. Yamada is in charge of this class.", VOC8D1)
V("打ち合わせる", "うちあわせる", "Discuss / make arrangements", "明日の会議について打ち合わせた。", "あしたのかいぎについてうちあわせた。", "We discussed tomorrow's meeting.", VOC8D1)
V("打ち消す", "うちけす", "Deny (e.g. a rumor)", "彼はうわさを打ち消した。", "かれはうわさをうちけした。", "He denied the rumor.", VOC8D1)
V("売り切れる", "うりきれる", "Sell out", "人気商品はすぐに売り切れる。", "にんきしょうひんはすぐにうりきれる。", "Popular products sell out quickly.", VOC8D1)
V("売り切れ", "うりきれ", "Sold out", "そのチケットはもう売り切れです。", "そのチケットはもううりきれです。", "Those tickets are already sold out.", VOC8D1)
V("売り上げ", "うりあげ", "Sales", "今日1日で100万円の売り上げがあった。", "きょう1にちで100まんえんのうりあげがあった。", "There were 1 million yen in sales in a single day.", VOC8D1)
V("売れ行き", "うれゆき", "Sales / demand", "最近、音楽CDの売れ行きがとても悪い。", "さいきん、おんがくCDのうれゆきがとてもわるい。", "Recently, sales of music CDs have been very poor.", VOC8D1)
V("売り出す", "うりだす", "Put on the market / put on sale", "新商品を来月売り出す予定だ。", "しんしょうひんをらいげつうりだすよていだ。", "We plan to put the new product on sale next month.", VOC8D1)
V("売り出し", "うりだし", "A sale / launch", "デパートで冬物の売り出しが始まった。", "デパートでふゆもののうりだしがはじまった。", "The department store started its winter sale.", VOC8D1)
V("取り上げる", "とりあげる", "Take up / discuss (e.g. a problem)", "会議でその問題を取り上げた。", "かいぎでそのもんだいをとりあげた。", "We took up that issue at the meeting.", VOC8D1)
V("取り入れる", "とりいれる", "Incorporate / adopt", "主婦の意見を取り入れた使いやすいキッチン。", "しゅふのいけんをとりいれたつかいやすいキッチン。", "An easy-to-use kitchen that incorporates housewives' opinions.", VOC8D1)
V("取り組む", "とりくむ", "Tackle / grapple with (e.g. a new project)", "新しいプロジェクトに取り組んでいる。", "あたらしいプロジェクトにとりくんでいる。", "I'm tackling a new project.", VOC8D1)
V("取り組み", "とりくみ", "Effort / tackling", "環境問題への取り組みを強化する。", "かんきょうもんだいへのとりくみをきょうかする。", "We will strengthen our efforts on environmental issues.", VOC8D1)
V("取り扱う", "とりあつかう", "Operate / handle (e.g. a machine)", "当店では、その商品は取り扱っておりません。", "とうてんでは、そのしょうひんはとりあつかっておりません。", "We do not carry that product at our store.", VOC8D1)
V("取り扱い", "とりあつかい", "Handling", "この機械の取り扱いには注意が必要だ。", "このきかいのとりあつかいにはちゅういがひつようだ。", "Handling this machine requires care.", VOC8D1)
V("取り付ける", "とりつける", "Install / attach (e.g. an air-conditioner)", "壁にエアコンを取り付けた。", "かべにエアコンをとりつけた。", "I installed an air conditioner on the wall.", VOC8D1)
V("取り外す", "とりはずす", "Remove / detach", "古いエアコンを取り外した。", "ふるいエアコンをとりはずした。", "I removed the old air conditioner.", VOC8D1)
V("取り除く", "とりのぞく", "Remove (e.g. obstacles)", "危険な物を取り除いた。", "きけんなものをとりのぞいた。", "I removed the dangerous items.", VOC8D1)
V("振り向く", "ふりむく", "Turn around / look back", "名前を呼ばれて振り向いた。", "なまえをよばれてふりむいた。", "I turned around when my name was called.", VOC8D1)
V("振り返る", "ふりかえる", "Look back", "自分の人生を振り返る。", "じぶんのじんせいをふりかえる。", "I look back on my own life.", VOC8D1)
V("持ち上げる", "もちあげる", "Lift / raise (e.g. a suitcase)", "掃除するので、ちょっとイスを持ち上げてください。", "そうじするので、ちょっとイスをもちあげてください。", "Please lift the chair a bit since I'm going to clean.", VOC8D1)
V("払い戻す", "はらいもどす", "Refund / pay back (e.g. ticket cost)", "キャンセルしたチケット代を払い戻してもらった。", "キャンセルしたチケットだいをはらいもどしてもらった。", "I got a refund for the cancelled ticket.", VOC8D1)
V("立て替える", "たてかえる", "Pay for someone else temporarily / advance money", "電車賃は私が立て替えて払っておきました。", "でんしゃちんはわたしがたてかえてはらっておきました。", "I paid the train fare in advance for him.", VOC8D1)

# --- Vocabulary Day 2: 組み合わせの言葉② (more combining verbs) ---
VOC8D2 = "vocabulary::w8 vocabulary::w8d2 jlpt::n2"
V("追いかける", "おいかける", "Chase (e.g. a dog)", "その警察官は逃げる犯人を追いかけた。", "そのけいさつかんはにげるはんにんをおいかけた。", "That police officer chased the fleeing criminal.", VOC8D2)
V("追いつく", "おいつく", "Catch up with", "急いで走って、前を行く友達に追いついた。", "いそいではしって、まえをいくともだちにおいついた。", "I ran quickly and caught up with my friend ahead.", VOC8D2)
V("追い越し", "おいこし", "Passing", "この道路は追い越し禁止です。", "このどうろはおいこしきんしです。", "Passing is prohibited on this road.", VOC8D2)
V("追い出す", "おいだす", "Force to move out / expel (e.g. from an apartment)", "家賃を滞納して、アパートを追い出された。", "やちんをたいのうして、アパートをおいだされた。", "I fell behind on rent and was kicked out of the apartment.", VOC8D2)
V("乗り過ごす", "のりすごす", "Miss the stop (go past one's station)", "居眠りをして、駅を乗り過ごしてしまった。", "いねむりをして、えきをのりすごしてしまった。", "I dozed off and missed my stop.", VOC8D2)
V("乗り越し", "のりこし", "Riding past (one's stop)", "駅の改札で乗り越しの清算をした。", "えきのかいさつでのりこしのせいさんをした。", "I paid the fare adjustment for riding past my stop at the station gate.", VOC8D2)
V("乗り遅れる", "のりおくれる", "Miss the train", "寝坊して、電車に乗り遅れた。", "ねぼうして、でんしゃにのりおくれた。", "I overslept and missed the train.", VOC8D2)
V("割り引く", "わりびく", "Reduce the price / discount", "常連客には料金を割り引いている。", "じょうれんきゃくにはりょうきんをわりびいている。", "We give discounts to regular customers.", VOC8D2)
V("3割引", "さんわりびき", "30% discount", "セールで3割引になっていた。", "セールでさんわりびきになっていた。", "It was 30% off during the sale.", VOC8D2)
V("割り込む", "わりこむ", "Cut into the line / wedge oneself in", "列に割り込むのはマナー違反だ。", "れつにわりこむのはマナーいはんだ。", "Cutting into a line is a breach of manners.", VOC8D2)
V("割り込み乗車", "わりこみじょうしゃ", "Pushing one's way onto a train", "割り込み乗車はやめてください。", "わりこみじょうしゃはやめてください。", "Please don't push your way onto the train.", VOC8D2)
V("当てはめる", "あてはめる", "Apply / fit (e.g. to oneself)", "この公式を問題に当てはめて解く。", "このこうしきをもんだいにあてはめてとく。", "I solve the problem by applying this formula.", VOC8D2)
V("当てはまる", "あてはまる", "Fit / apply to (e.g. requirements)", "かっこの中に当てはまる語句を書きなさい。", "かっこのなかにあてはまるごくをかきなさい。", "Write the word that fits in the parentheses.", VOC8D2)
V("思い込み", "おもいこみ", "Firm belief / assumption", "それは単なる思い込みにすぎない。", "それはたんなるおもいこみにすぎない。", "That is nothing more than a mere assumption.", VOC8D2)
V("思いつく", "おもいつく", "Come up with (e.g. a good idea)", "いいアイデアを思いついた。", "いいアイデアをおもいついた。", "I came up with a good idea.", VOC8D2)
V("見つめる", "みつめる", "Stare at / look someone in the eye", "彼女は黙って私を見つめた。", "かのじょはだまってわたしをみつめた。", "She silently stared at me.", VOC8D2)
V("見かける", "みかける", "Happen to see / spot", "駅で偶然、昔の同級生を見かけた。", "えきでぐうぜん、むかしのどうきゅうせいをみかけた。", "I happened to see an old classmate at the station by chance.", VOC8D2)
V("見直す", "みなおす", "Check over / review (e.g. answers)", "インターネットの便利さを見直した。", "インターネットのべんりさをみなおした。", "I reconsidered the convenience of the internet.", VOC8D2)
V("見直し", "みなおし", "Review / re-evaluation", "予算の見直しが必要だ。", "よさんのみなおしがひつようだ。", "A budget review is necessary.", VOC8D2)
V("書き直す", "かきなおす", "Rewrite", "レポートを一から書き直した。", "レポートをいちからかきなおした。", "I rewrote the report from scratch.", VOC8D2)
V("言い直す", "いいなおす", "Rephrase", "誤解を招いた表現を言い直した。", "ごかいをまねいたひょうげんをいいなおした。", "I rephrased the expression that had caused a misunderstanding.", VOC8D2)
V("聞き直す", "ききなおす", "Ask again", "聞き取れなかったので、もう一度聞き直した。", "ききとれなかったので、もういちどききなおした。", "I couldn't catch it, so I asked again.", VOC8D2)
V("見習う", "みならう", "Learn from / emulate (e.g. a senior)", "先輩の仕事ぶりを見習いたい。", "せんぱいのしごとぶりをみならいたい。", "I want to learn from my senior's way of working.", VOC8D2)
V("見慣れる", "みなれる", "Become familiar with (e.g. scenery)", "この景色にもすっかり見慣れた。", "このけしきにもすっかりみなれた。", "I've become completely used to this scenery.", VOC8D2)
V("見渡す", "みわたす", "Look out over / survey", "山の頂上から街を見渡した。", "やまのちょうじょうからまちをみわたした。", "I looked out over the town from the top of the mountain.", VOC8D2)
V("書き留める", "かきとめる", "Jot down / write down", "大事なことをメモに書き留めた。", "だいじなことをメモにかきとめた。", "I jotted down the important thing in a memo.", VOC8D2)
V("書き込む", "かきこむ", "Write in / fill in", "アンケート用紙に意見を書き込んだ。", "アンケートようしにいけんをかきこんだ。", "I wrote my opinion on the survey form.", VOC8D2)
V("仕上がる", "しあがる", "Be finished / be completed (e.g. laundry)", "クリーニングに出した服が仕上がった。", "クリーニングにだしたふくがしあがった。", "The clothes I sent to the cleaner's are finished.", VOC8D2)
V("仕上がり", "しあがり", "Finish / completion", "この料理の仕上がりは上々だ。", "このりょうりのしあがりはじょうじょうだ。", "This dish turned out great.", VOC8D2)
V("仕上げる", "しあげる", "Finish / complete (e.g. a paper)", "この仕事を仕上げるのに、まだあと1週間はかかるでしょう。", "このしごとをしあげるのに、まだあと1しゅうかんはかかるでしょう。", "It will probably take another week to finish this job.", VOC8D2)
V("仕上げ", "しあげ", "Finishing touches", "最後の仕上げに丁寧に磨いた。", "さいごのしあげにていねいにみがいた。", "I carefully polished it as the finishing touch.", VOC8D2)
V("呼びかける", "よびかける", "Call out to / appeal to", "節電を呼びかけるポスターを貼った。", "せつでんをよびかけるポスターをはった。", "I put up a poster calling for energy conservation.", VOC8D2)
V("貸し出す", "かしだす", "Lend out", "図書館は本を無料で貸し出している。", "としょかんはほんをむりょうでかしだしている。", "The library lends out books for free.", VOC8D2)
V("貸し出し", "かしだし", "Lending", "自転車の貸し出しサービスがある。", "じてんしゃのかしだしサービスがある。", "There is a bicycle rental service.", VOC8D2)

# --- Vocabulary Day 3: よく使われる表現① (body-part expressions) ---
# 口がかたい (this day's 口 list) is an exact cross-week duplicate of week7's already-carded
# 口がかたい (Tight-lipped/discreet) -- skipped here, kept in week7.
VOC8D3 = "vocabulary::w8 vocabulary::w8d3 jlpt::n2"
V("目に見えて上達している", "めにみえてじょうたつしている", "Improving very fast / noticeably", "彼の日本語は目に見えて上達している。", "かれのにほんごはめにみえてじょうたつしている。", "His Japanese is improving noticeably.", VOC8D3)
V("環境問題に目を向けよう", "かんきょうもんだいにめをむけよう", "Pay more attention to environmental problems", "もっと環境問題に目を向けよう。", "もっとかんきょうもんだいにめをむけよう。", "Let's pay more attention to environmental problems.", VOC8D3)
V("歩き始めの幼児は目が離せない", "あるきはじめのようじはめがはなせない", "Must keep an eye on toddlers", "歩き始めの幼児は目が離せない。", "あるきはじめのようじはめがはなせない。", "You must keep an eye on toddlers who've just started walking.", VOC8D3)
V("目に付くところに置く", "めにつくところにおく", "Put in a place where people will easily notice it", "大事なものは目に付くところに置いておきましょう。", "だいじなものはめにつくところにおいておきましょう。", "Let's keep important things where they'll be easily noticed.", VOC8D3)
V("甘いものに目がない", "あまいものにめがない", "Have a sweet tooth / be extremely fond of", "妹は甘いものに目がない。", "いもうとはあまいものにめがない。", "My little sister has a sweet tooth.", VOC8D3)
V("目が回るように忙しい", "めがまわるようにいそがしい", "Extremely busy / dizzyingly busy", "昨日は忙しくて目が回るような1日だった。", "きのうはいそがしくてめがまわるような1にちだった。", "Yesterday was such a dizzyingly busy day.", VOC8D3)
V("母の姿が目に浮かぶ", "ははのすがたがめにうかぶ", "Mother comes to mind", "田舎に帰ると母の姿が目に浮かぶ。", "いなかにかえるとははのすがたがめにうかぶ。", "When I go back to the countryside, my mother's figure comes to mind.", VOC8D3)
V("学生のレポートに目を通す", "がくせいのレポートにめをとおす", "Go through the students' papers", "求人広告に目を通したけれど、適当なものがなかった。", "きゅうじんこうこくにめをとおしたけれど、てきとうなものがなかった。", "I went through the job ads, but there wasn't anything suitable.", VOC8D3)
V("親の目を盗んで遊びに行く", "おやのめをぬすんであそびにいく", "Go and play without parents knowing", "息子は親の目を盗んで遊んでばかりいる。", "むすこはおやのめをぬすんであそんでばかりいる。", "My son is always sneaking off to play behind his parents' backs.", VOC8D3)
V("ひどい目にあう", "ひどいめにあう", "Have a terrible experience", "山で道に迷って、ひどい目にあった。", "やまでみちにまよって、ひどいめにあった。", "I got lost in the mountains and had a terrible experience.", VOC8D3)
V("うわさを耳にした", "うわさをみみにした", "Heard a rumor", "この曲はだれもが一度は耳にしたことがあると思う。", "このきょくはだれもがいちどはみみにしたことがあるとおもう。", "I think everyone has heard this song at least once.", VOC8D3)
V("欠点を言われて耳が痛い", "けってんをいわれてみみがいたい", "It hurts to be reminded of my shortcomings", "自分の欠点を言われて耳が痛い。", "じぶんのけってんをいわれてみみがいたい。", "It stings to have my shortcomings pointed out.", VOC8D3)
V("祖母は耳が遠い", "そぼはみみがとおい", "Grandmother is hard of hearing", "祖母は耳が遠いので、大きな声で話す。", "そぼはみみがとおいので、おおきなこえではなす。", "My grandmother is hard of hearing, so I speak loudly.", VOC8D3)
V("ちょっと耳を貸して", "ちょっとみみをかして", "Let me tell you this / lend me your ear", "ちょっと耳を貸して、大事な話があるの。", "ちょっとみみをかして、だいじなはなしがあるの。", "Lend me your ear for a moment, I have something important to tell you.", VOC8D3)
V("耳が早いね", "みみがはやいね", "You catch on fast / you have quick ears", "もう知ってるの？耳が早いね。", "もうしってるの？みみがはやいね。", "You already know? You catch on fast.", VOC8D3)
V("事件のことを聞いて、耳を疑った", "じけんのことをきいて、みみをうたがった", "Couldn't believe my ears", "事件のことを聞いて、耳を疑った。", "じけんのことをきいて、みみをうたがった。", "I couldn't believe my ears when I heard about the incident.", VOC8D3)
V("セールスマンは口がうまい", "セールスマンはくちがうまい", "Watch out for salesmen who are good at flattery", "口がうまい人にだまされてはだめですよ。", "くちがうまいひとにだまされてはだめですよ。", "You mustn't be fooled by smooth-talking people.", VOC8D3)
V("彼は口が悪いけれど、やさしい", "かれはくちがわるいけれど、やさしい", "He has a sharp tongue but is actually kind", "彼は口が悪いけれど、やさしい。", "かれはくちがわるいけれど、やさしい。", "He has a sharp tongue but is actually kind.", VOC8D3)
V("これは私の口に合わない", "これはわたしのくちにあわない", "This is not to my taste", "この料理はちょっと口に合いません。", "このりょうりはちょっとくちにあいません。", "This dish isn't quite to my taste.", VOC8D3)
V("口にする", "くちにする", "Eat / talk about", "彼はその話題を一切口にしなかった。", "かれはそのわだいをいっさいくちにしなかった。", "He never once talked about that topic.", VOC8D3)
V("そんなことを口に出すべきではない", "そんなことをくちにだすべきではない", "You should not say such things", "そんなことを口に出すべきではない。", "そんなことをくちにだすべきではない。", "You should not say such things.", VOC8D3)
V("ぼくはその店では顔がきく", "ぼくはそのみせではかおがきく", "I have a lot of influence / am well-known at that shop", "ぼくはその店では顔がきく。", "ぼくはそのみせではかおがきく。", "I have a lot of influence at that shop.", VOC8D3)
V("彼は顔が広い", "かれはかおがひろい", "He has a lot of contacts / is well-connected", "彼は顔が広いので、いろいろな人を紹介してくれる。", "かれはかおがひろいので、いろいろなひとをしょうかいしてくれる。", "He's well-connected, so he introduces me to all kinds of people.", VOC8D3)
V("ちょっと顔を貸して", "ちょっとかおをかして", "Come for a short time / show your face", "ちょっと顔を貸してくれない？話があるんだ。", "ちょっとかおをかしてくれない？はなしがあるんだ。", "Can you come with me for a bit? I need to talk to you.", VOC8D3)
V("集まりに顔を出す", "あつまりにかおをだす", "Drop in on the meeting / show up", "今日の飲み会には、ちょっとだけ顔を出す予定です。", "きょうののみかいには、ちょっとだけかおをだすよていです。", "I plan to just briefly show my face at today's drinking party.", VOC8D3)
V("学生の態度に頭に来た", "がくせいのたいどにあたまにきた", "Got mad at the student's attitude", "学生の態度に頭に来た。", "がくせいのたいどにあたまにきた。", "I got mad at the student's attitude.", VOC8D3)
V("頭を下げる", "あたまをさげる", "Apologize / bow one's head", "ミスをして、上司に頭を下げた。", "ミスをして、じょうしにあたまをさげた。", "I made a mistake and bowed my head to apologize to my boss.", VOC8D3)
V("レポートのことを考えると頭が痛い", "レポートのことをかんがえるとあたまがいたい", "My head hurts thinking about the report", "レポートのことを考えると頭が痛い。", "レポートのことをかんがえるとあたまがいたい。", "My head hurts thinking about the report.", VOC8D3)
V("父は頭が固い", "ちちはあたまがかたい", "My father is inflexible / stubborn", "父は頭が固いから、新しい意見を聞き入れない。", "ちちはあたまがかたいから、あたらしいいけんをききいれない。", "My father is stubborn, so he doesn't accept new opinions.", VOC8D3)

# --- Vocabulary Day 4: よく使われる表現② (body-part expressions) ---
VOC8D4 = "vocabulary::w8 vocabulary::w8d4 jlpt::n2"
V("問題に手をつける", "もんだいにてをつける", "Start working on the problem", "そろそろこの問題に手をつけよう。", "そろそろこのもんだいにてをつけよう。", "Let's start working on this problem soon.", VOC8D4)
V("手が空いたら、来てください", "てがあいたら、きてください", "Please come when you have free time", "手が空いたら、来てください。", "てがあいたら、きてください。", "Please come when you have free time.", VOC8D4)
V("手がかかる子ども", "てがかかるこども", "A child who needs a lot of looking after", "3歳の娘はまだ手がかかる子どもだ。", "3さいのむすめはまだてがかかるこどもだ。", "My 3-year-old daughter is still a child who needs a lot of care.", VOC8D4)
V("手がない", "てがない", "No help / no means", "今は忙しくて手がない。", "いまはいそがしくててがない。", "I don't have anyone to help right now.", VOC8D4)
V("手が離せません", "てがはなせません", "I am too busy right now", "今、手が離せません。後でかけ直します。", "いま、てがはなせません。あとでかけなおします。", "I can't get away right now. I'll call you back later.", VOC8D4)
V("手がふさがっています", "てがふさがっています", "I am too busy right now (hands are full)", "今、手がふさがっているので、後にしてください。", "いま、てがふさがっているので、あとにしてください。", "My hands are full right now, so please come back later.", VOC8D4)
V("安く手に入れる", "やすくてにいれる", "Get it cheap", "3時間並んで、やっと手に入れた。", "3じかんならんで、やっとてにいれた。", "I waited in line for 3 hours and finally got it.", VOC8D4)
V("手に入る", "てにはいる", "Obtain", "珍しい本がようやく手に入った。", "めずらしいほんがようやくてにはいった。", "I finally obtained the rare book.", VOC8D4)
V("こんな病気、医者の手にかかればすぐ治る", "こんなびょうき、いしゃのてにかかればすぐなおる", "You will be fine if you go to the doctor", "こんな病気、医者の手にかかればすぐ治る。", "こんなびょうき、いしゃのてにかかればすぐなおる。", "With an illness like this, you'll be cured right away in the doctor's hands.", VOC8D4)
V("歯が痛くて勉強が手につかない", "はがいたくてべんきょうがてにつかない", "Tooth hurts so much I cannot concentrate on studying", "歯が痛くて勉強が手につかない。", "はがいたくてべんきょうがてにつかない。", "My tooth hurts so much I can't concentrate on studying.", VOC8D4)
V("ちょっと手を貸して", "ちょっとてをかして", "Lend me a hand / help me", "重いから、ちょっと手を貸して。", "おもいから、ちょっとてをかして。", "It's heavy, so please lend me a hand.", VOC8D4)
V("ちょっと手を休めましょう", "ちょっとてをやすめましょう", "Let's have a little break", "ちょっと手を休めましょう。", "ちょっとてをやすめましょう。", "Let's have a little break.", VOC8D4)
V("これは少し手を入れれば、まだ使えます", "これはすこしてをいれれば、まだつかえます", "You can use this longer if you repair it a bit", "この机は、少し手を入れれば、十分に使える。", "このつくえは、すこしてをいれれば、じゅうぶんにつかえる。", "This desk can still be used well if you fix it up a little.", VOC8D4)
V("私は彼とは気が合わない", "わたしはかれとはきがあわない", "I don't get along with him", "私は彼とは気が合わない。", "わたしはかれとはきがあわない。", "I don't get along with him.", VOC8D4)
V("明日試験だから気が重い", "あしたしけんだからきがおもい", "I feel depressed/heavy because tomorrow is the exam", "明日からまた学校だと思うと気が重い。", "あしたからまたがっこうだとおもうときがおもい。", "I feel heavy-hearted thinking that school starts again tomorrow.", VOC8D4)
V("気が利いた冗談を言う", "きがきいたじょうだんをいう", "Tell a sophisticated/clever joke", "彼はいつも気が利いた冗談を言う。", "かれはいつもきがきいたじょうだんをいう。", "He always tells clever jokes.", VOC8D4)
V("今、甘いものを食べる気がしない", "いま、あまいものをたべるきがしない", "I don't feel like eating sweets right now", "今、甘いものを食べる気がしない。", "いま、あまいものをたべるきがしない。", "I don't feel like eating sweets right now.", VOC8D4)
V("気が進まないけれど、やってみよう", "きがすすまないけれど、やってみよう", "I don't really want to, but I'll try", "今度の仕事はあまり気が進まない。", "こんどのしごとはあまりきがすすまない。", "I'm not really enthusiastic about this new job.", VOC8D4)
V("息子のことが気にかかる", "むすこのことがきにかかる", "I can't take my mind off my son / worry about", "息子のことが気にかかる。", "むすこのことがきにかかる。", "I can't take my mind off my son.", VOC8D4)
V("あいつの態度が気にくわない", "あいつのたいどがきにくわない", "I don't like his attitude", "あいつの態度が気にくわない。", "あいつのたいどがきにくわない。", "I don't like his attitude.", VOC8D4)
V("気を落とさないように", "きをおとさないように", "Don't get discouraged", "試験に落ちても気を落とさないように。", "しけんにおちてもきをおとさないように。", "Don't get discouraged even if you fail the exam.", VOC8D4)
V("上司に気をつかう", "じょうしにきをつかう", "Make an effort to satisfy the boss", "働くのもいいけど、健康にも気を使うようにしてください。", "はたらくのもいいけど、けんこうにもきをつかうようにしてください。", "Working is fine, but please also be careful about your health.", VOC8D4)
V("気を悪くしないでください", "きをわるくしないでください", "Please don't feel offended", "気を悪くしないでくださいね。", "きをわるくしないでくださいね。", "Please don't feel offended.", VOC8D4)
V("腕がいい大工", "うでがいいだいく", "A very experienced/skilled carpenter", "あの歯医者はとても腕がいいという評判だ。", "あのはいしゃはとてもうでがいいというひょうばんだ。", "That dentist has a reputation for being very skilled.", VOC8D4)
V("ゴルフの腕が上がった", "ゴルフのうでがあがった", "Golfing skills have improved", "練習のおかげでゴルフの腕が上がった。", "れんしゅうのおかげでゴルフのうでがあがった。", "Thanks to practice, my golf skills have improved.", VOC8D4)
V("腕が落ちる", "うでがおちる", "Skills decline", "練習しないと腕が落ちる。", "れんしゅうしないとうでがおちる。", "If you don't practice, your skills decline.", VOC8D4)
V("もっとうまくなるように腕をみがこう", "もっとうまくなるようにうでをみがこう", "Let's practice more to improve our skills", "もっとうまくなるように腕をみがこう。", "もっとうまくなるようにうでをみがこう。", "Let's practice more to improve our skills.", VOC8D4)
V("京都まで足を伸ばそう", "きょうとまであしをのばそう", "Let's extend our trip to Kyoto", "せっかくここまで来たんだから、もう少し足を伸ばして京都まで行こうよ。", "せっかくここまできたんだから、もうすこしあしをのばしてきょうとまでいこうよ。", "Since we've come this far, let's go a bit further to Kyoto.", VOC8D4)
V("足がないので、行けない", "あしがないので、いけない", "I have no means of transportation, so I can't go", "車を修理に出してしまったので、行きたいけど足がないのです。", "くるまをしゅうりにだしてしまったので、いきたいけどあしがないのです。", "I sent my car in for repair, so even though I want to go, I have no way to get there.", VOC8D4)
V("実際に足を運んで、品物を確かめる", "じっさいにあしをはこんで、しなものをたしかめる", "Actually go and check the item", "実際に足を運んで、品物を確かめる。", "じっさいにあしをはこんで、しなものをたしかめる。", "Actually go and check the item in person.", VOC8D4)
V("予算から足が出る", "よさんからあしがでる", "Be over budget", "旅行の費用が予算から足が出てしまった。", "りょこうのひようがよさんからあしがでてしまった。", "The travel costs went over budget.", VOC8D4)

# --- Vocabulary Day 5: よく使われる表現③ (idiomatic expressions & adverbs) ---
VOC8D5 = "vocabulary::w8 vocabulary::w8d5 jlpt::n2"
V("ついていく", "ついていく", "Follow / go along with", "子どもが母親のあとをついていく。", "こどもがははおやのあとをついていく。", "The child follows behind his mother.", VOC8D5)
V("彼の考えにはついていけない", "かれのかんがえにはついていけない", "I can't go along with his idea", "彼の考えにはついていけない。", "かれのかんがえにはついていけない。", "I can't go along with his idea.", VOC8D5)
V("ついてる", "ついてる", "Be lucky", "ラッシュなのに座れて、今日はついている。", "ラッシュなのにすわれて、きょうはついている。", "Even though it's rush hour, I got a seat—I'm lucky today.", VOC8D5)
V("ついてない", "ついてない", "Be unlucky", "今日はついてない。財布まで落とした。", "きょうはついてない。さいふまでおとした。", "I'm having bad luck today. I even lost my wallet.", VOC8D5)
V("私は、日本酒はダメですが、ビールはいけます", "わたしは、にほんしゅはダメですが、ビールはいけます", "I can't drink sake, but beer is OK", "私は、日本酒はダメですが、ビールはいけます。", "わたしは、にほんしゅはダメですが、ビールはいけます。", "I can't drink sake, but beer is OK for me.", VOC8D5)
V("この料理はなかなかいける", "このりょうりはなかなかいける", "This dish is quite good", "この料理はなかなかいける。", "このりょうりはなかなかいける。", "This dish is quite good.", VOC8D5)
V("つまらないことにこだわる", "つまらないことにこだわる", "Fuss over small details", "彼はいつもつまらないことにこだわる。", "かれはいつもつまらないことにこだわる。", "He always fusses over trivial things.", VOC8D5)
V("材料にこだわって料理を作る", "ざいりょうにこだわってりょうりをつくる", "Choose good ingredients for cooking", "材料にこだわって料理を作る。", "ざいりょうにこだわってりょうりをつくる。", "I choose good ingredients when cooking.", VOC8D5)
V("こだわりがある", "こだわりがある", "Care about / have particular standards", "彼はコーヒーの淹れ方にこだわりがある。", "かれはコーヒーのいれかたにこだわりがある。", "He has particular standards about how coffee is brewed.", VOC8D5)
V("捨てるのはもったいない", "すてるのはもったいない", "Too good to be thrown out", "まだ使えるのに捨てるのはもったいない。", "まだつかえるのにすてるのはもったいない。", "It's a waste to throw it out when it can still be used.", VOC8D5)
V("ボーナスが5万円でも、ないよりはましだ", "ボーナスが5まんえんでも、ないよりはましだ", "50,000 yen is better than nothing", "ボーナスが5万円でも、ないよりはましだ。", "ボーナスが5まんえんでも、ないよりはましだ。", "Even if the bonus is only 50,000 yen, it's better than nothing.", VOC8D5)
V("まともな生活をする", "まともなせいかつをする", "Live a decent life", "まともな生活をする。", "まともなせいかつをする。", "I live a decent life.", VOC8D5)
V("最近、ろくな仕事がない", "さいきん、ろくなしごとがない", "There are no decent jobs these days", "最近、ろくな仕事がない。", "さいきん、ろくなしごとがない。", "There are no decent jobs these days.", VOC8D5)
V("妻はろくに料理を作らない", "つまはろくにりょうりをつくらない", "My wife hardly cooks", "妻はろくに料理を作らない。", "つまはろくにりょうりをつくらない。", "My wife hardly cooks.", VOC8D5)
V("彼の実力は大したものだ", "かれのじつりょくはたいしたものだ", "He is really something", "彼の実力は大したものだ。", "かれのじつりょくはたいしたものだ。", "He is really something.", VOC8D5)
V("大したものはありませんが、どうぞ召し上がってください", "たいしたものはありませんが、どうぞめしあがってください", "This isn't much of a meal, but please enjoy", "大したものはありませんが、どうぞ召し上がってください。", "たいしたものはありませんが、どうぞめしあがってください。", "This isn't much of a meal, but please enjoy.", VOC8D5)
V("母の病気は大したことはない", "ははのびょうきはたいしたことはない", "My mother's illness isn't very serious", "母の病気は大したことはない。", "ははのびょうきはたいしたことはない。", "My mother's illness isn't very serious.", VOC8D5)
V("あっという間に", "あっというまに", "In the blink of an eye / before I knew it", "あの店は、開店したと思ったらあっという間につぶれてしまった。", "あのみせは、かいてんしたとおもったらあっというまにつぶれてしまった。", "That shop closed down in the blink of an eye after it opened.", VOC8D5)
V("あれこれ／あれやこれや／なんだかんだ", "あれこれ／あれやこれや／なんだかんだ", "This and that / one way or another", "あれこれ悩んだが、結局引っ越すことにした。", "あれこれなやんだが、けっきょくひっこすことにした。", "I worried over this and that, but in the end decided to move.", VOC8D5)
V("当たり前", "あたりまえ", "Natural / reasonable / common", "赤ちゃんが泣くのは当たり前です。", "あかちゃんがなくのはあたりまえです。", "It's natural for babies to cry.", VOC8D5)
V("彼女は仕事の覚えが悪い", "かのじょはしごとのおぼえがわるい", "She is slow to learn her job", "彼女は仕事の覚えが悪い。", "かのじょはしごとのおぼえがわるい。", "She is slow to learn her job.", VOC8D5)
V("そんなことを言った覚えはない", "そんなことをいったおぼえはない", "I don't recall saying anything like that", "そんなことを言った覚えはない。", "そんなことをいったおぼえはない。", "I don't recall saying anything like that.", VOC8D5)
V("覚えがない", "おぼえがない", "Have no recollection (of something)", "利用した覚えのない請求書が届いた。", "りようしたおぼえのないせいきゅうしょがとどいた。", "A bill arrived for something I have no recollection of using.", VOC8D5)
V("新しい車を買う余裕がない", "あたらしいくるまをかうよゆうがない", "Can't afford a new car", "新しい車を買う余裕がない。", "あたらしいくるまをかうよゆうがない。", "I can't afford a new car.", VOC8D5)
V("待ち合わせには余裕をもって出かけよう", "まちあわせにはよゆうをもってでかけよう", "Go to appointments with time to spare", "待ち合わせには余裕をもって出かけよう。", "まちあわせにはよゆうをもってでかけよう。", "Let's leave with plenty of time to spare for our meeting.", VOC8D5)

# --- Vocabulary Day 6: よく使われる表現④ (paired actions, set phrases, slang) ---
# 超～ (slang note on the already-carded 超 prefix, week7 kanji-w7d5's 超満員/超特急/超小型/超忙しい)
# skipped -- the prefix itself already has cards; this bullet is just a register note, not new
# vocabulary.
VOC8D6 = "vocabulary::w8 vocabulary::w8d6 jlpt::n2"
V("見聞き", "みきき", "Experience / see and hear", "旅先で見聞きしたことをブログに書いた。", "たびさきでみききしたことをブログにかいた。", "I wrote about what I saw and heard on my trip in my blog.", VOC8D6)
V("行き来", "いきき", "Visit each other / come and go", "駅から会場までを行き来するバスが出ている。", "えきからかいじょうまでをいききするバスがでている。", "There's a bus that goes back and forth between the station and the venue.", VOC8D6)
V("貸し借り", "かしかり", "Borrow and lend", "友達とお金の貸し借りはしない主義だ。", "ともだちとおかねのかしかりはしないしゅぎだ。", "My policy is not to lend or borrow money with friends.", VOC8D6)
V("出し入れ", "だしいれ", "Take in and out", "頻繁に出し入れするものは手前に置く。", "ひんぱんにだしいれするものはてまえにおく。", "Put things you take in and out often near the front.", VOC8D6)
V("付け外し", "つけはずし", "Attach and detach / detachable", "このフードは付け外しができる。", "このフードはつけはずしができる。", "This hood is detachable.", VOC8D6)
V("脱ぎ着", "ぬぎき", "Put on and take off (clothes)", "脱ぎ着しやすい服を選んだ。", "ぬぎきしやすいふくをえらんだ。", "I chose clothes that are easy to put on and take off.", VOC8D6)
V("読み書き", "よみかき", "Reading and writing", "子どもに漢字の読み書きを教える。", "こどもにかんじのよみかきをおしえる。", "I teach my child to read and write kanji.", VOC8D6)
V("上げ下げ", "あげさげ", "Raising and lowering", "音量の上げ下げはこのボタンで行います。", "おんりょうのあげさげはこのボタンでおこないます。", "You adjust the volume up and down with this button.", VOC8D6)
V("売り買い", "うりかい", "Buying and selling", "株の売り買いで利益を得た。", "かぶのうりかいでりえきをえた。", "I made a profit from buying and selling stocks.", VOC8D6)
V("行き帰り", "いきかえり", "Going and returning / round trip", "会社への行き帰りに本を読んでいる。", "かいしゃへのいきかえりにほんをよんでいる。", "I read books on my way to and from work.", VOC8D6)
V("好き嫌い", "すききらい", "Likes and dislikes / picky", "子どもの好き嫌いをなくしたい。", "こどものすききらいをなくしたい。", "I want to get rid of my child's picky eating.", VOC8D6)
V("いつもお世話になっています", "いつもおせわになっています", "Thank you for your kind support", "娘がいつもお世話になっています。", "むすめがいつもおせわになっています。", "Thank you for always taking care of my daughter.", VOC8D6)
V("少し様子をみましょう", "すこしようすをみましょう", "Let's see how it goes", "手術をする前に、とりあえず薬を飲んで少し様子をみましょう。", "しゅじゅつをするまえに、とりあえずくすりをのんですこしようすをみましょう。", "Before surgery, let's first try medicine and see how it goes.", VOC8D6)
V("試しにやってみましょう", "ためしにやってみましょう", "Let's give it a try!", "試しにやってみましょう。", "ためしにやってみましょう。", "Let's give it a try!", VOC8D6)
V("そんなつもりはありません", "そんなつもりはありません", "That's not what I meant / I didn't intend to", "そんなつもりはありませんでした、誤解しないでください。", "そんなつもりはありませんでした、ごかいしないでください。", "I didn't mean it that way, please don't misunderstand.", VOC8D6)
V("困ったときはお互い様です", "こまったときはおたがいさまです", "We help each other at difficult times", "困ったときはお互い様です。", "こまったときはおたがいさまです。", "We help each other at difficult times.", VOC8D6)
V("申し訳ありませんが、これをコピーしてください", "もうしわけありませんが、これをコピーしてください", "Would you kindly make a copy of this for me?", "申し訳ありませんが、これをコピーしてください。", "もうしわけありませんが、これをコピーしてください。", "I'm sorry to trouble you, but could you make a copy of this?", VOC8D6)
V("悪いけど、そこの雑誌を取ってくれる？", "わるいけど、そこのざっしをとってくれる？", "Would you get me that magazine?", "悪いけど、お茶、入れてくれる？", "わるいけど、おちゃ、いれてくれる？", "Sorry to bother you, but could you make some tea?", VOC8D6)
V("ノリが悪い人", "ノリがわるいひと", "Someone who never joins in / killjoy", "彼はノリが悪い人だ。", "かれはノリがわるいひとだ。", "He's a person who never gets into the mood.", VOC8D6)
V("ノリがいい", "ノリがいい", "Good beat / lively", "この曲はノリがいい。", "このきょくはノリがいい。", "This song has a great beat.", VOC8D6)
V("いまいち", "いまいち", "Not quite right / lacking something", "このケーキは、いまいちだ。", "このケーキは、いまいちだ。", "This cake is a bit lacking.", VOC8D6)
V("ばらす", "ばらす", "Expose / reveal a secret", "彼は友達の秘密をばらしてしまった。", "かれはともだちのひみつをばらしてしまった。", "He ended up revealing his friend's secret.", VOC8D6)
V("ばれる", "ばれる", "Be exposed", "うそがばれてしまった。", "うそがばれてしまった。", "My lie got exposed.", VOC8D6)
V("パクる", "パクる", "Steal / copy", "人のアイデアをパクるのはよくない。", "ひとのアイデアをパクるのはよくない。", "It's not good to steal someone's idea.", VOC8D6)
V("マジ", "マジ", "Serious / for real", "マジな話、彼は転職を考えている。", "マジなはなし、かれはてんしょくをかんがえている。", "Seriously, he's thinking about changing jobs.", VOC8D6)
V("ヤバい", "ヤバい", "Dangerous / risky / bad situation", "遅れるとヤバい。", "おくれるとヤバい。", "It'll be bad if we're late.", VOC8D6)
V("うざい", "うざい", "Annoying / bothersome", "電話してくる友達がうざい。", "でんわしてくるともだちがうざい。", "My friend who keeps calling is annoying.", VOC8D6)

# --- Grammar Day 1: それなのに… ---
GRAM8D1 = "grammar::w8 grammar::w8d1 jlpt::n2 type::grammar"
G("それなのに", "それなのに", "explanation", "Indicates a result that is contrary to the expectation set up by the previous statement",
  [("この時計は高かった。それなのにすぐに壊れた。", "このとけいはたかかった。それなのにすぐにこわれた。", "This watch was expensive, yet it stopped working right after I bought it.")], GRAM8D1)
G("それなのに", "それなのに", "explanation", "Indicates a result that is contrary to the expectation set up by the previous statement",
  [("一生懸命勉強している。それなのに成績はよくならない。", "いっしょうけんめいべんきょうしている。それなのにせいせきはよくならない。", "I am studying very hard, but my grades have not improved.")], GRAM8D1)
G("それでも", "それでも", "explanation", "Introduces an opinion or result that runs counter to the situation just described",
  [("外は大雨だ。それでも出かけないといけない。", "そとはおおあめだ。それでもでかけないといけない。", "It is raining very hard but I have to go out.")], GRAM8D1)
G("それでも", "それでも", "explanation", "Introduces an opinion or result that runs counter to the situation just described",
  [("みんなに反対されている。それでも私は彼と結婚したい。", "みんなにはんたいされている。それでもわたしはかれとけっこんしたい。", "Although everyone is against me, I still want to marry him.")], GRAM8D1)
G("それなら(ば)", "それなら(ば)", "explanation", "Acknowledging the previous statement and making a decision or suggestion based on it",
  [("「道がすごく渋滞しているようだよ。」「それなら、電車で行こう。」", "「みちがすごくじゅうたいしているようだよ。」「それなら、でんしゃでいこう。」", "\"The traffic looks bad.\" \"Well then let's go by train.\"")], GRAM8D1)
G("それなら(ば)", "それなら(ば)", "explanation", "Acknowledging the previous statement and making a decision or suggestion based on it",
  [("「今、それ、やりたくない。」「それならやらなくていいよ。」", "「いま、それ、やりたくない。」「それならやらなくていいよ。」", "\"I don't want to do that right now.\" \"Then you don't have to do it.\"")], GRAM8D1)
G("それで", "それで", "explanation", "Introduces a result caused by the previous statement, or draws out more of what the other person is saying",
  [("父は働きすぎた。それで病気になった。", "ちちはたらきすぎた。それでびょうきになった。", "My dad worked so hard he became ill.")], GRAM8D1)
G("それで", "それで", "explanation", "Introduces a result caused by the previous statement, or draws out more of what the other person is saying",
  [("「田中君、インフルエンザにかかったんだって。」「それで学校を休んだんだね。」", "「たなかくん、インフルエンザにかかったんだって。」「それでがっこうをやすんだんだね。」", "\"I heard Mr. Tanaka has got the flu.\" \"I guess that is why he didn't come to school.\"")], GRAM8D1)
G("それで", "それで", "explanation", "Introduces a result caused by the previous statement, or draws out more of what the other person is saying",
  [("「田中君にお金を貸してくれって言われたんだ。」「へえー。それで、貸してあげたの？」", "「たなかくんにおかねをかしてくれっていわれたんだ。」「へえー。それで、かしてあげたの？」", "\"Tanaka-kun asked me if I would lend him some money.\" \"Well did you?\"")], GRAM8D1)
G("それで", "それで", "explanation", "Introduces a result caused by the previous statement, or draws out more of what the other person is saying",
  [("「今日、面接を受けたんだ。」「で、どうだった？」", "「きょう、めんせつをうけたんだ。」「で、どうだった？」", "\"I had an interview today.\" \"How was it?\"")], GRAM8D1)

# --- Grammar Day 2: そういえば… ---
GRAM8D2 = "grammar::w8 grammar::w8d2 jlpt::n2 type::grammar"
G("それが", "それが", "explanation", "Used to introduce a fact that contradicts what the other person thinks or expects",
  [("「お嬢さん、もう大学をご卒業されましたでしょう？」「それが、まだなんですよ。」", "「おじょうさん、もうだいがくをごそつぎょうされましたでしょう？」「それが、まだなんですよ。」", "\"Your daughter must have graduated from university by now, right?\" \"Actually, not yet.\"")], GRAM8D2)
G("それが", "それが", "explanation", "Used to introduce a fact that contradicts what the other person thinks or expects",
  [("たばこをやめると誓った。それが、たった三日でまた吸ってしまった。", "たばこをやめるとちかった。それが、たったみっかでまたすってしまった。", "I vowed to quit smoking but I gave up after 3 days.")], GRAM8D2)
G("そこで", "そこで", "explanation", "Used to propose an action or suggest a solution based on the previous situation",
  [("明日は車が混むらしい。そこで我々は朝早く出発するつもりだ。", "あしたはくるまがこむらしい。そこでわれわれはあさはやくしゅっぱつするつもりだ。", "The traffic will probably be bad tomorrow so we are thinking of leaving early.")], GRAM8D2)
G("そこで", "そこで", "explanation", "Used to propose an action or suggest a solution based on the previous situation",
  [("「今度アメリカに旅行します。そこでお願いがあるのですが……。」", "「こんどアメリカにりょこうします。そこでおねがいがあるのですが……。」", "\"I am going on a trip to America. In connection with that, I want to ask you for a favor.\"")], GRAM8D2)
G("そういえば", "そういえば", "explanation", "Used to recall information related to the topic just mentioned",
  [("「そういえば、田中君、元気かな？」", "「そういえば、たなかくん、げんきかな？」", "\"By the way, I wonder how Tanaka-kun is doing?\"")], GRAM8D2)
G("そういえば", "そういえば", "explanation", "Used to recall information related to the topic just mentioned",
  [("「いい家ですね。そういえば、お父様は設計士さんでしたよね。」", "「いいいえですね。そういえば、おとうさまはせっけいしさんでしたよね。」", "\"It's a very nice house. When I think of it, isn't your father an architect?\"")], GRAM8D2)
G("それはそうと", "それはそうと", "explanation", "Used to abruptly change the topic",
  [("「今日の授業、おもしろかったね。」「うん、すごくためになった。それはそうと、今度の試験いつだっけ？」", "「きょうのじゅぎょう、おもしろかったね。」「うん、すごくためになった。それはそうと、こんどのしけんいつだっけ？」", "\"Today's class was interesting, wasn't it?\" \"Yeah, I learned a lot. By the way, when is the next exam?\"")], GRAM8D2)
G("それはそうと", "それはそうと", "explanation", "Used to abruptly change the topic",
  [("「春になりましたね。それはそうと、田中さんの息子さん、大学受かったでしょうか。」", "「はるになりましたね。それはそうと、たなかさんのむすこさん、だいがくうかったでしょうか。」", "\"It feels like spring, doesn't it? By the way, did Mr. Tanaka's son get into university?\"")], GRAM8D2)

# --- Grammar Day 3: だって… ---
GRAM8D3 = "grammar::w8 grammar::w8d3 jlpt::n2 type::grammar"
G("すなわち", "すなわち", "explanation", "Restating something in different words",
  [("「母の兄、すなわち僕のおじですが……」", "「ははのあに、すなわちぼくのおじですが……」", "\"My mother's older brother, in other words my uncle...\"")], GRAM8D3)
G("すなわち", "すなわち", "explanation", "Restating something in different words",
  [("このペットボトルには1,000ミリリットル、すなわち1リットルの水が入っています。", "このペットボトルには1,000ミリリットル、すなわち1リットルのみずがはいっています。", "In this PET bottle there are 1,000mL of water, in other words there is a liter.")], GRAM8D3)
G("あるいは", "あるいは", "explanation", "Presenting an alternative between two options",
  [("ファックス、あるいはメールでお知らせください。", "ファックス、あるいはメールでおしらせください。", "Please respond by fax or e-mail.")], GRAM8D3)
G("あるいは", "あるいは", "explanation", "Presenting an alternative between two options",
  [("来週の火曜日の午後はどうですか。あるいは水曜日の午前でもかまいませんが……。", "らいしゅうのかようびのごごはどうですか。あるいはすいようびのごぜんでもかまいませんが……。", "How about the afternoon of Tuesday next week, or Wednesday morning?")], GRAM8D3)
G("だが", "だが", "explanation", "Formal way to say \"but\" or \"however\"",
  [("これは難しい挑戦だ。だが失敗を恐れてはいけない。", "これはむずかしいちょうせんだ。だがしっぱいをおそれてはいけない。", "This is a difficult challenge, but I cannot be worried about messing up.")], GRAM8D3)
G("だが", "だが", "explanation", "Formal way to say \"but\" or \"however\"",
  [("生活は貧しい。だが幸せだ。", "せいかつはまずしい。だがしあわせだ。", "We are poor but happy.")], GRAM8D3)
G("だって", "だって", "explanation", "Used to state a reason in a casual or defensive manner",
  [("「何を怒っているの？」「だって、約束を破ったじゃないか。」", "「なにをおこっているの？」「だって、やくそくをやぶったじゃないか。」", "\"Why are you mad?\" \"You broke your promise!\"")], GRAM8D3)
G("だって", "だって", "explanation", "Used to state a reason in a casual or defensive manner",
  [("「テストの点、よかったんだって？」「うん。だってやさしかったんだもん。」", "「テストのてん、よかったんだって？」「うん。だってやさしかったんだもん。」", "\"I heard you did well on the exam.\" \"Yeah, it was easy.\"")], GRAM8D3)

# --- Grammar Day 4: ということは… ---
GRAM8D4 = "grammar::w8 grammar::w8d4 jlpt::n2 type::grammar"
G("ということは", "ということは", "explanation", "Summarizing or judging based on preceding information",
  [("彼はまだ来ませんね。ということは、欠席ということですね。", "かれはまだきませんね。ということは、けっせきということですね。", "He hasn't come. That means he's absent.")], GRAM8D4)
G("ということは", "ということは", "explanation", "Summarizing or judging based on preceding information",
  [("「私はもうお酒を飲めます。」「ということは二十歳を過ぎてるんだね。」", "「わたしはもうおさけをのめます。」「ということははたちをすぎてるんだね。」", "\"I can drink now.\" \"That means you're over twenty.\"")], GRAM8D4)
G("というのは", "というのは", "explanation", "Explaining the reason for the previous statement",
  [("今日は家を出られないんです。というのは父の具合が悪くなりまして…。", "きょうはいえをでられないんです。というのはちちのぐあいがわるくなりまして…。", "I can't leave home today. The reason is that my father got sick...")], GRAM8D4)
G("というのは", "というのは", "explanation", "Explaining the reason for the previous statement",
  [("ぼくは卵を食べないんです。というのは、アレルギーがあるんですよ。", "ぼくはたまごをたべないんです。というのは、アレルギーがあるんですよ。", "I don't eat eggs. The reason is I have an allergy.")], GRAM8D4)
G("したがって", "したがって", "explanation", "A formal consequence resulting from the previous statement",
  [("彼はまじめで誠実な人だ。したがってみんなから信頼されている。", "かれはまじめでせいじつなひとだ。したがってみんなからしんらいされている。", "He is a diligent and sincere person. Therefore, he is trusted by everyone.")], GRAM8D4)
G("したがって", "したがって", "explanation", "A formal consequence resulting from the previous statement",
  [("教授は急用で来られません。したがって講義は中止です。", "きょうじゅはきゅうようでこられません。したがってこうぎはちゅうしです。", "The professor cannot come due to an urgent matter. Therefore, the lecture is cancelled.")], GRAM8D4)
G("ただし", "ただし", "explanation", "Adding an exception or condition to the previous statement",
  [("全商品3割引です。ただし、この棚の商品は除きます。", "ぜんしょうひん3わりびきです。ただし、このたなのしょうひんはのぞきます。", "All items are at a 30% discount except those on this shelf.")], GRAM8D4)
G("ただし", "ただし", "explanation", "Adding an exception or condition to the previous statement",
  [("明日は9時に集合です。ただし、雨の場合は中止です。", "あしたは9じにしゅうごうです。ただし、あめのばあいはちゅうしです。", "Please assemble at 9 o'clock tomorrow morning unless it rains.")], GRAM8D4)
G("ただ", "ただ", "explanation", "A related casual/plain form of ただし -- adds a caveat to a positive statement, or a worry/concern to a settled one",
  [("品はいい。ただ値段が高すぎる。", "しなはいい。ただねだんがたかすぎる。", "The quality is good, but it is too expensive.")], GRAM8D4)
G("ただ", "ただ", "explanation", "A related casual/plain form of ただし -- adds a caveat to a positive statement, or a worry/concern to a settled one",
  [("ぼくはかまわない。ただ妻が何と言うか。", "ぼくはかまわない。ただつまがなんというか。", "I do not mind, but I do not know what my wife would say.")], GRAM8D4)

# --- Grammar Day 5: もっとも… ---
GRAM8D5 = "grammar::w8 grammar::w8d5 jlpt::n2 type::grammar"
G("もっとも", "もっとも", "explanation", "Adding an exception or condition that softens the previous statement",
  [("検査の前夜から飲食禁止です。もっとも水は飲んでもかまいません。", "けんさのぜんやからいんしょくきんしです。もっともみずはのんでもかまいません。", "No food is allowed from the night before the physical examination, except water.")], GRAM8D5)
G("もっとも", "もっとも", "explanation", "Adding an exception or condition that softens the previous statement",
  [("全員が参加しなければなりません。もっとも病気の場合は別です。", "ぜんいんがさんかしなければなりません。もっともびょうきのばあいはべつです。", "Everyone has to attend except those who are sick.")], GRAM8D5)
G("なお", "なお", "explanation", "Adding supplementary information, which does not need to be related to what came before",
  [("この件の説明は以上です。なお、詳細についてはプリントをご覧ください。", "このけんのせつめいはいじょうです。なお、しょうさいについてはプリントをごらんください。", "I am finished explaining this matter. Please look at the handout for details.")], GRAM8D5)
G("なお", "なお", "explanation", "Adding supplementary information, which does not need to be related to what came before",
  [("今日はこれで終わります。なお次回の日時は……。", "きょうはこれでおわります。なおじかいのにちじは……。", "We are finished for today. Our next session will be...")], GRAM8D5)
G("さて", "さて", "explanation", "Shifting the conversation to a new subject",
  [("これで授業を終わります。さて来週の予定ですが……。", "これでじゅぎょうをおわります。さてらいしゅうのよていですが……。", "Today's lesson is over. Now, next week we will be covering...")], GRAM8D5)
G("さて", "さて", "explanation", "Shifting the conversation to a new subject",
  [("以上、今日のニュースをお伝えしました。さて次に天気予報です。", "いじょう、きょうのニュースをおつたえしました。さてつぎにてんきよほうです。", "That was today's news. Now, we will look at the weather forecast for tomorrow.")], GRAM8D5)
G("すると", "すると", "explanation", "Action A leads directly to result B, or drawing a conclusion from what was just said",
  [("薬を塗った。すると痛みが治まった。", "くすりをぬった。するといたみがおさまった。", "The pain stopped as soon as I put some medicine on the wound.")], GRAM8D5)
G("すると", "すると", "explanation", "Action A leads directly to result B, or drawing a conclusion from what was just said",
  [("窓を開けた。すると、蛾が入ってきた。", "まどをあけた。すると、ががはいってきた。", "A moth came in right after I opened the window.")], GRAM8D5)
G("すると", "すると", "explanation", "Action A leads directly to result B, or drawing a conclusion from what was just said",
  [("「私は外出していました。」「すると、家には誰もいなかったんですね。」", "「わたしはがいしゅつしていました。」「すると、いえにはだれもいなかったんですね。」", "\"I was out.\" \"So, no one was at home. Is that right?\"")], GRAM8D5)

# --- Grammar Day 6: おまけに… ---
GRAM8D6 = "grammar::w8 grammar::w8d6 jlpt::n2 type::grammar"
G("要するに", "ようするに", "explanation", "Summarizing or simplifying information",
  [("試合に大負けした。要するに、相手のチームと力の差があったということだ。", "しあいにおおまけした。ようするに、あいてのチームとちからのさがあったということだ。", "We were badly defeated. In short the other team was a lot better.")], GRAM8D6)
G("要するに", "ようするに", "explanation", "Summarizing or simplifying information",
  [("彼は一度も入賞しなかった。要するに、才能がなかったということだ。", "かれはいちどもにゅうしょうしなかった。ようするに、さいのうがなかったということだ。", "He never won a prize. In short, he had no talent.")], GRAM8D6)
G("しかも", "しかも", "explanation", "Adding more information, usually of the same positive or negative sentiment",
  [("彼女は美人で頭がいい。しかも性格もいい。", "かのじょはびじんであたまがいい。しかもせいかくもいい。", "She is smart and beautiful and even has a nice personality.")], GRAM8D6)
G("しかも", "しかも", "explanation", "Adding more information, usually of the same positive or negative sentiment",
  [("先日治まったホテルは、古くて高かった。しかもサービスが悪かったので、もう二度と行かない。", "せんじつとまったホテルは、ふるくてたかかった。しかもサービスがわるかったので、もうにどといかない。", "The hotel I stayed in the other day was shabby and yet expensive. Moreover the service was bad. I will never go back there again.")], GRAM8D6)
G("おまけに", "おまけに", "explanation", "Same function as しかも, but more colloquial",
  [("日本の夏は暑いし、おまけに湿気も多いです。", "にほんのなつはあついし、おまけにしっけもおおいです。", "The summer here in Japan is hot and humid.")], GRAM8D6)
G("おまけに", "おまけに", "explanation", "Same function as しかも, but more colloquial",
  [("あのそば屋は高いしまずい。おまけにサービスも悪い。", "あのそばやはたかいしまずい。おまけにサービスもわるい。", "The soba in that shop is expensive and not good, let alone the service.")], GRAM8D6)
G("ちなみに", "ちなみに", "explanation", "Adding a small, incidental piece of information",
  [("最近は、ペットを飼う家が増えているようです。ちなみに、うちにも犬が1匹とネコが2匹います。", "さいきんは、ペットをかういえがふえているようです。ちなみに、うちにもいぬが1ぴきとネコが2ひきいます。", "There're a lot of people who have pets these days. By the way, I have one dog and two cats.")], GRAM8D6)
G("ちなみに", "ちなみに", "explanation", "Adding a small, incidental piece of information",
  [("燃えるゴミは月曜日と木曜日、燃えないゴミは金曜日に出してください。ちなみに資源ごみの収集日は第3水曜日です。", "もえるゴミはげつようびともくようび、もえないゴミはきんようびにだしてください。ちなみにしげんごみのしゅうしゅうびはだい3すいようびです。", "Please put out burnable garbage on Mondays and Thursdays, and nonburnable on Fridays. Incidentally, recyclable garbage is collected on the third Wednesday of each month.")], GRAM8D6)

# --- Grammar Bonus: 敬語 (Keigo) — お礼を言う② ---
GRAM8DE = "grammar::w8 grammar::w8dExtra jlpt::n2 type::keigo"
G("お招きくださいました／ご招待くださいました", "おまねきくださいました／ごしょうたいくださいました", "explanation", "Keigo for 呼んでくれました (kindly invited me)",
  [("先生が私をパーティーにお招きくださいました。", "せんせいがわたしをパーティーにおまねきくださいました。", "My teacher was kind enough to invite me to the party."),
   ("先生が私をパーティーに呼んでくれました。", "せんせいがわたしをパーティーによんでくれました。", "My teacher invited me to the party.")], GRAM8DE)
G("来てくださいました／お越しくださいました／おいでくださいました", "きてくださいました／おこしくださいました／おいでくださいました", "explanation", "Keigo for 来てくれました (kindly came for me)",
  [("先生が私のためにお越しくださいました。", "せんせいがわたしのためにおこしくださいました。", "My teacher was kind enough to come for my sake."),
   ("先生が私のために来てくれました。", "せんせいがわたしのためにきてくれました。", "My teacher came for my sake.")], GRAM8DE)

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
        "# Week 8 (Sou Matome N2) — Japanese vocabulary: Kanji/Vocabulary words",
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
        "# Week 8 (Sou Matome N2) — Japanese grammar and usage: Grammar patterns",
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

    with open(os.path.join(base, "week8-v3-vocabulary.tsv"), "w", encoding="utf-8") as f:
        f.write(vocab_tsv)
    with open(os.path.join(base, "week8-v3-grammar-usage.tsv"), "w", encoding="utf-8") as f:
        f.write(grammar_tsv)
    print("Wrote TSVs.")

    if not errs:
        model1 = make_model(MODEL1_ID, "Japanese vocabulary")
        model2 = make_model(MODEL2_ID, "Japanese grammar and usage")
        n1 = build_apkg(vocab_tsv, DECK1_ID, "Japanese N2 Vocabulary", model1,
                         os.path.join(base, "week8-v3-vocabulary.apkg"))
        n2 = build_apkg(grammar_tsv, DECK2_ID, "Japanese N2 Grammar & Usage", model2,
                         os.path.join(base, "week8-v3-grammar-usage.apkg"))
        print(f"Wrote apkg: vocabulary={n1} notes, grammar-usage={n2} notes")
