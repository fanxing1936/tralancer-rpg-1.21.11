scoreboard players remove @s rpg_ex_wave 1
execute if score @s rpg_ex_wave matches 12 run function rpg:inquest/phase2/wave_dispatch
execute if score @s rpg_ex_wave matches 1 run function rpg:inquest/phase2/wave_dispatch
