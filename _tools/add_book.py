# -*- coding: utf-8 -*-
"""《破碎大陆手记》—— 一本写在游戏里的书，讲清全部玩法。

网页图鉴是给人在屏幕外查的；这本是给人在世界里翻的。所以两者分工不同：
图鉴摊开所有数值，这本只讲**你需要知道才能玩下去的东西** ——
怎么开始、每个体系是什么、按哪个键、代价是什么。

页面容量：原版书一页约 14 行，中文一行约 9 个字，所以一页 120 字上下就满。
这里每页都按这个尺度写，宁可多分几页，也不让文字被截断。

数值不在这里手抄：五等佣兵读 `_squad.json`，七柱读 `_pact.json` ——
和图鉴同源，改了数值两边一起变。
"""
import io
import json
import os
import sys

DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"
FUNC = os.path.join(DP, "data/rpg/function")
GIVE = os.path.join(FUNC, "command/give/item.mcfunction")

Q = json.load(io.open("../_squad.json", encoding="utf-8"))
P = json.load(io.open("../_pact.json", encoding="utf-8"))

TITLE = "破碎大陆手记"
AUTHOR = "无名的边缘者"

# 书页里反复用到的几种口吻
G = "#7A6A55"        # 正文旁注的暗棕
K = "#8B2500"        # 强调用的暗红
B = "#1B4F72"        # 章节名的深蓝


def t(text, colour=None, bold=False, italic=False):
    d = {"text": text}
    if colour:
        d["color"] = colour
    if bold:
        d["bold"] = True
    if italic:
        d["italic"] = True
    return d


def page(*parts):
    """一页 = 一个文本组件列表。原样返回，序列化留到最后。"""
    return list(parts)


def esc(v):
    """SNBT 的双引号字符串。

    真正的换行必须写成 `\\n` 两个字符：mcfunction 是按行读的，
    塞一个真换行进去，这条命令当场断成两截。
    """
    return (v.replace(BS, BS * 2)
             .replace('"', BS + '"')
             .replace(chr(10), BS + "n"))


def snbt(v):
    """把组件转成 SNBT。

    1.21.5 之后文本组件在物品里是**以 NBT 存的**，写成 JSON 字符串会被
    当作字面文字 —— 那正是书页显示成一堆源码的原因。
    """
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return '"' + esc(v) + '"'
    if isinstance(v, list):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ",".join(k + ":" + snbt(x) for k, x in v.items()) + "}"
    return str(v)


def head(n, name):
    return t("卷%s · %s\n\n" % (n, name), B, True)


# 一条线正好占满书页一行：书页宽 114 像素，默认字体的 `-` 与 `+` 各 6 像素，
# 19 个字符 = 114。所以它前后的文字必然分行 —— 排版靠它，不靠堆 \n。
# 分隔线。18 个字符 = 108 像素，书页宽 114，正好一行。
#
# 它**必须**自带换行。我一度以为一条接近满宽的线会自己占住一行 ——
# 不会：书页的折行是按字符来的，`-` 的连续段会被从中间劈开，
# 变成 "+---------" / "-------+" 两截，比不加线还难看。
# 模拟一遍折行就看见了。
BAR = "+----------------+"


def rule():
    return t("\n" + BAR + "\n", "dark_gray")


def vol(n, name):
    """卷号 + 标题。与罪器名牌同一套：方括号标签加粗上色，名字用青色。"""
    return [t("[卷%s]" % n, K, True), t(name, "aqua")]   # 换行由下一条 rule 带


def aside(text):
    """页脚那句旁白。留给读者记住的一句，不承载规则。"""
    return t("▸ " + text, G, italic=True)


