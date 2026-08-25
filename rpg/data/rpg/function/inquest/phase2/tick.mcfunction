scoreboard players remove @s rpg_ex_phase 1
execute if score @s rpg_ex_phase matches 20 run function rpg:inquest/phase2/warning
execute if score @s rpg_ex_phase matches ..0 run function rpg:inquest/phase2/pressure
