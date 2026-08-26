scoreboard players set @s rpg_ch1_sub 12
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"战间复盘｜敌人暂未入场","color":"#B8A98B","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[安全对白] ","color":"#B8A98B","bold":true,"italic":false},{"text":"下一轮将在对白结束后开始。","color":"gray","bold":false,"italic":false}]
