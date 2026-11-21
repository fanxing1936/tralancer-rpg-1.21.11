summon minecraft:marker ~ ~ ~ {Tags:["rpg.fg.fx","rpg.fg.banner","rpg.fg.new"]}
summon minecraft:item_display ~ ~1.3 ~ {Tags:["rpg.fg.bdisp"],item:{id:"minecraft:white_banner",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.4f,1.4f,1.4f]}}
scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.new] rpg_fg_t 200
tag @e[type=minecraft:marker,tag=rpg.fg.new] remove rpg.fg.new
playsound minecraft:event.raid.horn player @a[distance=..32] ~ ~ ~ 0.6 1.4
