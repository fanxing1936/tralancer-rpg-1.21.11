# 别的配乐在放：让路
execute if entity @s[tag=rpg.pr] run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @s[tag=rpg.ob] run return run scoreboard players set @s rpg_bgm_w 0
execute if score @s rpg_ob_mi matches 1.. run return run scoreboard players set @s rpg_bgm_w 0
execute if score @s rpg_q_mt matches 1.. run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @e[type=minecraft:marker,tag=rpg.jqb.center,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @e[type=minecraft:marker,tag=rpg.lub.center,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @e[type=minecraft:marker,tag=rpg.mkb.center,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @e[type=minecraft:marker,tag=rpg.slb.center,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @e[type=minecraft:marker,tag=rpg.usb.center,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0
execute if entity @e[type=minecraft:marker,tag=rpg.pf.center,distance=..56] run return run scoreboard players set @s rpg_bgm_w 0
