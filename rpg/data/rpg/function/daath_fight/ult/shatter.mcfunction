scoreboard players set @s rpg_dt_sk 25
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/gong
data merge entity @s {NoAI:1b,Invulnerable:1b}
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~ ~ ~
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"𝔖𝔭𝔢𝔠𝔲𝔩𝔲𝔪 𝔉𝔯𝔞𝔠𝔱𝔲𝔪","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"碎镜","color":"#FFFFFF","bold":true,"italic":false}]
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"镜子碎了，你还在吗？","color":"#E6DFCF","bold":false,"italic":false},{"text":"　When the glass breaks, are you still there?","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s15 voice @s ~ ~ ~ 1 1 1
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.6 0.5
