execute unless score @s rpg_k21 matches 1.. run return run function rpg:force/fail/say {m:"先学会「影步」"}
execute if score @s rpg_fs_m1 matches 21 run scoreboard players set @s rpg_fs_m1 0
execute if score @s rpg_fs_m3 matches 21 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m2 21
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
