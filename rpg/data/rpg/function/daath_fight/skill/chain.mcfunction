# 一套连招：2 到 6 下
execute store result score @s rpg_dt_cl run random value 2..4
execute if score @s rpg_dt_st matches 2 run execute store result score @s rpg_dt_cl run random value 3..6
function rpg:daath_fight/weapon/pick
execute if score @s rpg_dt_wc matches 8..9 run return run function rpg:daath_fight/skill/shoot
scoreboard players set @s rpg_dt_sk 1
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
scoreboard players set @s rpg_dt_ht 999
scoreboard players set @s rpg_dt_ln 10
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
function rpg:daath/anim/enter/guard
summon minecraft:text_display ^-0.4 ^1.6 ^0.5 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 10
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 7
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:item.trident.riptide_1 hostile @a[distance=..24] ~ ~ ~ 0.5 1.7
