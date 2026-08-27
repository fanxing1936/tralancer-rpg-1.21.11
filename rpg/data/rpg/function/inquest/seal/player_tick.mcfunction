scoreboard players add @s rpg_agit 0
scoreboard players add @s rpg_rel_cd 0
scoreboard players add @s rpg_rel_gap 0
scoreboard players add @s rpg_seal_i 1
execute if score @s rpg_rel_cd matches 1.. run scoreboard players remove @s rpg_rel_cd 1
execute if score @s rpg_rel_gap matches 1.. run scoreboard players remove @s rpg_rel_gap 1
execute if score @s rpg_rel_gap matches ..0 run scoreboard players set @s rpg_rel_hold 0
execute if score @s rpg_seal_i matches 100.. run function rpg:inquest/seal/reindex
execute if entity @s[tag=rpg.seal.carrier] run function rpg:inquest/seal/tick
