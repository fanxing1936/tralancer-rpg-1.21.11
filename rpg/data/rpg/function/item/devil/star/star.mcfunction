advancement revoke @s only rpg:devil/star
execute as @e[tag=devil,distance=..7] at @s run particle ominous_spawning ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 3 80 normal
execute as @e[tag=devil,distance=..7] at @s run effect give @s minecraft:glowing 5 1 true
execute as @e[tag=devil,distance=..7] at @s run effect give @s minecraft:slowness 5 255 true
execute as @e[type=minecraft:vindicator,tag=devil2,distance=..7] at @s run particle ominous_spawning ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 3 80 normal
execute as @e[type=minecraft:vindicator,tag=devil2,distance=..7] at @s run effect give @s minecraft:glowing 5 1 true
execute as @e[type=minecraft:vindicator,tag=devil2,distance=..7] at @s run effect give @s minecraft:slowness 5 255 true
# ---- 驱魔适配 ----
# 「能指引恶魔的繁星，审判罪恶」—— 原本这颗星只照 devil 标签、半径 7 格，
# 与魔化值和空缺者毫无交集。既然它是一颗**星**，照的范围理应远得多，
# 也理应照得出披着人皮的那些。
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..32] at @s run function rpg:item/devil/star/shell
execute as @a[distance=..32,scores={rpg_taint=31..}] at @s run function rpg:item/devil/star/judge
execute at @s run particle end_rod ~ ~1 ~ 0.6 1.2 0.6 0.4 120
execute at @s run particle flash{color:16777200} ~ ~1.4 ~ 0 0 0 0 1
execute at @s run playsound minecraft:block.beacon.power_select master @a[distance=..32] ~ ~ ~ 1 1.6
item replace entity @s weapon.mainhand with air
