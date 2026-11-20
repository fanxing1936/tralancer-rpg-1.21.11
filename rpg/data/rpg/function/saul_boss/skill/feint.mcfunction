scoreboard players set @s rpg_sl_sk 15
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 46
data merge entity @s {NoAI:1b}
execute store result score #r rpg_sl run random value 0..1
execute if score #r rpg_sl matches 0 run tp @s ~ ~ ~ ~75 0
execute if score #r rpg_sl matches 1 run tp @s ~ ~ ~ ~-75 0
function rpg:saul/anim/enter/final
execute if score @s rpg_sl matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"错招 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"在那儿！……咦？","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl matches 2.. run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"错招 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"在那儿！……咦？","color":"#9C9A94","bold":false,"italic":false}]
