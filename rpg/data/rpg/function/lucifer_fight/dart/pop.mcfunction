particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.2} ~ ~ ~ 0.15 0.15 0.15 0.05 6
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 23
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 16
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
kill @s
