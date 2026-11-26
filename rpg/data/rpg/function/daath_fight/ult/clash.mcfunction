scoreboard players set @s rpg_dt_sk 24
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
function rpg:daath_fight/weapon/pick_melee
function rpg:daath/anim/enter/mighty
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
data merge entity @s {NoAI:1b,Invulnerable:0b}
title @a[tag=rpg.dt.me,limit=1] times 5 35 12
title @a[tag=rpg.dt.me,limit=1] subtitle ["",{"text":"ℑ𝔡𝔢𝔪 𝔊𝔩𝔞𝔡𝔦𝔲𝔰","color":"#8F7430","bold":false,"italic":false}]
title @a[tag=rpg.dt.me,limit=1] title ["",{"text":"同一把剑","color":"#FFFFFF","bold":true,"italic":false}]
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"同一把剑。看谁先落下。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　The same blade. Let us see whose falls first.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s14 voice @s ~ ~ ~ 1 1 1
function rpg:daath_fight/clash/back
tag @s add rpg.dt.clash
