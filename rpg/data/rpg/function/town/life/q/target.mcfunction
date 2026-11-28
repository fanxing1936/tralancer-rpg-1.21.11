summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tl.target"],width:0.8f,height:1.6f}
summon minecraft:block_display ~-0.3 ~ ~-0.3 {Tags:["rpg.tl.tdisp"],block_state:{Name:"minecraft:target"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,1.4f,0.6f]}}
scoreboard players set @e[type=minecraft:interaction,tag=rpg.tl.target,distance=..0.5] rpg_tl 30
