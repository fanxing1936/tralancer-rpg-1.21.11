# 契约改写（as/at 载体）。没人签契约就改用封印。
execute unless entity @e[tag=rpg.unit.f,distance=..25,scores={rpg_pact=1..7}] run return run function rpg:usurper_boss/skill/seal
scoreboard players set @s rpg_ub_sk 3
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 30
function rpg:usurper/anim/enter/enchant
execute as @e[tag=rpg.unit.f,distance=..25,scores={rpg_pact=1..7}] at @s run function rpg:usurper_boss/rewrite/mark
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"契约改写 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"你们的契约，我替你们重写一遍。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:text_display ~ ~1.8 ~ {Tags:["rpg.usb.fx","rpg.usb.fxnew"],text:{text:"",font:"rpg:usurper_fx",color:"#E8D5FF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_life 10
scoreboard players set @e[tag=rpg.usb.fxnew] rpg_ub_kd 4
tag @e[tag=rpg.usb.fxnew] remove rpg.usb.fxnew
