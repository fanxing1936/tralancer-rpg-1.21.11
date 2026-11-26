# 还盔甲（as/at 影子）
scoreboard players set @s rpg_dt_sa 0
scoreboard players set @s rpg_dt_sp 0
execute as @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/steal/give_one_a
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"拿回去吧。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Take it back.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s23 voice @s ~ ~ ~ 1 1 1
summon minecraft:text_display ~ ~1.2 ~ {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5875f,2.5875f,2.5875f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 18
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 30
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:item.armor.equip_chain hostile @a[distance=..48] ~ ~ ~ 1.2 1.2
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..48] ~ ~ ~ 1 1.2
function rpg:daath/wear/all
execute if entity @s[tag=!rpg.dt.lit] if score @s rpg_dt_st matches 1 run function rpg:daath/look/dark
