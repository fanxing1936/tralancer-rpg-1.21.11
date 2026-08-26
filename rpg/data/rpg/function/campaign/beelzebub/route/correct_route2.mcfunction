kill @e[type=minecraft:text_display,tag=rpg.ch1.route2.label,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.route2,distance=..72]
scoreboard players add @s rpg_ch1_choice 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[排序成立] ","color":"#62D9E8","bold":true,"italic":false},{"text":"慈济所车辙","color":"gray","bold":false,"italic":false}]
