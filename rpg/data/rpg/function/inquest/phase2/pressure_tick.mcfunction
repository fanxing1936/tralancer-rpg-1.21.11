scoreboard players remove @s rpg_ex_pressure 1
execute if score @s rpg_ex_pressure matches 40 run function rpg:inquest/phase2/pressure_warning
execute if score @s rpg_ex_pressure matches ..0 run function rpg:inquest/phase2/pressure
