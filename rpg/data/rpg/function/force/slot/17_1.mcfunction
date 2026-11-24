execute unless score @s rpg_k17 matches 1.. run return run function rpg:force/fail/say {m:"先学会「血肉护壳」"}
execute if score @s rpg_fs_m2 matches 17 run scoreboard players set @s rpg_fs_m2 0
execute if score @s rpg_fs_m3 matches 17 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m1 17
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
