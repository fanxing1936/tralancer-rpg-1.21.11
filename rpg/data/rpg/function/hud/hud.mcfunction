# 屏幕下方唯一的 actionbar 出口。技能不再各写各的 —— 它们只更新
# rpg_hud / rpg_hud_p 并把 rpg_hud_t 顶到 3，这里按优先级挑一条渲染。
# 蓄力条永远压过魔化条；蓄力一结束，魔化条自己就回来了。

execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=1}] run function rpg:hud/s1
execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=2}] run function rpg:hud/s2
execute if entity @s[scores={rpg_hud_t=1..,rpg_hud=3}] run function rpg:hud/s3

# 没有技能占用、且确实有魔化时，才轮到魔化条
execute if entity @s[scores={rpg_hud_t=..0,rpg_taint=1..}] run function rpg:hud/taint

execute if entity @s[scores={rpg_hud_t=1..}] run scoreboard players remove @s rpg_hud_t 1
