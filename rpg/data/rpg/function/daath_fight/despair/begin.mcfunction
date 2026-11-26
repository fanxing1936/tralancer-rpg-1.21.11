tag @s add rpg.dt.desp
tag @s add rpg.dt.mute
scoreboard players set @s rpg_dt_t 0
scoreboard players set @s rpg_dt_i 0
function rpg:daath_fight/unit/refill
function rpg:daath_fight/hp_low
data merge entity @s {NoAI:1b,Invulnerable:1b}
execute if score @s rpg_dt_sw matches 1.. run function rpg:daath_fight/steal/lose_w
execute if score @s rpg_dt_sa matches 1.. run function rpg:daath_fight/steal/lose_a
function rpg:daath_fight/eye/off
kill @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..60]
stopsound @a[tag=rpg.dt.me,limit=1] record
function rpg:daath/anim/enter/walk
effect give @a[tag=rpg.dt.me,limit=1] minecraft:blindness 1 0 true
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound minecraft:entity.warden.heartbeat record @s ~ ~ ~ 1 0.8
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"𝔔𝔲𝔦𝔰 𝔘𝔪𝔟𝔯𝔞","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"谁是影子","color":"#FFFFFF","bold":true,"italic":false}]
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"别打了。看着我。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Stop. Look at me.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s16 voice @s ~ ~ ~ 1 1 1
