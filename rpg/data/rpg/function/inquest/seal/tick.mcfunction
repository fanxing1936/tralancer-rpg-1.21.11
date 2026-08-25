scoreboard players add @s rpg_seal_t 1
execute if score @s rpg_seal_t matches 12000.. run execute store result score @s rpg_seal_roll run random value 1..6
execute if score @s rpg_seal_t matches 12000.. run scoreboard players set @s rpg_seal_t 0
execute if score @s rpg_seal_roll matches 1 run function rpg:inquest/seal/escape
execute if score @s rpg_seal_roll matches 1.. run scoreboard players set @s rpg_seal_roll 0
