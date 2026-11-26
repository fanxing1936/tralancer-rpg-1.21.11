# 影子每刻（as/at 影子）
tag @s add rpg.dt.it
tag @p[tag=rpg.dt.in,distance=..90] add rpg.dt.me
execute if entity @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/unit/run
tag @a remove rpg.dt.me
tag @e[type=minecraft:vindicator,tag=rpg.dt.it] remove rpg.dt.it
