scoreboard players set #pick rpg_l2_v 7
function rpg:lucifer_fight/p1/begin
scoreboard players set @s rpg_dm_cd 30
function rpg:lucifer_lord/play/strong
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"蛇之后裔 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"起来，我的后裔。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/root_sigil"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.05f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 1
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 110
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 2 0.2 2 0.1 40
playsound minecraft:block.rooted_dirt.break hostile @a[distance=..32] ~ ~ ~ 1.2 0.6
