execute unless score @s rpg_k14 matches 1.. run return run function rpg:force/fail/say {m:"先学会「血刃」"}
execute if score @s rpg_fs_m2 matches 14 run scoreboard players set @s rpg_fs_m2 0
execute if score @s rpg_fs_m3 matches 14 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m1 14
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
