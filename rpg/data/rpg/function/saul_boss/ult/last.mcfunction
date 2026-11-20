scoreboard players set @s rpg_sl_sk 17
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 137
data merge entity @s {NoAI:1b}
execute at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] facing entity @s feet positioned ^ ^ ^15 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:saul/anim/enter/mighty
tag @e[tag=rpg.unit] remove rpg.slb.failed
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔡 𝔎𝔦𝔫𝔤","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"最后一课 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"最后一课，斯塔福德。看清楚。","color":"#9C9A94","bold":false,"italic":false}]
execute at @s positioned ~ ~0.05 ~ run function rpg:saul_boss/last/aim
execute at @s run function rpg:saul_boss/vfx/ult2
