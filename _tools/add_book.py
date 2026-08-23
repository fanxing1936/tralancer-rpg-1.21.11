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


def build_pages():
    """给玩家的手册。

    不复述实现 —— 每一页只回答「这是什么 / 按什么 / 代价是什么」。
    """
    p = []

    # ---- 扉页 ----
    p.append(page(
        t("\n"),
        t("  破碎大陆\n", K, True),
        t("  ─────────\n", G),
        t("\n  Eretz\n  Ha-Shevarim\n\n", G, italic=True),
        t("  这里的每一样东西\n  都要向你收费。\n\n", G, italic=True),
        t("  先读完这本。\n", G, italic=True)))

    p.append(page(
        head("零", "开局"),
        t("对着聊天栏敲一次：\n\n"),
        t("/function\nrpg:command/give/box\n\n", K),
        t("几个潜影盒到手，武器、护甲、材料都在里面。\n\n"),
        t("剩下的，边走边看。", G, italic=True)))

    # ---- 圣与魔 ----
    p.append(page(
        head("一", "两种东西"),
        t("你捡到的兵器分两路。\n\n"),
        t("圣器", "#DAA520", True), t("护着你。\n"),
        t("魔器", K, True), t("更强，但它认主 —— 认的不是你。\n\n"),
        t("握久了，它会开始把你当成它的。", G, italic=True)))

    p.append(page(
        head("一", "魔化"),
        t("屏幕正下方那条就是。\n满格 100。\n\n"),
        t("握着魔器，它涨。\n握着圣器，它退。\n两手都拿，互相抵消。\n\n"),
        t("打村子里那些"), t("空壳", K, True), t("，涨得最快。")))

    p.append(page(
        head("一", "什么算圣器"),
        t("拿在手上"), t("或者穿在身上", None, True), t("都算：\n\n"),
        t("· 驱魔图腾、驱魔圣水\n· 驱魔替死人偶\n· 驱魔天启星\n"),
        t("· 朗基努斯之枪\n· 圣荆棘冠、都灵裹尸布\n"),
        t("· 淬过神圣分支的武器\n\n"),
        t("但魔化过 91，它们会烫手。", K)))

    # ---- 堕落 ----
    p.append(page(
        head("二", "到顶那一刻"),
        t("没有警报，没有提示。\n\n"),
        t("屏幕上只浮起四个字：\n"),
        t("堕落开始", K, True), t("。\n\n"),
        t("然后你会发现自己变强了。\n\n"),
        t("那正是要命的地方。", G, italic=True)))

    p.append(page(
        head("二", "接下来九十秒"),
        t("你的攻击一路往上走。\n\n"),
        t("同时：\n"),
        t("视角会被扯开\n"),
        t("脚步不听使唤\n"),
        t("眼前时不时发黑\n"),
        t("到最后，"), t("手会自己挥出去", K, True), t("\n\n"),
        t("越强，越不是你。", G, italic=True)))

    p.append(page(
        head("二", "然后它出来了"),
        t("九十秒走完，有东西从你身上挣出去。\n\n"),
        t("你看不见它 —— 只能看见它周身那团黑烟。\n\n"),
        t("它待三十秒。\n\n"),
        t("如果你签过契约，来的就是"), t("你那一位", None, True), t("。")))

    p.append(page(
        head("二", "刹车"),
        t("有一条路能停下来，但没有人会告诉你它在哪。\n\n"),
        t("魔化正好满格时，立一支"),
        t("驱魔图腾", "#DAA520", True), t("，点燃它。\n\n"),
        t("它会朝你烧十秒。\n"),
        t("站着别动，熬完。\n\n"),
        t("熬过去，你就干净了。")))

    # ---- 驱魔 ----
    p.append(page(
        head("三", "村子里的空壳"),
        t("六个村民里大概有一个已经不是人了。\n\n"),
        t("平时看不出来。"),
        t("带着圣器走近，它才会亮起来。", None, True),
        t("\n\n别急着动手 —— 你杀了它，里面那东西会跳进旁边那个村民身上。")))

    p.append(page(
        head("三", "该怎么办"),
        t("举着"), t("驱魔图腾", "#DAA520", True), t("长按右键，把它立下。\n\n"),
        t("再朝它扔一瓶"),
        t("驱魔圣水", "#DAA520", True), t("。\n\n"),
        t("必须是"), t("滞留型", None, True),
        t("的那种 —— 喷溅的一落地就散了。\n\n"),
        t("图腾烧起来，方圆六格的脏东西一起洗掉。")))

    # ---- 契约 ----
    p.append(page(
        head("四", "另一条路"),
        t("上一卷讲的是怎么爬出来。\n\n"),
        t("这一卷讲怎么"), t("自己走进去", None, True), t("。\n\n"),
        t("你会捡到七本书。每一本背后站着一位。\n\n"),
        t("长按右键，就算签了。", G, italic=True)))

    rows = []
    for q in P["pillars"]:
        rows.append(t("%s " % q["who"], q["colour"], True))
        rows.append(t("%s\n" % q["sin"], G))
    p.append(page(
        head("四", "七位"),
        *(rows + [t("\n签下之后，恩赐与枷锁一起生效。", G, italic=True)])))

    p.append(page(
        head("四", "签了以后"),
        t("再长按那本书，就是"),
        t("动用他的力量", None, True), t("。\n\n"),
        t("但契约一直在渗 —— 魔化会自己往上爬，什么都不做也一样。\n\n"),
        t("贪婪那一位渗得最快。", G, italic=True)))

    p.append(page(
        head("四", "反悔"),
        t("两条路：\n\n"),
        t("一、熬一次逆圣化，柱位连同污染一起烧掉。\n\n"),
        t("二、立一支图腾点燃，在它烧着的时候长按你那本已签的书。\n\n"),
        t("都要疼一下。", G, italic=True)))

    # ---- 罪器 ----
    p.append(page(
        head("五", "七宗罪"),
        t("七位领主，各留下一件东西在人间。\n\n"),
        t("拿着它们，你会变强，也会更快地脏掉。\n\n"),
        t("值不值，你自己算。", G, italic=True)))

    p.append(page(
        head("五", "玛门的弓"),
        t("贪婪那一件。\n\n"),
        t("一次射三根箭 —— 多出来的两根凭空出现，不吃你的箭。\n\n"),
        t("听起来像白捡的。\n"),
        t("玛门不做白工。", G, italic=True)))

    p.append(page(
        head("五", "他怎么收账"),
        t("每射一箭，他从你身上拿走一样：\n\n"),
        t("可能是经验\n可能是钱\n可能是一颗心\n也可能是你的下一顿饭\n\n"),
        t("拿哪一样，他说了算。", G, italic=True)))

    p.append(page(
        head("五", "买断"),
        t("拉满之后别松手，继续拉。\n\n"),
        t("攒够了，射出去的是一支"),
        t("金箭", "#DAA520", True), t("。\n\n"),
        t("这一箭"), t("一定要钱", None, True),
        t("：五级经验。\n\n"),
        t("掏不出来，他就拿命抵。", K)))

    p.append(page(
        head("五", "如果你签了贪婪"),
        t("那把弓不再翻你的口袋了。\n\n"),
        t("它改从"), t("魂上", None, True), t("收 —— 每射一箭，魔化多涨一点。\n\n"),
        t("而你的金箭落地时，周围的掉落物会变成两份。\n\n"),
        t("同一位，两副面孔。", G, italic=True)))

    # ---- 佣兵 ----
    p.append(page(
        head("六", "花钱雇人"),
        t("这一卷和前面都没关系。你可以一样魔器都不碰，只带着人打。\n\n"),
        t("两面旗：\n"),
        t("募兵旗", "#DAA520", True), t(" —— 招人\n"),
        t("指挥旗", "#DAA520", True), t(" —— 指挥\n\n"),
        t("最多带 %d 个。" % Q["cap"])))

    rows = []
    for x in Q["tiers"]:
        rows.append(t("%s" % x["key"], x["colour"], True))
        rows.append(t("  %d 枚\n" % x["price"], G))
        rows.append(t("  ❤%d ⛊%d ⚔%d\n" % (x["hp"], x["armor_real"], x["total"]), G))
    p.append(page(head("六", "五个档次"), *rows))

    p.append(page(
        head("六", "怎么招"),
        t("空着手长按募兵旗，会有人走过来站着 —— 不要钱。\n\n"),
        t("他什么档次是当场掷出来的，写在名牌上。\n\n"),
        t("看得上，再长按一次雇下他。\n"),
        t("看不上，走开，重来。", G, italic=True)))

    p.append(page(
        head("六", "升级"),
        t("潜行着长按募兵旗，对准你已经雇下的人。\n\n"),
        t("升一档，付那一档的"),
        t("全价", None, True), t("。\n\n"),
        t("比重新招贵。\n"),
        t("但重新招是碰运气，这个一定成。", G, italic=True)))

    p.append(page(
        head("六", "怎么指挥"),
        t("空着手长按指挥旗：\n"),
        t("你看哪儿，他们打哪儿。\n\n"),
        t("副手拿把武器再长按：\n"),
        t("交给最近那个人，他原来那把掉地上。\n\n"),
        t("潜行 + 空手 = 跟着走／原地待命\n"),
        t("潜行 + 拿东西 = 遣散")))

    p.append(page(
        head("六", "关于他们"),
        t("他们不会自己找架打，也不会误伤你 —— 你不下令，他们就只是跟着。\n\n"),
        t("盔甲是他们自己的，死了也带走。\n"),
        t("你塞给他的武器，会掉在地上。\n\n"),
        t("他们不下水。", G, italic=True)))

    # ---- 尾 ----
    p.append(page(
        t("\n"),
        t("  ─────────\n", G),
        t("\n  你手上的力量\n  正在变大。\n\n", G, italic=True),
        t("  那不是你的。\n", K, italic=True),
        t("\n  ─────────\n", G)))

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
