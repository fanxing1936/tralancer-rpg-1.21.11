scoreboard players set @s rpg_ch1_sub 3
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第3轮 · 处刑","color":"#5A6B1E","bold":true,"italic":false}]
execute positioned ^ ^ ^30 run function rpg:campaign/beelzebub/spawn/minion/purson
tellraw @a[tag=rpg.ch1.current] ["",{"text":"布松：","color":"#5A6B1E","bold":true,"italic":false},{"text":"见证不是事实。活下来的见证才是。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"处决令早于所谓疫病。它们不是来止灾，是来让灾情没人能说出口。","color":"gray","bold":false,"italic":false}]
