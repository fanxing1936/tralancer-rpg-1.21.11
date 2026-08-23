# 认箭。只有窗口没走完的人才会进到这里 —— 没碰过这把弓的人一条不欠。
scoreboard players remove @s rpg_mam_win 1
execute if entity @s[scores={rpg_mam_dw=1..}] run scoreboard players remove @s rpg_mam_dw 1

# 身边六格内的新箭。带类型、带半径，比一次全表遍历便宜得多。
# 标记自己是当前射手：箭那头要用 `on origin` 回头核对。
tag @s add rpg.mam.shooter
execute as @e[type=minecraft:arrow,tag=!rpg.mam.seen,distance=..10] run function rpg:mammon/arrow
tag @s remove rpg.mam.shooter

# 窗口走完还没等到箭 —— 那是拉到一半松了手，没出箭。蓄力作废。
execute if entity @s[scores={rpg_mam_win=..0}] run scoreboard players set @s rpg_mam_c 0