def build_pages():
    """给玩家的手册。

    每页：卷号 / 分隔线 / 正文 / 分隔线 / 一句旁白。
    正文交给书页自己折行 —— 手动断句只会断得难看。
    """
    p = []

    # ---- 扉页 ----
    # 扉页只有一件事要做：定调子。所以留白，不塞内容。
    p.append(page(
        t("\n   破 碎 大 陆\n", K, True),
        rule(),
        t("   Eretz Ha-Shevarim\n\n", G, italic=True),
        t("这里的每一样东西，都要向你收费。", G, italic=True),
        rule(),
        t("   先读完这本。", G, italic=True)))

    p.append(page(
        *vol("零", "开局"), rule(),
        t("对着聊天栏敲一次：\n"),
        t("/function rpg:command/give/box\n", "#DAA520"),
        t("几个潜影盒到手，武器、护甲、材料都在里面。"),
        rule(),
        aside("剩下的，边走边看。")))

    # ---- 一、圣与魔 ----
    p.append(page(
        *vol("一", "两种兵器"), rule(),
        t("你捡到的东西分两路。"),
        t("圣器", "#DAA520", True), t("护着你；"),
        t("魔器", K, True), t("更强，但它认主 —— 认的不是你。"),
        rule(),
        aside("握久了，它开始把你当成它的。")))

    p.append(page(
        *vol("一", "魔化"), rule(),
        t("屏幕正下方那条就是，满格 100。\n"),
        t("握着魔器它涨，握着圣器它退，两手都拿就互相抵消。"),
        t("打村子里那些空壳，涨得最快。"),
        rule(),
        aside("它不会自己降下去。")))

    p.append(page(
        *vol("一", "什么算圣器"), rule(),
        t("拿在手上或穿在身上都算：驱魔图腾、驱魔圣水、驱魔替死人偶、驱魔天启星、"
          "朗基努斯之枪、圣荆棘冠、都灵裹尸布，以及淬过神圣分支的武器。"),
        rule(),
        t("代价：", "white"), t("魔化过 91，它们会烫手", K)))

    # ---- 二、堕落 ----
    p.append(page(
        *vol("二", "到顶那一刻"), rule(),
        t("没有警报，没有提示。屏幕上只浮起四个字："),
        t("堕落开始", K, True), t("。\n"),
        t("然后你会发现自己变强了。"),
        rule(),
        aside("那正是要命的地方。")))

    p.append(page(
        *vol("二", "之后九十秒"), rule(),
        t("你的攻击一路往上走。同时视角会被扯开、脚步不听使唤、"
          "眼前时不时发黑；到最后，"),
        t("手会自己挥出去", K, True), t("。"),
        rule(),
        aside("越强，越不是你。")))

    p.append(page(
        *vol("二", "它出来了"), rule(),
        t("九十秒走完，有东西从你身上挣出去。你看不见它 —— "
          "只能看见它周身那团黑烟。它待三十秒。"),
        rule(),
        aside("你签过谁的约，来的就是谁。")))

    p.append(page(
        *vol("二", "刹车"), rule(),
        t("魔化满格时，立一支"), t("驱魔图腾", "#DAA520", True),
        t("并点燃它。它会朝你烧十秒 —— 站着别动，熬完。"),
        rule(),
        t("代价：", "white"), t("熬不住，一点都不会少", K)))

    # ---- 三、驱魔 ----
    p.append(page(
        *vol("三", "村里的空壳"), rule(),
        t("六个村民里大概有一个已经不是人了。平时看不出来，"),
        t("带着圣器走近，它才会亮起来", None, True), t("。"),
        rule(),
        aside("别急着动手 —— 你杀了它，里面那东西会跳进旁边那个人身上。")))

    p.append(page(
        *vol("三", "怎么办"), rule(),
        t("举着"), t("驱魔图腾", "#DAA520", True),
        t("长按右键立下，再朝它扔一瓶"),
        t("驱魔圣水", "#DAA520", True),
        t("。必须是滞留型的那种 —— 喷溅的一落地就散了。"),
        rule(),
        aside("图腾烧起来，方圆六格一起洗干净。")))

    # ---- 四、契约 ----
    p.append(page(
        *vol("四", "另一条路"), rule(),
        t("上一卷讲怎么爬出来，这一卷讲怎么"),
        t("自己走进去", None, True),
        t("。你会捡到七本书，每一本背后站着一位。长按右键，就算签了。"),
        rule(),
        aside("签下之后，恩赐与枷锁一起生效。")))

    rows = []
    for q in P["pillars"]:
        rows.append(t("%s" % q["who"], q["colour"], True))
        rows.append(t(" · %s\n" % q["sin"], G))
    p.append(page(*(vol("四", "七位") + [rule()] + rows + [rule()])))

    p.append(page(
        *vol("四", "签了以后"), rule(),
        t("再长按那本书，就是动用他的力量。但契约一直在渗 —— "
          "魔化会自己往上爬，你什么都不做也一样。"),
        rule(),
        t("代价：", "white"), t("贪婪那一位，渗得最快", K)))

    p.append(page(
        *vol("四", "反悔"), rule(),
        t("一、熬一次逆圣化，柱位连同污染一起烧掉。\n"),
        t("二、立一支图腾点燃，在它烧着时长按你那本已签的书。"),
        rule(),
        aside("两条都要疼一下。")))

    # ---- 五、罪器 ----
    p.append(page(
        *vol("五", "七宗罪"), rule(),
        t("七位领主各留下一件东西在人间。拿着它们你会变强，"
          "也会更快地脏掉。"),
        rule(),
        aside("值不值，你自己算。")))

    p.append(page(
        *vol("五", "玛门的弓"), rule(),
        t("贪婪那一件。一次射三根箭 —— 多出来的两根凭空出现，不吃你的箭。"),
        rule(),
        aside("听起来像白捡的。玛门不做白工。")))

    p.append(page(
        *vol("五", "他怎么收账"), rule(),
        t("每射一箭，他从你身上拿走一样：可能是经验，可能是钱，"
          "可能是一颗心，也可能是你的下一顿饭。"),
        rule(),
        aside("拿哪一样，他说了算。")))

    p.append(page(
        *vol("五", "买断"), rule(),
        t("拉满之后别松手，继续拉。攒够了，射出去的是一支"),
        t("金箭", "#DAA520", True), t("。"),
        rule(),
        t("代价：", "white"), t("五级经验；掏不出来就拿命抵", K)))

    p.append(page(
        *vol("五", "若你签了贪婪"), rule(),
        t("那把弓不再翻你的口袋，它改从"),
        t("魂上", None, True),
        t("收 —— 每射一箭，魔化多涨一点。而你的金箭落地时，"
          "周围的掉落物会变成两份。"),
        rule(),
        aside("同一位，两副面孔。")))

    # ---- 六、佣兵 ----
    p.append(page(
        *vol("六", "花钱雇人"), rule(),
        t("这一卷和前面都没关系。你可以一样魔器都不碰，只带着人打。\n"),
        t("募兵旗", "#DAA520", True), t(" 招人　"),
        t("指挥旗", "#DAA520", True), t(" 指挥"),
        rule(),
        aside("最多带 %d 个。" % Q["cap"])))

    rows = []
    for x in Q["tiers"]:
        rows.append(t("%s " % x["key"], x["colour"], True))
        rows.append(t("%d枚\n" % x["price"], "#DAA520"))
        rows.append(t("  ❤%d ⛊%d ⚔%d\n" % (x["hp"], x["armor_real"], x["total"]), G))
    p.append(page(*(vol("六", "五个档次") + [rule()] + rows)))

    p.append(page(
        *vol("六", "怎么招"), rule(),
        t("空着手长按募兵旗，会有人走过来站着 —— 不要钱。"
          "他什么档次是当场掷出来的，写在名牌上。看得上，再长按一次雇下他。"),
        rule(),
        aside("看不上，走开，重来。")))

    p.append(page(
        *vol("六", "升级"), rule(),
        t("潜行着长按募兵旗，对准你已经雇下的人。升一档，付那一档的"),
        t("全价", None, True), t("。"),
        rule(),
        aside("比重新招贵，但重新招是碰运气，这个一定成。")))

    p.append(page(
        *vol("六", "怎么指挥"), rule(),
        t("空手长按指挥旗：你看哪儿，他们打哪儿。\n"),
        t("副手拿把武器再长按：交给最近那个人。\n"),
        t("潜行＋空手：跟着走／原地待命\n"),
        t("潜行＋拿东西：遣散"),
        rule()))

    p.append(page(
        *vol("六", "关于他们"), rule(),
        t("他们不会自己找架打，也不会误伤你。盔甲是他们自己的，死了也带走；"
          "你塞给他的武器会掉在地上。"),
        rule(),
        aside("还有：他们不下水。")))

    # ---- 尾 ----
    p.append(page(
        t("\n"), rule(),
        t("\n   你手上的力量\n   正在变大。\n\n", G, italic=True),
        t("   那不是你的。\n\n", K, italic=True),
        rule()))

    return p


