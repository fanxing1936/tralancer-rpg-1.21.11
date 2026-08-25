scoreboard players set @s rpg_ch1_sub 2
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"五席未满｜第二轮 · 转运与伪记忆","color":"#5A6B1E","bold":true,"italic":false}]
execute positioned ^12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/bathin
execute positioned ^-12 ^ ^26 run function rpg:campaign/beelzebub/spawn/minion/sallos
tellraw @a[tag=rpg.ch1.current] ["",{"text":"虚假的家人：","color":"#706B5E","bold":true,"italic":false},{"text":"回来吃饭吧。战争已经结束了。","color":"gray","bold":false,"italic":false}]
