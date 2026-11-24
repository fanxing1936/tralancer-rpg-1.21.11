function rpg:force/unholy
execute unless score #u rpg_fo matches 1 run return 0
scoreboard players set #b rpg_fo 0
execute if entity @s[tag=rpg.pope] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.mkb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.jqb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.lub] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.slb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.usb] run scoreboard players set #b rpg_fo 1
execute if score #b rpg_fo matches 1 run return run effect give @s minecraft:slowness 2 1 true
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:slowness 2 9 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:slowness 3 9 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:slowness 4 9 true
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:jump_boost 2 250 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:jump_boost 3 250 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:jump_boost 4 250 true
execute if score #lv rpg_fo matches 1 run effect give @s minecraft:weakness 2 4 true
execute if score #lv rpg_fo matches 2 run effect give @s minecraft:weakness 3 4 true
execute if score #lv rpg_fo matches 3 run effect give @s minecraft:weakness 4 4 true
summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.75f,1.75f,1.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 16
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 16
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
particle minecraft:wax_off ~ ~2 ~ 0.3 0.2 0.3 0 6
