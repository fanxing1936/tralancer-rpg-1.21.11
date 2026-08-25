
scoreboard players add @s player_level 0
execute if score @s level > @s player_level run function rpg:level/up
execute unless score @s rpg_hp_level = @s player_level run function rpg:level/sync_health
