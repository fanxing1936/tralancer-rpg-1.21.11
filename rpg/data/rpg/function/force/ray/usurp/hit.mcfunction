tag @s add rpg.fo.hit
scoreboard players set #stop rpg_fo 1
tag @s add rpg.fo.hit
scoreboard players set #st rpg_fo 0
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:strength"}]}] run function rpg:force/x/l/steal_strength
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:speed"}]}] run function rpg:force/x/l/steal_speed
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:resistance"}]}] run function rpg:force/x/l/steal_resistance
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:regeneration"}]}] run function rpg:force/x/l/steal_regeneration
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:absorption"}]}] run function rpg:force/x/l/steal_absorption
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:fire_resistance"}]}] run function rpg:force/x/l/steal_fire_resistance
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:invisibility"}]}] run function rpg:force/x/l/steal_invisibility
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:jump_boost"}]}] run function rpg:force/x/l/steal_jump_boost
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:haste"}]}] run function rpg:force/x/l/steal_haste
execute if score #st rpg_fo matches 0 if entity @s[nbt={active_effects:[{id:"minecraft:health_boost"}]}] run function rpg:force/x/l/steal_health_boost
scoreboard players set #b rpg_fo 0
execute if entity @s[tag=rpg.pope] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.mkb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.jqb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.lub] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.slb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.usb] run scoreboard players set #b rpg_fo 1
execute if score #b rpg_fo matches 0 run effect give @s minecraft:slowness 5 9 true
execute if score #b rpg_fo matches 0 run effect give @s minecraft:jump_boost 5 250 true
execute if score #b rpg_fo matches 0 run effect give @s minecraft:weakness 5 4 true
execute if score #st rpg_fo matches 1 run particle minecraft:totem_of_undying ~ ~1.2 ~ 0.3 0.5 0.3 0.2 16
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..16] ~ ~ ~ 1 0.8
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8E0F0"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.75f,2.75f,2.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 4
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.fo.xm","rpg.fo.xmnew"],text:{text:"",font:"rpg:usurper_fx",color:"#A276BE"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_life 8
scoreboard players set @e[tag=rpg.fo.xmnew] rpg_fo_kd 13
tag @e[tag=rpg.fo.xmnew] remove rpg.fo.xmnew
