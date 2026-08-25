execute store result score @s rpg_ex_counter run random value 180..260
execute if entity @s[tag=rpg.layout.suppress] run scoreboard players add @s rpg_ex_counter 80
execute if score @s rpg_dm_lord matches 1 run return run function rpg:inquest/counter/start1
execute if score @s rpg_dm_lord matches 2 run return run function rpg:inquest/counter/start2
execute if score @s rpg_dm_lord matches 3 run return run function rpg:inquest/counter/start3
execute if score @s rpg_dm_lord matches 4 run return run function rpg:inquest/counter/start4
execute if score @s rpg_dm_lord matches 5 run return run function rpg:inquest/counter/start5
execute if score @s rpg_dm_lord matches 6 run return run function rpg:inquest/counter/start6
execute if score @s rpg_dm_lord matches 7 run return run function rpg:inquest/counter/start7
