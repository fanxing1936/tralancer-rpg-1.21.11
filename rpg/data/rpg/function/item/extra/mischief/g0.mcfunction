# 13 行原本各自扫一遍全实体表找 @e[tag=rpg.mis]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
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
