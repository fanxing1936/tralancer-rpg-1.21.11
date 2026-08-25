execute store result score @s rpg_ex_pressure_roll run random value 1..3
execute store result score @s rpg_ex_pressure run random value 280..360
function rpg:inquest/phase2/pressure_core
function rpg:minion/phase2_summon
execute if score @s rpg_dm_lord matches 1 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/1_1
execute if score @s rpg_dm_lord matches 1 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/1_2
execute if score @s rpg_dm_lord matches 1 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/1_3
execute if score @s rpg_dm_lord matches 2 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/2_1
execute if score @s rpg_dm_lord matches 2 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/2_2
execute if score @s rpg_dm_lord matches 2 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/2_3
execute if score @s rpg_dm_lord matches 3 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/3_1
execute if score @s rpg_dm_lord matches 3 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/3_2
execute if score @s rpg_dm_lord matches 3 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/3_3
execute if score @s rpg_dm_lord matches 4 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/4_1
execute if score @s rpg_dm_lord matches 4 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/4_2
execute if score @s rpg_dm_lord matches 4 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/4_3
execute if score @s rpg_dm_lord matches 5 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/5_1
execute if score @s rpg_dm_lord matches 5 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/5_2
execute if score @s rpg_dm_lord matches 5 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/5_3
execute if score @s rpg_dm_lord matches 6 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/6_1
execute if score @s rpg_dm_lord matches 6 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/6_2
execute if score @s rpg_dm_lord matches 6 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/6_3
execute if score @s rpg_dm_lord matches 7 if score @s rpg_ex_pressure_roll matches 1 run function rpg:inquest/phase2/pressure/7_1
execute if score @s rpg_dm_lord matches 7 if score @s rpg_ex_pressure_roll matches 2 run function rpg:inquest/phase2/pressure/7_2
execute if score @s rpg_dm_lord matches 7 if score @s rpg_ex_pressure_roll matches 3 run function rpg:inquest/phase2/pressure/7_3
