# 刑台（广场中间，地下城的吊笼与柴堆模型由 add_town_models 挂上）：女巫、审判官、两名圣卫、兜帽人
summon minecraft:villager ~ ~ ~ {Tags:["rpg.tw.ev","rpg.tnpc","rpg.tnpc.witch","rpg.te.witch"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"女巫","color":"#B48AD8","bold":true,"italic":false},VillagerData:{type:"minecraft:swamp",profession:"minecraft:none",level:1}}
execute as @e[type=minecraft:villager,tag=rpg.te.witch,distance=..1] at @s run function #rpg:town_dress
execute positioned ~ ~ ~1 run function rpg:town/prop {n:"pyre"}
execute positioned ~ ~ ~ run function rpg:town/prop {n:"cage"}
summon minecraft:vindicator ~3 ~ ~ {Tags:["rpg.te.inq.new"],PersistenceRequired:1b,CanPickUpLoot:0b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:90},{id:"minecraft:armor",base:10},{id:"minecraft:attack_damage",base:7}],Health:90f}
execute as @e[type=minecraft:vindicator,tag=rpg.te.inq.new,limit=1] at @s run function rpg:town/ev/w/inq
execute positioned ~-4 ~ ~3 run function rpg:tower_guard/summon
execute positioned ~4 ~ ~-3 run function rpg:tower_guard/summon
execute as @e[tag=rpg.tg,distance=..8,tag=!rpg.tw.guard] run function rpg:town/ev/w/guard
execute positioned ^ ^ ^-10 positioned over motion_blocking_no_leaves run function rpg:town/ev/w/hood
