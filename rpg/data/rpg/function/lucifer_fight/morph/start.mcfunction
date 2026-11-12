function rpg:lucifer_fight/cancel
tag @s add rpg.lu2f.morph
scoreboard players set @s rpg_l2_t 0
scoreboard players set @s rpg_dm_ult 0
function rpg:lucifer_fight/hold
effect give @s minecraft:resistance 6 4 true
execute unless score @s rpg_l2_id matches 1.. run function rpg:lucifer_fight/new_id
function rpg:lucifer_lord/play/laugh
tellraw @a[distance=..32] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":" 𝔏𝔲𝔠𝔦𝔣𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"蛇回到了树上。","color":"#9C9A94","bold":false,"italic":false}]
playsound rpg:lucifer_p2.intro_foley hostile @a[distance=..48] ~ ~ ~ 1.4 1
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~1 ~ 1 1.2 1 0.04 40
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/root_sigil"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 1
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 110
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
