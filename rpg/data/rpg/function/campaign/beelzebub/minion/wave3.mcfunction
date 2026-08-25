scoreboard players set @s rpg_ch1_sub 3
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第三轮 · 处刑者","color":"#5A6B1E","bold":true,"italic":false}]
execute positioned ^ ^ ^30 run function rpg:campaign/beelzebub/spawn/minion/purson
tellraw @a[tag=rpg.ch1.current] ["",{"text":"布松：","color":"#5A6B1E","bold":true,"italic":false},{"text":"见证不是事实。活下来的见证才是。","color":"gray","bold":false,"italic":false}]
