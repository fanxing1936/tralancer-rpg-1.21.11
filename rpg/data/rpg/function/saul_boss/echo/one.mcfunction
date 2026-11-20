summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slg","rpg.slb.echo","rpg.slb.ghostnew"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"残影","color":"#E6ECF6","italic":true},active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] remove rpg.slb.ghostnew
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.3 0.7 0.3 0 12
particle minecraft:end_rod ~ ~1 ~ 0.25 0.6 0.25 0.02 6
execute positioned ~ ~0.05 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/beam","minecraft:custom_model_data":{colors:[9213602]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,4.5f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.02f,9f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~0.05 ~ run tp @e[tag=rpg.slb.fxnew,limit=1] ~ ~ ~ ~ ~
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 22
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
