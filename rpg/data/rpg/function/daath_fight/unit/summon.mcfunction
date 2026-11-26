# 影子从倒影里站起来（as/at 挑战者）
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1,sort=nearest] positioned ~ ~ ~-7 run summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.el.seen","rpg.dtb","rpg.dtwear","rpg.dt.new"],Silent:1b,PersistenceRequired:1b,NoAI:1b,Invulnerable:1b,Rotation:[0f,0f],active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:attack_damage",base:0d},{id:"minecraft:armor",base:0d},{id:"minecraft:follow_range",base:64d},{id:"minecraft:knockback_resistance",base:1d},{id:"minecraft:movement_speed",base:0.34d}],equipment:{mainhand:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:empty"}}},drop_chances:{mainhand:0f,offhand:0f}}
tag @s add rpg.dt.me
execute as @e[type=minecraft:vindicator,tag=rpg.dtb,tag=rpg.dt.new,distance=..80,limit=1,sort=nearest] at @s run function rpg:daath_fight/unit/init
tag @s remove rpg.dt.me
