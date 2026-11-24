# 每秒（as/at 有力的玩家）：回力、生命力
execute if score @s rpg_force matches 1 run function rpg:sephira/force/holy_regen
execute if score @s rpg_force matches 3 run function rpg:sephira/force/holy_regen
execute if score @s rpg_force matches 2 run function rpg:sephira/force/mana_regen
execute if score @s rpg_force matches 3 run function rpg:sephira/force/mana_regen
execute if score @s rpg_force matches 1 run function rpg:sephira/force/vital_sec
execute if entity @s[tag=rpg.fallen,tag=!rpg.pact] if score @s rpg_taint matches 0 run function rpg:sephira/force/rise
execute if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max
execute if score @s rpg_mana2 > @s rpg_mana_max run scoreboard players operation @s rpg_mana2 = @s rpg_mana_max
scoreboard players operation @s rpg_fz_mv0 = @s rpg_fz_mv
scoreboard players set @s rpg_fz_dd 0
