summon minecraft:text_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],text:{text:"",font:"rpg:lucifer_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[3.25f,3.25f,3.25f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 30
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 52
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
