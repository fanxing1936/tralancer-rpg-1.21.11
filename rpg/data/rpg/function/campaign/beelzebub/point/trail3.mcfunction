execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_obj 1
playsound minecraft:block.enchantment_table.use player @a[tag=rpg.ch1.current,distance=..24] ~ ~ ~ 0.55 1.35
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"[调查] ","color":"#B8A98B","bold":true,"italic":false},{"text":"配给牌上的姓名与明日处决名单重合，日期却早了两周。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current,distance=..24] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"这些记录早于卡西安接任。他是执行者，不是全部解释。","color":"gray","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/spawn/trail4
kill @e[type=minecraft:text_display,tag=rpg.ch1.trail3.label,distance=..2]
execute as @e[type=minecraft:item_display,tag=rpg.ch1.trail3.prop,distance=..3] if score @s rpg_ch1_id = @e[tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run kill @s
kill @e[type=minecraft:marker,tag=rpg.ch1.point.active,distance=..0.1]
