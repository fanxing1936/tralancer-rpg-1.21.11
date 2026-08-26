bossbar set rpg:chapter1 value 58
bossbar set rpg:chapter1 name ["",{"text":"粮仓门内｜Boss 尚未入场","color":"#B8A98B","bold":true,"italic":false}]
scoreboard players set @s rpg_ch1_seen 0
scoreboard players set @s rpg_ch1_sub 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[安全对白] ","color":"#B8A98B","bold":true,"italic":false},{"text":"别西卜将在简报结束后现身；此时没有战斗压力。","color":"gray","bold":false,"italic":false}]
