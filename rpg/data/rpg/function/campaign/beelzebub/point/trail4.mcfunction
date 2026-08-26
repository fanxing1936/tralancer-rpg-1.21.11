execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"三条路线都停在‘满仓’封条前；门内没有粮食，只有写着姓名的餐盘。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"仓库从来不是空的。空的是被端上桌的人。","color":"gray","bold":false,"italic":false}]
kill @e[type=minecraft:text_display,tag=rpg.ch1.trail4.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.trail4.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
