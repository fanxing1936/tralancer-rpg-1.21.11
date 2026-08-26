scoreboard players set @s rpg_ch1_sub 1
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第1轮 · 封路与追猎","color":"#5A6B1E","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[战斗开始] ","color":"#8B2500","bold":true,"italic":false},{"text":"第 1 轮罪仆越过封锁线；守住见证人。","color":"gray","bold":false,"italic":false}]
execute positioned ^8 ^ ^18 run function rpg:campaign/beelzebub/spawn/minion/zepar
execute positioned ^-8 ^ ^18 run function rpg:campaign/beelzebub/spawn/minion/botis
