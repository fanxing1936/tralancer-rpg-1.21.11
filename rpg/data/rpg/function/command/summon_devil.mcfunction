# 八位恶魔的召唤入口，手动招唤用。
#
# **整份跑下去会把八位一起招出来** —— 通常你只想要其中一行，
# 把那一行复制到聊天栏（记得带 /）即可。
#
# 为什么不是裸的 summon：恶魔的寿命是由 rpg:taint/advent_life 给的，
# 只 summon 不走那一步，rpg_fall 停在 0，下一刻就被判过期清掉 ——
# 手动招出来的会瞬间消失。lordN 这一条是完整入口：
# 召唤 + 记下他是谁（技能按这个分流）+ 给寿命。
#
# 每条前面把 #boss 拨上，所以手动招出来的按**两分钟**算，
# 而不是降临那只"来收账的"三十秒。
#
# 他们都挂着 devil 标签，于是自动继承包里恶魔 boss 那一套：
# 常驻隐身、周身黑烟与墨。

# 路西法 · 傲慢　　［原罪］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord1

# 利维坦 · 嫉妒　　［沉锚］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord2

# 亚巴顿 · 怠惰　　［收割］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord3

# 别西卜 · 暴食　　［余烬］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord4

# 萨麦尔 · 暴怒　　［毒雾］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord5

# 贝利尔 · 色欲　　［朝拜］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord6

# 玛门 · 贪婪　　［点金］
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord7

# 无名者（没签过契约的人招出来的那一位）
scoreboard players set #boss rpg_fall 1
function rpg:taint/lord
