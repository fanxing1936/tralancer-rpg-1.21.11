scoreboard players set @s rpg_ch1_sub 2
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第2轮 · 转运与伪记忆","color":"#5A6B1E","bold":true,"italic":false}]
execute positioned ^12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/bathin
execute positioned ^-12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/sallos
tellraw @a[tag=rpg.ch1.current] ["",{"text":"虚假的家人：","color":"#706B5E","bold":true,"italic":false},{"text":"回来吃饭吧。战争已经结束了。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"夺回的转运单盖着卡西安的印。先记作‘参与’，不要急着写成‘源头’。","color":"gray","bold":false,"italic":false}]
