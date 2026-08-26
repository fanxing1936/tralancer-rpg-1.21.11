execute unless entity @s[tag=rpg.ch1.theory.1] run return 0
execute unless entity @s[tag=rpg.ch1.theory.2] run return 0
kill @e[type=minecraft:marker,tag=rpg.ch1.theory3,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.theory3.label,distance=..72]
scoreboard players set @s rpg_ch1_sub 2
scoreboard players set @s rpg_ch1_time 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[假说保留] ","color":"#B5D957","bold":true,"italic":false},{"text":"暴食寄生是唯一未被证物反驳的解释，但仍必须在 Boss 战亲历权能才能确证真名。","color":"gray","bold":false,"italic":false}]
