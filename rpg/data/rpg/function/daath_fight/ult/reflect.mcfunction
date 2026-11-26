scoreboard players set @s rpg_dt_sk 21
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/vanish
data merge entity @s {NoAI:1b,Invulnerable:1b}
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"ℑ𝔫𝔳𝔢𝔯𝔰𝔦𝔬","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"倒影","color":"#AAB4C3","bold":true,"italic":false}]
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"往下看。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Look down.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s06 voice @s ~ ~ ~ 1 1 1
playsound rpg:daath.splinter hostile @a[distance=..48] ~ ~ ~ 1.2 0.8
playsound minecraft:entity.generic.splash hostile @a[distance=..48] ~ ~ ~ 1.4 0.4
