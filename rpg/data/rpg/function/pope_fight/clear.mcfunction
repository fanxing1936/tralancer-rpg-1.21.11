# 清除教皇战的全部实体。
scoreboard players set #stage rpg_pf 0
execute as @e[type=minecraft:vindicator,tag=rpg.pf.unit] run function rpg:tower_guard/ai/remove
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss] run function rpg:pope_fight/boss/remove
kill @e[type=minecraft:vindicator,tag=rpg.pf.heart]
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig] at @s run function rpg:heart_of_ender/internal/clear
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.face] at @s run function rpg:arch_visage/internal/clear
tag @a[tag=rpg.pf.tgt] remove rpg.pf.tgt
kill @e[tag=rpg.pope.fx]
stopsound @a record minecraft:boss3
stopsound @a record minecraft:boss2
stopsound @a record minecraft:boss1
kill @e[type=minecraft:marker,tag=rpg.pf.center]
bossbar set minecraft:pope players
bossbar set minecraft:pope visible false
