summon minecraft:iron_golem ~ ~ ~ {Tags:["rpg.ally","rpg.jqa","rpg.jqwear","rpg.unit","rpg.unit.ns","rpg.unit.nc","rpg.unit.f","rpg.jqa.new"],NoAI:1b,PlayerCreated:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",CustomNameVisible:1b,CustomName:["",{"text":"[圣殿誓约]","color":"#F0CF7A","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":false,"italic":false}],Health:100f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"scale",base:0.7407f},{id:"max_health",base:100f},{id:"armor",base:8f},{id:"knockback_resistance",base:0.6f}]}
execute as @e[type=minecraft:iron_golem,tag=rpg.jqa,tag=rpg.jqa.new] run function rpg:jacques_ally/init
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.2f,28f,0.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 24
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 16
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,14f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.1f,28f,0.1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 24
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 17
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:end_rod ~ ~6 ~ 0.15 6 0.15 0.01 30
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/sigil","minecraft:custom_model_data":{colors:[13111342]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.5f,1f,3.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 30
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 1
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.jqa.fx","rpg.jqa.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[16773832]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_life 12
scoreboard players set @e[tag=rpg.jqa.fxnew] rpg_al_kd 18
tag @e[tag=rpg.jqa.fxnew] remove rpg.jqa.fxnew
particle minecraft:end_rod ~0.40 ~0.20 ~0.00 1.000 0 0.000 0.3 0
particle minecraft:end_rod ~0.38 ~0.20 ~0.12 0.951 0 0.309 0.3 0
particle minecraft:end_rod ~0.32 ~0.20 ~0.24 0.809 0 0.588 0.3 0
particle minecraft:end_rod ~0.24 ~0.20 ~0.32 0.588 0 0.809 0.3 0
particle minecraft:end_rod ~0.12 ~0.20 ~0.38 0.309 0 0.951 0.3 0
particle minecraft:end_rod ~0.00 ~0.20 ~0.40 0.000 0 1.000 0.3 0
particle minecraft:end_rod ~-0.12 ~0.20 ~0.38 -0.309 0 0.951 0.3 0
particle minecraft:end_rod ~-0.24 ~0.20 ~0.32 -0.588 0 0.809 0.3 0
particle minecraft:end_rod ~-0.32 ~0.20 ~0.24 -0.809 0 0.588 0.3 0
particle minecraft:end_rod ~-0.38 ~0.20 ~0.12 -0.951 0 0.309 0.3 0
particle minecraft:end_rod ~-0.40 ~0.20 ~0.00 -1.000 0 0.000 0.3 0
particle minecraft:end_rod ~-0.38 ~0.20 ~-0.12 -0.951 0 -0.309 0.3 0
particle minecraft:end_rod ~-0.32 ~0.20 ~-0.24 -0.809 0 -0.588 0.3 0
particle minecraft:end_rod ~-0.24 ~0.20 ~-0.32 -0.588 0 -0.809 0.3 0
particle minecraft:end_rod ~-0.12 ~0.20 ~-0.38 -0.309 0 -0.951 0.3 0
particle minecraft:end_rod ~-0.00 ~0.20 ~-0.40 -0.000 0 -1.000 0.3 0
particle minecraft:end_rod ~0.12 ~0.20 ~-0.38 0.309 0 -0.951 0.3 0
particle minecraft:end_rod ~0.24 ~0.20 ~-0.32 0.588 0 -0.809 0.3 0
particle minecraft:end_rod ~0.32 ~0.20 ~-0.24 0.809 0 -0.588 0.3 0
particle minecraft:end_rod ~0.38 ~0.20 ~-0.12 0.951 0 -0.309 0.3 0
particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.8 0.4 0.4 30
