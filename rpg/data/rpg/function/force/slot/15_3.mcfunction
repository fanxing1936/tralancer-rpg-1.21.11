execute unless score @s rpg_k15 matches 1.. run return run function rpg:force/fail/say {m:"先学会「蚀骨」"}
execute if score @s rpg_fs_m1 matches 15 run scoreboard players set @s rpg_fs_m1 0
execute if score @s rpg_fs_m2 matches 15 run scoreboard players set @s rpg_fs_m2 0
scoreboard players set @s rpg_fs_m3 15
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
