# 调试：在自己身前召一个友军雅克（不走冷却）。必须由玩家执行。
execute store result score #now rpg_al run time query gametime
execute unless score @s rpg_al_id matches 1.. run function rpg:jacques_ally/new_id
scoreboard players operation #own rpg_al = @s rpg_al_id
execute rotated ~ 0 positioned ^ ^ ^1.5 run function rpg:jacques_ally/spawn
