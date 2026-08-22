# 稚弩［顽劣］
# 不加伤害：命中的目标被恶作剧缠上——眩晕、脱力，并在一段时间内无处可藏。
execute as @e[type=minecraft:arrow,tag=!rpg.mis] on origin if entity @s[tag=rpg.h.mischief_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.mis
execute as @e[tag=rpg.mis] at @s run particle dust_color_transition{from_color:[1.0,0.45,0.85],to_color:[1.0,0.85,0.35],scale:1} ~ ~ ~ 0.1 0.1 0.1 0.1 5
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run particle firework ~ ~0.6 ~ 0.4 0.4 0.4 0.12 40
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run particle happy_villager ~ ~0.8 ~ 0.5 0.5 0.5 0.1 20
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:nausea 6 0 true
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:weakness 8 1 true
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:glowing 10 0 true
execute as @e[tag=rpg.mis] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.mischief_tag1,distance=..1.6] run playsound minecraft:entity.allay.item_thrown player @a[distance=..12]
execute as @e[tag=rpg.mis] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=rpg.mis] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=rpg.mis] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=rpg.mis] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=rpg.mis] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=rpg.mis] at @s unless block ~ ~ ~0.1 air run kill @s
