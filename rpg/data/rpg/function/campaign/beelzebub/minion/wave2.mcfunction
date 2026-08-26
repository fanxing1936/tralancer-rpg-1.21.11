scoreboard players set @s rpg_ch1_sub 2
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第2轮 · 转运与伪记忆","color":"#5A6B1E","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[战斗开始] ","color":"#8B2500","bold":true,"italic":false},{"text":"第 2 轮罪仆越过封锁线；守住见证人。","color":"gray","bold":false,"italic":false}]
execute positioned ^12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/bathin
execute positioned ^-12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/sallos
