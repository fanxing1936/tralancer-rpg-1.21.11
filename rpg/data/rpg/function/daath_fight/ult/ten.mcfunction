scoreboard players set @s rpg_dt_sk 22
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath/anim/enter/twirl
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"𝔇𝔢𝔠𝔢𝔪 𝔘𝔪𝔟𝔯𝔞𝔢","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"十影","color":"#AAB4C3","bold":true,"italic":false}]
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"哪一个是你？","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Which one is you?","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s07 voice @s ~ ~ ~ 1 1 1
function rpg:daath_fight/lamp/all_out
playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.2 0.5
data merge entity @s {NoAI:1b,Invulnerable:1b}
