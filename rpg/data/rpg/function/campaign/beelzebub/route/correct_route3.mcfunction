kill @e[type=minecraft:text_display,tag=rpg.ch1.route3.label,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.route3,distance=..72]
scoreboard players add @s rpg_ch1_choice 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[排序成立] ","color":"#62D9E8","bold":true,"italic":false},{"text":"第七粮仓","color":"gray","bold":false,"italic":false}]
scoreboard players set @s rpg_ch1_sub 2
scoreboard players set @s rpg_ch1_time 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[密文解开] ","color":"#B8A98B","bold":true,"italic":false},{"text":"车辙从慈济所出发，以处决名册挑选货物，最终汇入第七粮仓。","color":"gray","bold":false,"italic":false}]
