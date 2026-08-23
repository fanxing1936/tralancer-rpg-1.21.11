# 5 行原本各自扫一遍全实体表找 @e[tag=devil,tag=boss]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=devil,tag=boss] at @s if score @s devil matches 150..151 run effect give @s minecraft:instant_health 1 3 true 
execute as @e[tag=devil,tag=boss] at @s if score @s devil matches 100..105 at @a[distance=..20] run summon evoker_fangs
execute as @e[tag=devil,tag=boss] at @s if score @s devil matches 40 if entity @a[distance=..5] run playsound minecraft:entity.vex.charge player @a[distance=..15]
execute as @e[tag=devil,tag=boss] at @s if score @s devil matches 50 if entity @a[distance=..5] run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 1000
execute as @e[tag=devil,tag=boss] at @s if score @s devil matches 50 if entity @a[distance=..5] run summon minecraft:creeper ~ ~1 ~ {"ExplosionRadius":8,ignited:1b}
