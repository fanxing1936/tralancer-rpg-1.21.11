execute unless entity @s[type=minecraft:player,tag=rpg.end.member.current,gamemode=!spectator] run return 0
execute if entity @s[nbt={Health:0.0f}] run return 0
execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] run return 0
execute unless score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run return 0
execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller.current,distance=..96] run return 0
execute unless score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_state matches 1 run return 0
scoreboard players operation #supply_mod rpg_end_tmp = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_floor
scoreboard players set #five rpg_end_tmp 5
scoreboard players operation #supply_mod rpg_end_tmp %= #five rpg_end_tmp
execute unless score #supply_mod rpg_end_tmp matches 0 run return 0
scoreboard players operation #supply_lord rpg_end_tmp = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_floor
scoreboard players operation #supply_lord rpg_end_tmp /= #five rpg_end_tmp
scoreboard players remove #supply_lord rpg_end_tmp 1
scoreboard players set #supply_seven rpg_end_tmp 7
scoreboard players operation #supply_lord rpg_end_tmp %= #supply_seven rpg_end_tmp
scoreboard players add #supply_lord rpg_end_tmp 1
scoreboard players operation @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord = #supply_lord rpg_end_tmp
execute if score @s rpg_end_kit_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id if score @s rpg_end_kit_floor = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_floor run return 0
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 1 run return run function rpg:endless/supply/kit1
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 2 run return run function rpg:endless/supply/kit2
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 3 run return run function rpg:endless/supply/kit3
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 4 run return run function rpg:endless/supply/kit4
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 5 run return run function rpg:endless/supply/kit5
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 6 run return run function rpg:endless/supply/kit6
execute if score @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_kit_lord matches 7 run return run function rpg:endless/supply/kit7
