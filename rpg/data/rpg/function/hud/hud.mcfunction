# 屏幕下方唯一的 actionbar 出口。技能不再各写各的 —— 它们只更新
# rpg_hud / rpg_hud_p 并把 rpg_hud_t 顶到 3，这里按优先级挑一条渲染。
# 蓄力条永远压过状态条；蓄力一结束，状态条自己就回来了。

# 先把占用计时器坐实。scores= 只认已经存在的分数，没有这一行，
# 从没蓄过力的玩家过不了下面 rpg_hud_t=..0 那一关，状态条永远不显示。
scoreboard players add @s rpg_hud_t 0
scoreboard players add @s rpg_hud_mt 0

# 一次性提示压过所有条，只活 40 刻；它一过期，条自己就回来。
execute if entity @s[scores={rpg_hud_mt=1..}] run function rpg:hud/msg_tick

execute if entity @s[scores={rpg_hud_mt=..0,rpg_hud_t=1..,rpg_hud=1}] run function rpg:hud/s1
execute if entity @s[scores={rpg_hud_mt=..0,rpg_hud_t=1..,rpg_hud=2}] run function rpg:hud/s2
execute if entity @s[scores={rpg_hud_mt=..0,rpg_hud_t=1..,rpg_hud=3}] run function rpg:hud/s3
execute if entity @s[scores={rpg_hud_mt=..0,rpg_hud_t=1..,rpg_hud=4}] run function rpg:hud/s4

# 没有技能占用时才轮到持续状态行。魔化（或圣痕）与契约冷却在那一行里
# **并排**显示 —— 它们都是状态，不该互相顶掉。
execute if entity @s[scores={rpg_hud_mt=..0,rpg_hud_t=..0}] run function rpg:hud/status

execute if entity @s[scores={rpg_hud_t=1..}] run scoreboard players remove @s rpg_hud_t 1
