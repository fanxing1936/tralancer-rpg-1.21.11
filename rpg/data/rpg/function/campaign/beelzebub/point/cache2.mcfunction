execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"圣器箱：图腾、水与银钉齐全；配置足以开阵，却不足以补写见证。","color":"gray","bold":false,"italic":false}]
execute as @a[tag=rpg.ch1.current] run function rpg:campaign/beelzebub/give/totem
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/strong_water
execute as @a[tag=rpg.ch1.current] run function rpg:inquest/give/nail
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"腐败媒介阻止吞食，银钉固定边缘；它们能拖住祂，不能替死者作证。","color":"gray","bold":false,"italic":false}]
kill @e[type=minecraft:text_display,tag=rpg.ch1.cache2.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.cache2.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
