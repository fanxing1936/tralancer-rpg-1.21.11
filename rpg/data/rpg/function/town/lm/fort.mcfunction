# 孤堡门前（教廷前哨）：四名站岗的圣卫与一位审判官；恶魔阵营的人靠近就醒
execute positioned ~4 ~ ~2 run function rpg:tower_guard/summon
execute positioned ~-4 ~ ~2 run function rpg:tower_guard/summon
execute positioned ~8 ~ ~4 run function rpg:royal_guard/summon
execute positioned ~-8 ~ ~4 run function rpg:royal_guard/summon
execute as @e[tag=rpg.hg,distance=..12] run data merge entity @s {NoAI:1b,PersistenceRequired:1b}
tag @e[tag=rpg.hg,distance=..12] add rpg.lm.guard
summon minecraft:vindicator ~ ~ ~3 {Tags:["rpg.te.inq","rpg.lm.guard","rpg.lm.inq"],NoAI:1b,PersistenceRequired:1b,CanPickUpLoot:0b,CustomName:{"text":"审判官","color":"#B8902F","bold":true,"italic":false},active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:160},{id:"minecraft:armor",base:14},{id:"minecraft:attack_damage",base:10}],Health:160f}
execute as @e[type=minecraft:vindicator,tag=rpg.lm.inq,distance=..6] at @s run function #rpg:town_dress
