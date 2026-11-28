# 失乐园里换圈（as/at 玩家）
scoreboard players set #r rpg_xb 4
execute positioned 0 83 0 if entity @s[distance=..560] run scoreboard players set #r rpg_xb 3
execute positioned 0 83 0 if entity @s[distance=..240] run scoreboard players set #r rpg_xb 2
execute positioned 0 83 0 if entity @s[distance=..160] run scoreboard players set #r rpg_xb 1
execute if score #r rpg_xb = @s rpg_x_pr run return 0
scoreboard players operation @s rpg_x_pr = #r rpg_xb
execute if score #r rpg_xb matches 1 run return run function rpg:explore/pl/1
execute if score #r rpg_xb matches 2 run return run function rpg:explore/pl/2
execute if score #r rpg_xb matches 3 run return run function rpg:explore/pl/3
execute if score #r rpg_xb matches 4 run return run function rpg:explore/pl/4
