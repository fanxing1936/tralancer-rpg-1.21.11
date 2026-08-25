execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"毒马铃薯被整齐推出餐盘：祂拒食自行腐败之物。","color":"gray","bold":false,"italic":false}]
tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.done.hyp.3
kill @e[type=minecraft:text_display,tag=rpg.ch1.hyp3.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.hyp3.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
