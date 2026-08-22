# 13 行原本各自扫一遍全实体表找 @e[tag=devil]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=devil] at @s if score @s devil matches 50..51 run effect give @a[distance=..15] minecraft:blindness 5 10 true
execute as @e[tag=devil] at @s if score @s devil matches 50 at @a[distance=..15] run particle minecraft:elder_guardian
execute as @e[tag=devil] at @s if score @s devil matches 50..51 run playsound minecraft:entity.allay.death player @a[distance=..15]

execute as @e[tag=devil] at @s if score @s devil matches 100 run effect give @a[distance=..15] minecraft:nausea 5 2 true

execute as @e[tag=devil] at @s if score @s devil matches 150..151 run playsound minecraft:entity.allay.ambient_with_item player @a[distance=..15]
execute as @e[tag=devil] at @s if score @s devil matches 150..151 run effect give @s minecraft:instant_health 1 1 true 


execute as @e[tag=devil] at @s run effect give @a[distance=..15] minecraft:darkness 5 10 true
execute as @e[tag=devil] at @s if score @s devil matches 60 run playsound minecraft:entity.vex.death player @a[distance=..15]
execute as @e[tag=devil] at @s if score @s devil matches 180 run playsound minecraft:entity.vex.death player @a[distance=..15]

execute as @e[tag=devil] at @s on attacker if entity @s[tag=rpg.h.devil_tag1] run effect give @e[distance=..1,limit=1] minecraft:instant_damage 1 0 true
execute as @e[tag=devil] at @s on attacker if entity @s[tag=rpg.h.devil_tag1] run effect clear @e[distance=..1,limit=1] minecraft:invisibility

execute as @e[tag=devil] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute as @e[tag=devil] at @s if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
