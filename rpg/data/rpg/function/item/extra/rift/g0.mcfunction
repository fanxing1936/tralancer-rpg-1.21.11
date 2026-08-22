# 14 行原本各自扫一遍全实体表找 @e[tag=rpg.rift]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.rift] at @s run particle dust_color_transition{from_color:[1.0,0.94,0.62],to_color:[0.85,0.95,1.0],scale:1} ~ ~ ~ 0.1 0.1 0.1 0.15 5
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle minecraft:flash{color:16766519} ~ ~0.7 ~ 0 0 0 0 1
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle minecraft:flash{color:16766519} ~ ~1.4 ~ 0 0 0 0 1
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle gust_emitter_large ~ ~0.5 ~ 0 0 0 0 1
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run particle sweep_attack ~ ~0.8 ~ 1.2 0.6 1.2 0 12
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run execute as @e[distance=..3,type=!minecraft:arrow,type=!player] run damage @s 3 minecraft:player_attack by @a[tag=rpg.h.rift_tag1,limit=1,sort=nearest]
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run data merge entity @e[distance=..3,limit=1,sort=nearest,type=!minecraft:arrow] {Motion:[0d,0.95d,0d]}
execute as @e[tag=rpg.rift] at @s if entity @e[distance=0.1..1.6,type=!minecraft:arrow] unless entity @a[tag=rpg.h.rift_tag1,distance=..1.6] run playsound minecraft:entity.breeze.wind_burst player @a[distance=..16]
execute as @e[tag=rpg.rift] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=rpg.rift] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=rpg.rift] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=rpg.rift] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=rpg.rift] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=rpg.rift] at @s unless block ~ ~ ~0.1 air run kill @s
