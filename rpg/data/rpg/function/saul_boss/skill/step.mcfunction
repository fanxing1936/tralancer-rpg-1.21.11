scoreboard players set @s rpg_sl_sk 21
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 34
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:saul/anim/enter/vanish
execute if score @s rpg_sl matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"影步斩 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"在你身后。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl matches 2.. run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"影步斩 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"在你身后。","color":"#9C9A94","bold":false,"italic":false}]
