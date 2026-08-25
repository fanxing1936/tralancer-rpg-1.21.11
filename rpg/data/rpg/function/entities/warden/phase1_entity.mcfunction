# 单次实体绑定完成一阶段常驻逻辑。
effect give @s minecraft:invisibility 1 1 true
particle large_smoke ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 1
particle squid_ink ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 5
execute if score @s devil matches 200.. run scoreboard players set @s devil 0
scoreboard players add @s devil 1
execute if entity @s[tag=rpg.boss.minion] run scoreboard players add @s rpg_boss_fx 1
execute if entity @s[tag=rpg.boss.minion,scores={rpg_boss_fx=1200..}] run return run kill @s
execute if score @s devil matches 50..51 run effect give @a[distance=..15] minecraft:blindness 5 10 true
execute if score @s devil matches 50 at @a[distance=..15] run particle minecraft:elder_guardian
execute if score @s devil matches 50..51 run playsound minecraft:entity.allay.death player @a[distance=..15]
execute if score @s devil matches 100 run effect give @a[distance=..15] minecraft:nausea 5 2 true
execute if score @s devil matches 150..151 run playsound minecraft:entity.allay.ambient_with_item player @a[distance=..15]
execute if score @s devil matches 150..151 run effect give @s minecraft:instant_health 1 1 true
effect give @a[distance=..15] minecraft:darkness 5 10 true
execute if score @s devil matches 60 run playsound minecraft:entity.vex.death player @a[distance=..15]
execute if score @s devil matches 180 run playsound minecraft:entity.vex.death player @a[distance=..15]
execute on attacker if entity @s[tag=rpg.h.devil_tag1] run effect give @e[distance=..1,limit=1] minecraft:instant_damage 1 0 true
execute on attacker if entity @s[tag=rpg.h.devil_tag1] run effect clear @e[distance=..1,limit=1] minecraft:invisibility
execute if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute if entity @s[tag=boss] run function rpg:entities/warden/phase1_boss
