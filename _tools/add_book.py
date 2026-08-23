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
    return json.dumps(list(parts), ensure_ascii=False, separators=(",", ":"))


def head(n, name):
    return t("卷%s · %s\n\n" % (n, name), B, True)


def build_pages():
    p = []

    # ---- 扉页 ----
    p.append(page(
        t("\n"),
        t("  破碎大陆\n", K, True),
        t("  ─────────\n", G),
        t("\n  Eretz\n  Ha-Shevarim\n\n", G, italic=True),
        t("  这片土地上的\n  每一件东西\n  都在向你索取\n", G, italic=True)))

    p.append(page(
        head("零", "怎么开始"),
        t("先执行一次：\n"),
        t("/function\nrpg:command/give/box\n\n", K),
        t("你会拿到几个潜影盒，包含全部装备与材料。\n\n"),
        t("再执行一次记分板初始化：\n"),
        t("/function\nrpg:command/soreboard", K)))

    # ---- 圣与魔 ----
    p.append(page(
        head("一", "圣与魔"),
        t("这个世界只有一条轴：\n\n"),
        t("圣器", "#DAA520", True), t(" 与 "),
        t("魔器", K, True), t("。\n\n"),
        t("握着魔器的人会慢慢变成它的主人 —— 这不是比喻，是一个每两秒结算一次的数字。")))

    p.append(page(
        head("一", "魔化值"),
        t("上限 100。屏幕下方那条就是它。\n\n"),
        t("持恶魔本体武器 +2\n持罪器 +1\n持圣器 −1\n\n"),
        t("打空缺者 +6\n杀空缺者 +8\n\n"),
        t("两者同时握着会互相抵消。", G, italic=True)))

    p.append(page(
        head("一", "什么算圣器"),
        t("手持"), t("或穿戴", None, True), t("都算：\n\n"),
        t("· 四件驱魔道具\n"),
        t("· 神圣品质的武具\n  （朗基努斯之枪、\n  圣荆棘冠、\n  都灵裹尸布）\n"),
        t("· 加过神圣分支的武器\n\n"),
        t("但魔化过 91，圣器会灼手。", K)))

    # ---- 堕落 ----
    p.append(page(
        head("二", "堕落"),
        t("魔化到顶不会有人来救你。\n\n"),
        t("屏幕上只写四个字：\n"),
        t("堕落开始", K, True), t("。\n\n"),
        t("此后每两秒往下掉一步，共六十步，约九十秒。过半之后一步变两步。")))

    p.append(page(
        head("二", "掉下去的样子"),
        t("躁动 ", G), t("攻击+1\n"),
        t("侵蚀 ", G), t("攻击+3，视角开始被扯动\n"),
        t("夺舍 ", G), t("攻击+6，脚步不听使唤\n"),
        t("临界 ", G), t("攻击+10，黑视，"),
        t("手会自己挥出去", K, True),
        t("\n\n你越来越强，也越来越不是你。", G, italic=True)))

    p.append(page(
        head("二", "降临"),
        t("六十步走完，有东西从你身上挣出来。\n\n"),
        t("你看不见它 —— 它常驻隐身，只有周身的黑烟能指出位置。\n\n"),
        t("它只待三十秒。\n\n"),
        t("签过契约的人，来的是那一位领主。", G, italic=True)))

    # ---- 驱魔 ----
    p.append(page(
        head("三", "空缺者"),
        t("约六分之一的村民是空壳。\n\n"),
        t("平时与常人无异，"),
        t("只有持圣器的人走进十六格才会显形", None, True),
        t("。\n\n"),
        t("放着不管会蔓延；动手打反而更糟 —— 杀死它，里面的东西会跳到旁边的村民身上。")))

    p.append(page(
        head("三", "驱魔仪式"),
        t("长按"), t("驱魔图腾", "#DAA520", True), t("立起，\n"),
        t("再用"), t("驱魔圣水", "#DAA520", True), t("浇上去点燃。\n\n"),
        t("圣水必须是"), t("滞留型", None, True),
        t("：喷溅型落地即散，图腾感知不到。\n\n"),
        t("六格内净化魔化、驱出空缺者。")))

    p.append(page(
        head("三", "逆圣化"),
        t("魔化正好 100 时点燃图腾，仪式不再净化，而是"),
        t("引燃", K, True), t("。\n\n"),
        t("图腾朝你烧十秒，共十九点伤害。"),
        t("你必须站在七格内熬完。", None, True),
        t("\n\n熬过去：魔化归零，得三分钟圣痕。\n熬不住：一点没少。")))

    # ---- 契约 ----
    p.append(page(
        head("四", "七十二柱"),
        t("上一卷是走出去的路。这一卷是走进去的路，而且是你自己选的。\n\n"),
        t("契约是一本书。长按右键签下，恩赐与枷锁一并生效。\n\n"),
        t("此后再长按 = 动用柱中之力。")))

    rows = []
    for q in P["pillars"]:
        rows.append(t("%s " % q["who"], q["colour"], True))
        rows.append(t("%s\n" % q["sin"], G))
    p.append(page(head("四", "七位领主"), *rows))

    p.append(page(
        head("四", "代价与解约"),
        t("立约本身就在渗：每次结算额外 +1 魔化。贪婪那一柱翻倍。\n\n"),
        t("解约两条路：\n"),
        t("· 逆圣化（连柱位一起烧）\n"),
        t("· 在燃着的图腾旁长按已立约的书\n\n"),
        t("柱位是排他的。", G, italic=True)))

    # ---- 罪器 ----
    p.append(page(
        head("五", "七宗罪的罪器"),
        t("六位领主各留下一件武器。第七件是玛门的弓。\n\n"),
        t("[DEVIL]", K, True), t("玛门\n\n"),
        t("一次射出三根箭。多出的两根凭空而来，不吃箭袋。")))

    p.append(page(
        head("五", "贪婪的账"),
        t("每射一箭，玛门都要从你身上取走一样：经验、钱、血，或者你的下一顿。\n\n"),
        t("满弓后继续持弓，攒满可射出"),
        t("买断", "#DAA520", True),
        t("金箭 —— 它"), t("必定收费", None, True),
        t("，五级经验，付不起就拿命抵。")))

    p.append(page(
        head("五", "契约与罪器"),
        t("签下第七柱之后，那把弓"),
        t("不再从你口袋里掏东西", None, True),
        t(" —— 它改从魂上收，每箭多沾两点魔化。\n\n"),
        t("而买断的金箭会顺带把周围的掉落物翻一倍。\n\n"),
        t("同一位魔神，两副面孔。", G, italic=True)))

    # ---- 佣兵 ----
    p.append(page(
        head("六", "佣兵小队"),
        t("一个独立分支，不与前面任何一条耦合。\n\n"),
        t("两面旗：\n"),
        t("募兵旗", "#DAA520", True), t(" 招人\n"),
        t("指挥旗", "#DAA520", True), t(" 指挥\n\n"),
        t("上限 %d 人。" % Q["cap"])))

    rows = []
    for x in Q["tiers"]:
        rows.append(t("%-7s" % x["key"], x["colour"], True))
        rows.append(t(" ❤%d ⛊%d ⚔%d\n" % (x["hp"], x["armor_real"], x["total"]), G))
        rows.append(t("   %d枚 · %d%%\n" % (x["price"], x["w"]), G))
    p.append(page(head("六", "五等"), *rows))

    p.append(page(
        head("六", "怎么招"),
        t("身边没人时长按募兵旗：招一名"),
        t("待雇者", None, True),
        t("到场，不花钱。等级当场掷点。\n\n"),
        t("看着名牌决定雇不雇 —— 再长按一次才是真的雇下他。\n\n"),
        t("不满意就走开重招。", G, italic=True)))

    p.append(page(
        head("六", "升级"),
        t("潜行 + 募兵旗，对着在编佣兵。\n\n"),
        t("升到某一等，付那一等的"),
        t("全价", None, True), t("。\n\n"),
        t("比掷点贵，但一定成 —— 你买的是确定性。\n\n"),
        t("甲与纹饰随等级换；手上那把武器不动。", G, italic=True)))

    p.append(page(
        head("六", "指挥"),
        t("指挥旗，副手空着：\n"),
        t("沿视线指定目标，全队压上。\n\n"),
        t("副手拿着武器：\n"),
        t("交给最近的佣兵，他原本那把掉在地上。\n\n"),
        t("潜行 + 副手空 = 跟随/驻守\n"),
        t("潜行 + 副手有物 = 解雇")))

    p.append(page(
        head("六", "为什么不会误伤"),
        t("尸壳是敌对生物，而原版命令没有办法清除一个生物的当前目标。\n\n"),
        t("所以佣兵的索敌半径被设成了"),
        t("零", None, True),
        t("。它永远不会自己选中任何东西 —— 安全是结构性的，不靠判定去兜。", G)))

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

    这里**不能**用 % 格式化：书页里有 "4%" 这样的字面百分号，
    一格式化就炸。全程字符串拼接。
    """
    pages = ",".join("'" + pg.replace(BS, BS * 2).replace(SQ, BS + SQ) + "'"
                     for pg in build_pages())
    name = ('[{"text":"《' + TITLE + '》","italic":false,'
            '"color":"' + B + '","bold":true}]')
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
