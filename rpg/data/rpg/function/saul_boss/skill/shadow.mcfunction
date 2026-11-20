scoreboard players set @s rpg_sl_sk 9
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 60
data merge entity @s {NoAI:1b}
tp @s ~ ~ ~ ~110 0
function rpg:saul/anim/enter/shadow
attribute @s minecraft:armor base set 7
execute at @s positioned ^ ^ ^2.6 rotated ~180 0 run function rpg:saul_boss/shadow/phantom
execute if score @s rpg_sl matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"对着空气练剑 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"老伙计，再来一次！……对，就是这样……","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl matches 2.. run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"对着空气练剑 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"老伙计，再来一次！……对，就是这样……","color":"#9C9A94","bold":false,"italic":false}]
