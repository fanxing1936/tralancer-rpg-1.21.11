execute if score @s rpg_agit matches ..39 run tag @s remove rpg.seal.warn40
execute if score @s rpg_agit matches ..69 run tag @s remove rpg.seal.warn70
execute if score @s rpg_agit matches ..89 run tag @s remove rpg.seal.warn90
execute if score @s rpg_agit matches 40..69 unless entity @s[tag=rpg.seal.warn40] run function rpg:inquest/seal/warn_agitated
execute if score @s rpg_agit matches 70..89 unless entity @s[tag=rpg.seal.warn70] run function rpg:inquest/seal/warn_danger
execute if score @s rpg_agit matches 70..89 if entity @s[tag=rpg.seal.warn70] if score @s rpg_rel_w matches 200.. run function rpg:inquest/seal/warn_danger
execute if score @s rpg_agit matches 90..99 unless entity @s[tag=rpg.seal.warn90] run function rpg:inquest/seal/warn_critical
execute if score @s rpg_agit matches 90..99 if entity @s[tag=rpg.seal.warn90] if score @s rpg_rel_w matches 60.. run function rpg:inquest/seal/warn_critical
