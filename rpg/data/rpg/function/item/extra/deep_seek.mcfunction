# 蔚蓝追寻者［深潜］
# 箭矢拖着深海的水压飞行；命中生物时把目标向下拽入"深渊"并短暂锚定。
execute as @e[type=minecraft:arrow,tag=!rpg.deep] on origin if entity @s[tag=rpg.h.deep_seek_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.deep
execute as @e[tag=rpg.deep] at @s run particle dust_color_transition{from_color:[0.0,0.29,0.61],to_color:[0.20,0.85,0.95],scale:1} ~ ~ ~ 0.12 0.12 0.12 0.1 6
execute as @e[tag=rpg.deep] at @s run particle bubble ~ ~ ~ 0.1 0.1 0.1 0.02 2
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run particle bubble_column_up ~ ~0.4 ~ 0.4 0.6 0.4 0.05 40
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run particle dust_color_transition{from_color:[0.0,0.29,0.61],to_color:[0.20,0.85,0.95],scale:3} ~ ~0.6 ~ 0.5 0.6 0.5 0.1 30
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:slowness 4 3 true
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run effect give @e[distance=..1.6,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:mining_fatigue 4 1 true
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run data merge entity @e[distance=..1.6,limit=1,sort=nearest,type=!minecraft:arrow] {Motion:[0d,-1.1d,0d]}
execute as @e[tag=rpg.deep] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.deep_seek_tag1,distance=..1.6] run playsound minecraft:ambient.underwater.enter player @a[distance=..12]
execute as @e[tag=rpg.deep] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=rpg.deep] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=rpg.deep] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=rpg.deep] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=rpg.deep] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=rpg.deep] at @s unless block ~ ~ ~0.1 air run kill @s