BS = chr(92)          # 反斜杠。写字面量容易在层层引号里被吃掉
SQ = chr(39)          # 单引号


def item_snbt():
    """整本书的 SNBT。

    不用 % 格式化：书页里有 "4%" 这样的字面百分号。
    也不用 json.dumps：见 snbt() —— 页面必须是 NBT，不是 JSON 字符串。
    """
    pages = ",".join(snbt(pg) for pg in build_pages())
    name = snbt([{"text": "\u300a" + TITLE + "\u300b",
                  "italic": False, "color": B, "bold": True}])
    return ("written_book[minecraft:written_book_content={"
            'title:"' + TITLE + '",author:"' + AUTHOR + '",'
            "resolved:true,pages:[" + pages + "]},"
            "minecraft:custom_name=" + name + ","
            "minecraft:enchantment_glint_override=true]")


def main():
    s = io.open(GIVE, encoding="utf-8").read()
    line = "give @a " + item_snbt()
    if TITLE in s:
        out, done = [], False
        for l in s.split("\n"):
            if TITLE in l and l.startswith("give "):
                out.append(line)
                done = True
            else:
                out.append(l)
        s = "\n".join(out)
        assert done
    else:
        s = s.rstrip("\n") + "\n\n##《%s》—— 游戏内玩法总览\n" % TITLE + line + "\n"
    io.open(GIVE, "w", encoding="utf-8", newline="\n").write(s)
    print("book: 《%s》%d 页" % (TITLE, len(build_pages())))


if __name__ == "__main__":
    main()
