execute unless score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run return 0
execute if score @s rpg_end_claim matches 1.. run return 0
scoreboard players set @s rpg_end_claim 1
execute if score @s rpg_end_pick matches 1 run function rpg:endless/reward/grace
execute if score @s rpg_end_pick matches 2 run function rpg:endless/reward/judgment
execute if score @s rpg_end_pick matches 3 run function rpg:endless/reward/loot_dispatch
execute if score #boss rpg_end_tmp matches 1 run function rpg:endless/reward/boss_bonus
scoreboard players set @s rpg_end_pick 0
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.7 1.3
