# -*- coding: utf-8 -*-
"""城镇台词原稿（2026-11-27，依据《开局参与感与熔炼重铸 · 想法策划书》与 LORE.md）。
python town_ref/lines_src.py 导出 town_ref/lines.json；配音（只配英语）照 town_ref/vo/VO-BRIEF.md 生成。
每条：(编号, speaker, 中文, English, 表演指令)。"""
import json
import os

SPEAKERS = {  # speaker: (显示名, 英文名, 声线, 角色基调)
    "priest": ("神父", "Father", "echo", "A village priest in his sixties: kind, patient, a little tired, speaks like he has buried many people and still believes."),
    "elder": ("村长", "Elder", "alloy", "A plain-spoken village elder: practical, warm, a farmer's voice, worried about his people."),
    "inquisitor": ("审判官", "Inquisitor", "cedar", "A Church inquisitor: cold, precise, never shouts; every sentence sounds like a verdict."),
    "edgewalker": ("兜帽人", "Hooded Man", "verse", "A senior Edgewalker hiding in plain sight: low, quick, wry, a man used to running."),
    "witch": ("女巫", "The Witch", "shimmer", "A wounded young woman the Church calls a witch: tired, clear, unafraid; quiet anger under it."),
    "farmwife": ("农妇", "Farmwife", "coral", "A busy farm woman gossiping over a fence: fast, a bit nervous, lowers her voice for secrets."),
    "farmer": ("农夫", "Farmer", "ash", "A gruff farmer: slow, few words, superstitious."),
    "youth": ("少年", "Lad", "nova", "An excitable teenage boy who repeats rumours as if they were adventures."),
    "bard": ("吟游诗人", "Bard", "ballad", "A wandering bard singing a fragment of an old song, unaccompanied, half-spoken, half-sung."),
    "watchman": ("守夜人", "Watchman", "onyx", "An old night watchman: hoarse, steady, a lantern-carrier who has seen strange things."),
    "child": ("孩子", "Child", "marin", "A lost child of about eight: small voice, shy, then brave."),
    "narrator": ("旁白", "Narrator", "fable", "An old storyteller reading scripture aloud: slow, unhurried, reverent, close to the microphone (same narrator as the onboarding)."),
    "servant": ("罪仆", "Sin-servant", "sage", "A minor demon of the Seventy-Two speaking through candle smoke: soft, courteous, tempting, never hurried."),
}

L = []


def add(pid, sp, zh, en, d):
    L.append((pid, sp, zh, en, d))


