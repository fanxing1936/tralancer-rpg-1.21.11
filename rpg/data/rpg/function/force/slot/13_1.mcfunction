execute unless score @s rpg_k13 matches 1.. run return run function rpg:force/fail/say {m:"先学会「暗焰」"}
execute if score @s rpg_fs_m2 matches 13 run scoreboard players set @s rpg_fs_m2 0
execute if score @s rpg_fs_m3 matches 13 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m1 13
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
