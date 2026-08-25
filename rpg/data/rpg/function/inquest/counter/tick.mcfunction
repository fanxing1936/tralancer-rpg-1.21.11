execute if score @s rpg_ex_kind matches 1 run return run function rpg:inquest/counter/lucifer_wait
execute if score @s rpg_ex_kind matches 2 run return run function rpg:inquest/counter/leviathan_wait
execute if score @s rpg_ex_kind matches 7 run return 0
scoreboard players remove @s rpg_ex_counter 1
execute if score @s rpg_ex_counter matches ..0 run function rpg:inquest/counter/cast
