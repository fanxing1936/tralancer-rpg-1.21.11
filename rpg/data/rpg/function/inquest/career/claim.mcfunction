execute if score @s rpg_ex_lvl matches 2.. unless entity @s[tag=rpg.ex.claim2] if score @s rpg_ex_path matches 1..3 run function rpg:inquest/career/claim2
execute if score @s rpg_ex_lvl matches 3.. unless entity @s[tag=rpg.ex.claim3] if score @s rpg_ex_path matches 1..3 run function rpg:inquest/career/claim3
execute if score @s rpg_ex_lvl matches 4.. unless entity @s[tag=rpg.ex.claim4] run function rpg:inquest/career/claim4
execute if score @s rpg_ex_lvl matches 5.. unless entity @s[tag=rpg.ex.claim5] run function rpg:inquest/career/claim5
