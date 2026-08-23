# 圣痕。逆圣化留下的那段时间：走到哪儿，空壳就散到哪儿。
# 属性增益在授予那一下就按整段时长给足了，这里只管计时、光晕和清场。
scoreboard players remove @s rpg_holy 1
particle end_rod ~ ~1.1 ~ 0.35 0.7 0.35 0.01 3
particle dust{color:[1.0,0.97,0.80],scale:1} ~ ~1 ~ 0.4 0.8 0.4 0.01 2
# 走到哪儿，空壳就散到哪儿 —— 本人就是一场行走的仪式。
# 这一行自己就是那次走查，前面再加一道同样的守卫只会白扫一遍。
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
execute if entity @s[scores={rpg_holy=..0}] run function rpg:taint/holy_end
