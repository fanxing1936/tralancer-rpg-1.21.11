# 玩家误伤了友军雅克：把他的生命补回这一刻之前（as 玩家）。
advancement revoke @s only rpg:jacques_ally/friendly
execute as @e[type=minecraft:iron_golem,tag=rpg.jqa,distance=..48] store result entity @s Health float 1 run scoreboard players get @s rpg_al_hp
