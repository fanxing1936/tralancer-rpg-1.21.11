execute unless entity @s[tag=rpg.ch1.slot.1] run return 0
execute unless entity @s[tag=rpg.ch1.slot.2] run return 0
execute unless entity @s[tag=rpg.ch1.slot.3] run return 0
scoreboard players set @s rpg_ch1_sub 2
scoreboard players set @s rpg_ch1_time 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[校准完成] ","color":"#B8A98B","bold":true,"italic":false},{"text":"边界、拒食与见证三环已经互相闭合；现在才适合进入 Boss 战。","color":"gray","bold":false,"italic":false}]
