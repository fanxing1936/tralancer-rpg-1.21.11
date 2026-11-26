scoreboard players set @s rpg_dt_sk 23
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/mighty
data merge entity @s {NoAI:1b,Invulnerable:1b}
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~ ~ ~
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"𝔑𝔬𝔰𝔠𝔢 𝔱𝔢 𝔦𝔭𝔰𝔲𝔪","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"认识你自己","color":"#FFFFFF","bold":true,"italic":false}]
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"认识你自己。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Know yourself.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s11 voice @s ~ ~ ~ 1 1 1
function rpg:daath_fight/lamp/all_out
function rpg:daath_fight/ask/make
playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
