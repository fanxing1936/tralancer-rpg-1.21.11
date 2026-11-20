scoreboard players set @s rpg_sl_sk 16
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 148
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:saul/anim/enter/vanish
tag @e[tag=rpg.unit] remove rpg.slb.failed
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔡 𝔎𝔦𝔫𝔤","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第四课 · 千刀 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"第四课，叫千刀。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:saul_boss/vfx/ult2
