# 7 行原本各自扫一遍全实体表找 @e[type=minecraft:spectral_arrow,tag=sakura_tag]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~1.5 ~ ~1.5 -3 -0.1 -3 0.2 200
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":3,ignited:1b}
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run kill @s

execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~1.5 ~ ~1.5 -3 -0.1 -3 0.2 200
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":3,ignited:1b}
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run kill @s
