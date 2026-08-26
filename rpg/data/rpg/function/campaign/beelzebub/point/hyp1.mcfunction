execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"炉灰中没有灼烧骨骼，只有带牙印的餐盘灰；排除普通焚尸。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"火灾说不能成立。灰是‘吃剩后’出现，不是燃烧后。","color":"gray","bold":false,"italic":false}]
tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.done.hyp.1
kill @e[type=minecraft:text_display,tag=rpg.ch1.hyp1.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.hyp1.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
