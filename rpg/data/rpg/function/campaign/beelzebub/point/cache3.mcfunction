execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"裁决箱：四种路线器具都在，说明教廷预期你完成一次看似合法的裁决。","color":"gray","bold":false,"italic":false}]
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/bell
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/incense
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/chalk1
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/lantern
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"四种裁决都能启动。也正因为都能启动，缺页才更像故意留下的缺口。","color":"gray","bold":false,"italic":false}]
kill @e[type=minecraft:text_display,tag=rpg.ch1.cache3.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.cache3.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
