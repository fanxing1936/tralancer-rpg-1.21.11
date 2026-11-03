summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fm.part","rpg.fm.new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:full_metal_chestplate"}},item_display:"none",teleport_duration:1,view_range:1f,transformation:{translation:[0f,1.0625f,0.0625f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.new] rpg_fm_id = #id rpg_fm_id
tag @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.new] add rpg.fm.mine
tag @e[type=minecraft:item_display,tag=rpg.fm.part,tag=rpg.fm.new] remove rpg.fm.new