# ---------------------------------------------------------------- 神父（24）
add("PR01", "priest", "孩子，你醒了。这里是你的故乡，你在这里出生，也在这里受洗。", "You're awake, child. This is your home; you were born here, and baptised here.", "Gentle, welcoming, a hand on the shoulder.")
add("PR02", "priest", "镇子外面不太平。先拿着这些，够你撑过头几天。", "It isn't safe beyond the town. Take these; they'll see you through the first days.", "Handing over a bundle, matter-of-fact.")
add("PR03", "priest", "教堂前的圣火会护着你，直到你站稳脚跟。", "The holy fire before the church will shelter you until you find your feet.", "Reassuring.")
add("PR04", "priest", "每天来一趟，教堂总有一份口粮给你。", "Come by each day. The church always keeps a ration for you.", "Kind, routine.")
add("PR05", "priest", "今天的口粮。别空着肚子出门。", "Today's ration. Don't go out on an empty stomach.", "Brief, fatherly.")
add("PR06", "priest", "你今天已经领过了。明天再来吧。", "You've had yours today. Come back tomorrow.", "Amused, patient.")
add("PR07", "priest", "要学驱魔，先学会看。恶魔留下的痕迹，比它本身好找。", "To learn exorcism, first learn to look. A demon's traces are easier to find than the demon.", "Teaching, slow.")
add("PR08", "priest", "采三样东西来：清水、盐、圣火的灰。我教你炼一瓶圣水。", "Bring me three things: clean water, salt, and ash from the holy fire. I'll teach you to make holy water.", "Practical, counting on fingers.")
add("PR09", "priest", "粮仓出事了。跟我来，别碰任何发黑的东西。", "Something's wrong in the granary. Follow me, and touch nothing that has gone black.", "Urgent but controlled.")
add("PR10", "priest", "苍蝇不会无缘无故聚成团。记下来，这是第一处。", "Flies don't swarm for no reason. Note it; that's the first sign.", "Quiet, crouching.")
add("PR11", "priest", "麦子从里面烂了，外面还是金的。贪吃的东西就是这样吃的。", "The grain rotted from the inside; the outside is still gold. That is how gluttony eats.", "Disgusted, low.")
add("PR12", "priest", "这个印记……三道横，一只眼。我见过它。", "This mark... three bars and an eye. I've seen it before.", "Recognition, a chill.")
add("PR13", "priest", "是蝇王。别西卜的一个化身。它不是全力，但足够吃空一个镇子。", "It's the Lord of Flies. An avatar of Beelzebub. Not his full strength, but enough to eat a town hollow.", "Grave, certain.")
add("PR14", "priest", "图腾立在门口。用圣水点燃它，法阵才会亮。", "Set the totem at the door. Light it with holy water, or the circle won't wake.", "Instructing quickly.")
add("PR15", "priest", "法阵亮了。守住它，别让蝇群扑灭圣火！", "The circle is lit. Hold it; don't let the swarm smother the fire!", "Raised voice, rallying.")
add("PR16", "priest", "撑住，它在变弱！", "Hold on, it's weakening!", "Shouted over noise.")
add("PR17", "priest", "它跪下了。由你来裁决：消灭、放逐，还是封印。", "It kneels. The verdict is yours: destroy, banish, or seal.", "Solemn, handing over authority.")
add("PR18", "priest", "做得好。今晚镇上的人能睡个好觉了。", "Well done. The town will sleep tonight.", "Relieved, warm.")
add("PR19", "priest", "火灭了……没关系，人都还活着。粮食的事，明天再想办法。", "The fire's out... never mind. Everyone's alive. We'll sort out the grain tomorrow.", "Tired, consoling.")
add("PR20", "priest", "这瓶圣水是你自己炼的。比我给你的那瓶更管用。", "You made this holy water yourself. It'll serve you better than any I could give.", "Proud.")
add("PR21", "priest", "新手的日子结束了。这枚徽章说明你是这个镇的人。", "Your first days are over. This badge says you belong to this town.", "Ceremonial, pinning a badge.")
add("PR22", "priest", "还有这道通行符。去伊甸之门吧，但别一个人走得太深。", "And this pass. Go to the Gate of Eden, but don't walk too deep alone.", "Serious, a warning.")
add("PR23", "priest", "你身上有烛烟的味道。我不问。但别让圣卫看见。", "You smell of candle smoke. I won't ask. But don't let the guards see.", "Quiet, knowing, not judging.")
add("PR24", "priest", "愿圣火照着你回家。", "May the holy fire light your way home.", "Blessing, soft.")
# ---------------------------------------------------------------- 村长（12）
add("EL01", "elder", "回来就好。镇上的人都还记得你。", "Good to have you back. The town still remembers you.", "Warm, gruff.")
add("EL02", "elder", "告示板上有活儿。镇上缺人手，你帮一把，大家都记着。", "There's work on the notice board. We're short of hands; help out and people will remember.", "Pointing.")
add("EL03", "elder", "大家开始叫你的名字了。铁匠那边会给你便宜些。", "People are starting to say your name. The smith will give you a better price.", "Pleased.")
add("EL04", "elder", "镇东头有间空屋。你要是愿意，租下来当个家吧。", "There's an empty house at the east end. Rent it as your home, if you like.", "Offering.")
add("EL05", "elder", "这张图纸是镇上的老手艺，只给自己人。", "This pattern is the town's old craft. We only give it to our own.", "Handing it over carefully.")
add("EL06", "elder", "从今天起，你就是这个镇的守护者。", "From today on, you are this town's guardian.", "Moved, formal.")
add("EL07", "elder", "昨晚的事别往心里去。镇子挨过比这更糟的夜。", "Don't take last night to heart. This town has survived worse nights.", "Consoling.")
add("EL08", "elder", "房子塌了还能盖，人没了就没了。你救下的比你想的多。", "Houses can be rebuilt; people can't. You saved more than you think.", "Firm, kind.")
add("EL09", "elder", "这封信得送到邻镇去。路远，带上地图。", "This letter must reach the next town. It's a long road; take a map.", "Handing a letter.")
add("EL10", "elder", "收税的又来了。你帮教廷收，还是帮我们藏？我不怪你。", "The tax-men are back. Will you collect for the Church, or help us hide the grain? I won't blame you either way.", "Torn, honest.")
add("EL11", "elder", "粮价涨了一天。没事，熬过去就好。", "Grain's dear for a day. No matter; we'll get through it.", "Sighing.")
add("EL12", "elder", "镇子不大，但它是你的。", "It's not a big town, but it's yours.", "Proud, simple.")
# ---------------------------------------------------------------- 审判官（8）
add("IQ01", "inquisitor", "以教廷之名：此女与恶魔立约，明日日出，火刑。", "In the name of the Church: this woman has made a pact with demons. At sunrise, she burns.", "Proclaiming to a crowd.")
add("IQ02", "inquisitor", "谁替她求情，谁就和她同罪。", "Whoever pleads for her shares her guilt.", "Flat, threatening.")
add("IQ03", "inquisitor", "犯人跑了！封住镇口！", "The prisoner is loose! Seal the gates!", "Sharp command, not panicked.")
add("IQ04", "inquisitor", "你们跑不远的。林子也是教廷的。", "You won't get far. The woods belong to the Church too.", "Calling after them, calm.")
add("IQ05", "inquisitor", "放下她，我只记你一笔。", "Put her down, and I'll only write your name.", "Offering a cold bargain.")
add("IQ06", "inquisitor", "孤堡的墙不是为挡恶魔造的，是为挡忘了神的人。", "The walls of the Lone Fort weren't built against demons. They were built against those who forget God.", "Lecturing recruits.")
add("IQ07", "inquisitor", "每一份名单都有用。今天的邻居，明天的证人。", "Every list has its use. Today's neighbour is tomorrow's witness.", "Cold, reasonable.")
add("IQ08", "inquisitor", "……这一次算你们赢。", "...You win this time.", "Through clenched teeth, almost a whisper.")
# ---------------------------------------------------------------- 兜帽人 · 高阶边缘者（14）
add("EW01", "edgewalker", "嘘。别回头，听我说。", "Shh. Don't turn around. Listen.", "Whispering from the shadows.")
add("EW02", "edgewalker", "明早要烧的那个人没做过他们说的事。我需要人手。", "The one they're burning at dawn didn't do what they say. I need hands.", "Low, urgent.")
add("EW03", "edgewalker", "天黑以后，到刑台后面的巷子找我。", "After dark, find me in the alley behind the scaffold.", "Leaving.")
add("EW04", "edgewalker", "听好：一个人点火引开圣卫，一个人割绳，一个人挡住审判官。", "Listen: one lights a fire to draw the guards, one cuts the ropes, one holds the inquisitor.", "Planning, quick.")
add("EW05", "edgewalker", "只有你一个？那我去点火，绳子交给你。", "Just you? Then I'll light the fire. The ropes are yours.", "Wry, adapting.")
add("EW06", "edgewalker", "圣卫只打晕，别杀。他们也是被派来的。", "Knock the guards out; don't kill them. They were sent too.", "Firm.")
add("EW07", "edgewalker", "火起来了！现在！", "Fire's lit! Now!", "Shouted.")
add("EW08", "edgewalker", "绳子断了，扶她走！", "The ropes are cut, get her up!", "Urgent.")
add("EW09", "edgewalker", "她走不快。挡住后面的人！", "She can't move fast. Hold off the ones behind us!", "Running, out of breath.")
add("EW10", "edgewalker", "再往前就是林子了，撑住。", "The woods are just ahead. Hold on.", "Encouraging, panting.")
add("EW11", "edgewalker", "到了。这里他们找不到。", "We're here. They won't find us here.", "Relief, catching breath.")
add("EW12", "edgewalker", "你救的不是女巫。她是我们的人，是边缘者。", "You didn't save a witch. She's one of us. An Edgewalker.", "Revealing, steady.")
add("EW13", "edgewalker", "营地的门一直开着。想通了就来。", "The camp's door is always open. Come when you've made up your mind.", "Calm invitation.")
add("EW14", "edgewalker", "教堂的蜡烛，教廷的圣水……总有人得让他们知道，不是所有人都怕。", "The church candles, the Church's holy water... someone has to show them not everyone is afraid.", "Handing out a secret job, a half-smile.")
# ---------------------------------------------------------------- 女巫（12）
add("WI01", "witch", "谢谢你……我还以为今天就是最后一天。", "Thank you... I thought today was my last.", "Weak, sincere.")
add("WI02", "witch", "你知道所罗门王吗？他是第一个被记下名字的边缘者。", "Do you know of King Solomon? He was the first Edgewalker whose name was written down.", "Storytelling, quiet.")
add("WI03", "witch", "他和七十二位魔神立约，把它们封进柱子里。没有杀，也没有放。", "He made pacts with seventy-two demons and sealed them in pillars. He didn't kill them, and he didn't free them.", "Measured.")
add("WI04", "witch", "后来教廷拿走了那些柱子，把它们当成军械库。", "Later the Church took those pillars and turned them into an armoury.", "Bitter.")
add("WI05", "witch", "每个边缘者都分到一根柱、一位魔神。我们借它的力，它借我们的心。", "Every Edgewalker is given a pillar and a demon. We borrow its strength; it borrows our hearts.", "Matter-of-fact, sad.")
add("WI06", "witch", "教廷需要我们去打仗。打完了，就叫我们女巫。", "The Church needs us for its wars. When the war's over, it calls us witches.", "Quiet anger.")
add("WI07", "witch", "我没有杀过人。我只是不肯再替他们杀人。", "I never killed anyone. I only refused to kill for them any more.", "Firm.")
add("WI08", "witch", "镇上的人不坏。他们只是怕，而怕最好用。", "The townsfolk aren't wicked. They're afraid, and fear is easy to use.", "Thoughtful.")
add("WI09", "witch", "这是我身上唯一值钱的东西。拿着，别推辞。", "This is the only thing of value I have. Take it; don't refuse.", "Pressing it into a hand.")
add("WI10", "witch", "如果有一天你也被教廷当成怪物，来林子里找我们。", "If the Church ever calls you a monster too, come find us in the woods.", "Slow, the most important line; let it land.")
add("WI11", "witch", "你又来了。坐吧，火是暖的。", "You came back. Sit; the fire's warm.", "Friendly, at ease.")
add("WI12", "witch", "祭坛在营地后面。想清楚了再点那支黑蜡烛。", "The altar is behind the camp. Think hard before you light the black candle.", "Serious warning.")
# ---------------------------------------------------------------- 镇民：风声与道谢（18）
add("RB01", "farmwife", "你闻到没有？粮仓那边一股酸味，麦子都发黑了。", "Can you smell it? Something sour by the granary. The grain's gone black.", "Gossiping, wrinkling nose.")
add("RB02", "farmer", "苍蝇。成团成团的。冬天哪来的苍蝇。", "Flies. Swarms of them. Where do flies come from at this time of year?", "Uneasy, slow.")
add("RB03", "youth", "老约拿家的人都在闹肚子，说是吃了新磨的面！", "Old Jonah's whole family is sick. They say it was the new flour!", "Excited.")
add("RB04", "farmwife", "神父今天在粮仓门口站了好久，脸色可难看了。", "The priest stood at the granary door for ages today. He looked awful.", "Lowering voice.")
add("RH01", "farmer", "墓地的土是松的。像是有人从里面往外挖。", "The graveyard soil is loose. As if someone dug their way out.", "Superstitious, quiet.")
add("RH02", "youth", "我昨晚看见一个人站在路口，没有脸！真的，没有脸！", "Last night I saw someone standing at the crossroads with no face! Honest, no face!", "Breathless.")
add("RH03", "farmwife", "你别盯着它看……可也别背过身去。我奶奶就是这么说的。", "Don't stare at it... but don't turn your back on it either. That's what my grandmother said.", "Whispering, scared.")
add("RH04", "farmer", "今晚关好门。守夜人说狗叫了一整夜。", "Bar your door tonight. The watchman says the dogs barked all night.", "Warning.")
add("RW01", "youth", "审判官进城了！带着一车柴火！", "The inquisitor's come to town! With a whole cart of firewood!", "Running in, excited and scared.")
add("RW02", "farmwife", "广场上在搭刑台……明早要烧女巫。", "They're building a scaffold in the square... they'll burn a witch in the morning.", "Uneasy.")
add("RW03", "farmer", "那姑娘给我家孩子看过病。我不信她是女巫。", "That girl once nursed my child. I don't believe she's a witch.", "Quiet, troubled.")
add("RW04", "farmwife", "嘘，别乱说话。圣卫在听。", "Hush, watch your tongue. The guards are listening.", "Hissing.")
add("TH01", "farmwife", "谢谢你，谢谢……我还以为再也见不到家了。", "Thank you, thank you... I thought I'd never see home again.", "Crying with relief.")
add("TH02", "farmer", "欠你一条命。有事说一声。", "I owe you my life. Just say the word.", "Gruff gratitude.")
add("TH03", "youth", "你是怎么做到的？教教我！", "How did you do that? Teach me!", "Awestruck.")
add("TH04", "farmwife", "来，拿着，自家烤的。", "Here, take this. Baked it myself.", "Pressing bread on you.")
add("TH05", "farmer", "镇子能撑到今天，多亏了你这样的人。", "This town's still standing because of people like you.", "Sincere.")
add("TH06", "youth", "等我长大了，也要跟你一样！", "When I grow up, I'm going to be just like you!", "Determined.")
# ---------------------------------------------------------------- 吟游诗人（3 段吟唱）
add("BD01", "bard", "世界曾是一整块，神说要有光；后来权与力分了家，大地就碎成了七样。", "The world was whole when God said light; then Might and Authority parted, and the land broke into seven.", "Sung slowly, a ballad fragment, unaccompanied.")
add("BD02", "bard", "七位领主坐王座下，傲慢、嫉妒、贪与饱；谁拿走他们的刀，谁就拿走他们的影。", "Seven lords beneath the throne: pride, envy, greed and gluttony; who takes their blades, takes their shadows too.", "Sung, darker, slower.")
add("BD03", "bard", "所罗门戴冠走进深渊，七十二个名字带回人间；柱子立着，锁还在，钥匙在教廷的袖子里。", "Solomon wore his crown into the deep, and brought back seventy-two names; the pillars stand, the locks still hold, the key is in the Church's sleeve.", "Sung, ending on a sly spoken note.")
# ---------------------------------------------------------------- 守夜人与孩子（8）
add("WT01", "watchman", "夜里绕镇走一圈。看见什么都别出声，回来告诉我。", "Walk the town once tonight. Whatever you see, keep quiet and tell me.", "Hoarse, serious.")
add("WT02", "watchman", "墓地那边的灯总是先灭。你去看看。", "The lamps by the graveyard always go out first. Go and look.", "Uneasy.")
add("WT03", "watchman", "土松了？……那就是了。要出事了。", "The soil's loose?... Then that's it. Something's coming.", "Grim.")
add("WT04", "watchman", "走完了？好。拿去，这是守夜的钱。", "All the way round? Good. Here, a watchman's wage.", "Approving.")
add("CH01", "child", "你是来找我的吗？", "Have you come to find me?", "Small, hopeful.")
add("CH02", "child", "我迷路了，是那个戴兜帽的叔叔给我饭吃。", "I got lost, and the man in the hood gave me food.", "Shy.")
add("CH03", "child", "他说别告诉神父，可我觉得他是好人。", "He said not to tell the priest, but I think he's a good man.", "Whispering a secret.")
add("CH04", "child", "我们回家吧。我不怕了。", "Let's go home. I'm not scared any more.", "Brave.")
# ---------------------------------------------------------------- 罪仆（6）
add("SV01", "servant", "是谁逆着画了圈，点了黑烛……啊，是你。", "Who drew the circle backwards and lit the black candle... ah. It's you.", "Emerging from smoke, pleased.")
add("SV02", "servant", "教廷给你的是锁链和名单。我们给你的是名字。", "The Church gave you chains and lists. We give you a name.", "Silky.")
add("SV03", "servant", "代价？一半的血，一枚印。很公道。", "The price? Half your blood, and one mark. Very fair.", "Courteous, like a merchant.")
add("SV04", "servant", "签吧。从此教廷的火烧不到你，只会追着你。", "Sign. From now on the Church's fire can't burn you. It can only chase you.", "Tempting, slow.")
add("SV05", "servant", "契成。欢迎回家。", "It is done. Welcome home.", "Satisfied, almost tender.")
add("SV06", "servant", "犹豫了？没关系，蜡烛还会再亮。", "Hesitating? No matter. The candle will light again.", "Patient, amused.")
# ---------------------------------------------------------------- 空缺者那场（3，旁白式提示由神父与守夜人分担）
add("HO01", "watchman", "它们从墓地出来了！看着它们，别让它们靠近镇口！", "They're coming out of the graveyard! Watch them; don't let them reach the gate!", "Shouting, ringing a bell.")
add("HO02", "watchman", "有人被拖走了！快追！", "Someone's been dragged off! After them!", "Alarm.")
add("HO03", "priest", "最后那个……它在显形。小心，它不再怕光了。", "That last one... it's taking shape. Careful. It doesn't fear the light any more.", "Tense, warning.")
add("HO04", "priest", "天亮了。它们回到土里去了。", "Dawn. They've gone back into the earth.", "Exhausted relief.")

