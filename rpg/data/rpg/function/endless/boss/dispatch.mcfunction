scoreboard players operation #lord rpg_end_tmp = @s rpg_end_floor
scoreboard players operation #lord rpg_end_tmp /= #five rpg_end_tmp
scoreboard players remove #lord rpg_end_tmp 1
scoreboard players set #seven rpg_end_tmp 7
scoreboard players operation #lord rpg_end_tmp %= #seven rpg_end_tmp
scoreboard players add #lord rpg_end_tmp 1
execute if score #lord rpg_end_tmp matches 1 positioned ^0 ^0 ^16 run function rpg:endless/boss/1
execute if score #lord rpg_end_tmp matches 2 positioned ^0 ^0 ^16 run function rpg:endless/boss/2
execute if score #lord rpg_end_tmp matches 3 positioned ^0 ^0 ^16 run function rpg:endless/boss/3
execute if score #lord rpg_end_tmp matches 4 positioned ^0 ^0 ^16 run function rpg:endless/boss/4
execute if score #lord rpg_end_tmp matches 5 positioned ^0 ^0 ^16 run function rpg:endless/boss/5
execute if score #lord rpg_end_tmp matches 6 positioned ^0 ^0 ^16 run function rpg:endless/boss/6
execute if score #lord rpg_end_tmp matches 7 positioned ^0 ^0 ^16 run function rpg:endless/boss/7
