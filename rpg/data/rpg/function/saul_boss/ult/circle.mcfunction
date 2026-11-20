scoreboard players set @s rpg_sl_sk 11
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 112
data merge entity @s {NoAI:1b}
function rpg:saul/anim/enter/twirl
tag @e[tag=rpg.unit] remove rpg.slb.failed
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔯𝔰𝔥𝔞𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"第二课 · 圆 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"剑也走圆。站对地方。","color":"#9C9A94","bold":false,"italic":false}]
execute positioned ~ ~0.05 ~ run function rpg:saul_boss/circle/warn0
execute positioned ~ ~0.05 ~ run function rpg:saul_boss/circle/warn1
execute positioned ~ ~0.05 ~ run function rpg:saul_boss/circle/warn2