# ---------------------------------------------------------------- 初见旁白：第一次走进一个群系（19）
add("EX01", "narrator", "平原上的风一直吹，像在数还有多少人没有回家。", "The wind on the plains never stops, as if counting who has not come home.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX02", "narrator", "林子记得每一个走进来的人，也记得没走出去的。", "The forest remembers everyone who walks in, and everyone who never walked out.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX03", "narrator", "原野的花开得很乱，好像没人告诉它们世界碎过。", "The wildflowers grow in disorder, as if no one told them the world had broken.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX04", "narrator", "雾月花在白天也发着光，像替谁守着一盏灯。", "The mistmoon flowers glow even by day, like a lamp kept for someone.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX05", "narrator", "这片林子金黄得像祭坛上的麦，丰饶是给活人的。", "This wood is gold like grain upon an altar. Plenty is for the living.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX06", "narrator", "沙漠什么都不留，连脚印也只借给你一会儿。", "The desert keeps nothing. Even your footprints are only lent.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX07", "narrator", "雪把一切都盖平了，好坏都一样白。", "The snow levels everything. Good and bad, all the same white.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX08", "narrator", "云杉底下，地热在冒气，大地还没有睡着。", "Under the spruce the earth still steams. The land has not yet slept.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX09", "narrator", "平顶的山像被一刀削过，那是神陨那天留下的。", "The flat-topped hills look cut by a single blade, a scar from the day God fell.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX10", "narrator", "风把沙漠一层层剥开，底下是更老的颜色。", "The wind peels the desert layer by layer, down to older colours.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX11", "narrator", "焦木还站着，只是不再长叶子了。", "The burnt trees still stand. They simply no longer grow leaves.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX12", "narrator", "石头站成了林子，比树还耐心。", "Here the stones stand like a forest, more patient than trees.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX13", "narrator", "高原上的颜色不对。这里的东西在等人犯错。", "The colours on this plateau are wrong. Things here wait for you to make a mistake.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX14", "narrator", "冰原上的尖塔一年长一寸，没有人知道它们要去哪里。", "The ice spires grow an inch a year. No one knows where they are going.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX15", "narrator", "山顶离天近，离人远。", "The summit is close to heaven, and far from people.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX16", "narrator", "大地在这里流血，流成了火。", "Here the land bleeds, and the blood is fire.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX17", "narrator", "这里打过的仗还没打完，只是人都死了。", "The war fought here has not ended. Only the people have.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX18", "narrator", "海崖把大陆的边缘咬得参差不齐。", "The sea cliffs have gnawed the edge of the continent ragged.", "Quiet, first sight of a new land; leave a breath at the end.")
add("EX19", "narrator", "水从碎裂的大地之间流过，把各国连在一起。", "Water runs between the broken lands and ties the nations together.", "Quiet, first sight of a new land; leave a breath at the end.")

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = {"source": "城镇台词（2026-11-27，依据开局参与感策划书与 LORE.md）", "speakers": {k: {"zh": v[0], "en": v[1], "voice": v[2], "tone": v[3]} for k, v in SPEAKERS.items()},
           "lines": [{"id": p, "speaker": s, "zh": z, "en": e, "direction": d, "voiced": True} for p, s, z, e, d in L]}
    ids = [p for p, *_ in L]
    assert len(ids) == len(set(ids))
    json.dump(out, open(os.path.join(here, "lines.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(L), "lines")
