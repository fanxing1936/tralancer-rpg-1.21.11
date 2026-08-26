execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"口粮袋封签完整，袋底只有虫翅；粮食在登记后被取走。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"像盗粮，但偷粮的人不会把虫翅封进每一只空袋。","color":"gray","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/spawn/trail2
kill @e[type=minecraft:text_display,tag=rpg.ch1.trail1.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.trail1.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
