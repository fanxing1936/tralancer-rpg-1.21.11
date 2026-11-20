scoreboard players set @s rpg_sl_sk 24
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 184
tag @s add rpg.slb.danced
data merge entity @s {NoAI:1b,Invulnerable:1b}
function rpg:saul/anim/enter/hero
execute as @e[tag=rpg.unit.f,distance=..40] run effect give @s minecraft:darkness 6 0 true
function rpg:saul_boss/vfx/ult2
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔡 𝔎𝔦𝔫𝔤","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"疯王之舞 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"……还没完。还没完！斯塔福德，看——这是我最后的剑！","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:entity.warden.roar hostile @a[distance=..48] ~ ~ ~ 1 1.4
