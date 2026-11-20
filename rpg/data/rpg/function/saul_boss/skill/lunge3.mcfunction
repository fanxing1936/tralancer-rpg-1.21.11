scoreboard players set @s rpg_sl_sk 13
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 66
data merge entity @s {NoAI:1b}
execute if score @s rpg_sl matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"三连突刺 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"一、二、三！","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl matches 2.. run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"三连突刺 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"一、二、三！","color":"#9C9A94","bold":false,"italic":false}]
