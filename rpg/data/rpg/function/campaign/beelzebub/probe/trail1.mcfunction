scoreboard players set #ch1_point_ok rpg_ch1_seen 0
tag @s add rpg.ch1.point.active
execute as @a[tag=rpg.ch1.current,distance=..2.8,sort=nearest,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run scoreboard players set #ch1_point_ok rpg_ch1_seen 1
execute if score #ch1_point_ok rpg_ch1_seen matches 1 run scoreboard players add @s rpg_ch1_seen 1
execute if score #ch1_point_ok rpg_ch1_seen matches 0 run scoreboard players set @s rpg_ch1_seen 0
execute if score @s rpg_ch1_seen matches 20 run playsound minecraft:block.amethyst_block.chime player @a[tag=rpg.ch1.current,distance=..8] ~ ~ ~ 0.35 1.4
execute if score @s rpg_ch1_seen matches 40.. as @a[tag=rpg.ch1.current,distance=..2.8,sort=nearest,limit=1] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.point.active,limit=1] rpg_ch1_id run return run function rpg:campaign/beelzebub/point/trail1
tag @s remove rpg.ch1.point.active
