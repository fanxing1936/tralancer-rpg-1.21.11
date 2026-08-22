# 10 行原本各自扫一遍全实体表找 @e[tag=hunter]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=hunter] at @s run particle dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.26,0.64,0.93],scale:3} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10
execute as @e[tag=hunter] at @s if entity @e[distance=0.1..2] unless entity @a[tag=rpg.h.hunter_tag1,distance=..2] run particle squid_ink ~0.5 ~0.5 ~0.5 -1 -1 -1 0.5 50
execute as @e[tag=hunter] at @s if entity @e[distance=0.1..2] unless entity @a[tag=rpg.h.hunter_tag1,distance=..2] run particle dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.26,0.64,0.93],scale:3} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.5 50
execute as @e[tag=hunter] at @s if entity @e[distance=0.1..2] unless entity @a[tag=rpg.h.hunter_tag1,distance=..2] run summon minecraft:creeper ~ ~1 ~ {"ExplosionRadius":3,"Fuse":0}
execute as @e[tag=hunter] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=hunter] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=hunter] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=hunter] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=hunter] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=hunter] at @s unless block ~ ~ ~0.1 air run kill @s
