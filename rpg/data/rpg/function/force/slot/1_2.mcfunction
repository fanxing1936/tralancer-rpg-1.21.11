execute unless score @s rpg_k01 matches 1.. run return run function rpg:force/fail/say {m:"先学会「圣光矛」"}
execute if score @s rpg_fs_h1 matches 1 run scoreboard players set @s rpg_fs_h1 0
execute if score @s rpg_fs_h3 matches 1 run scoreboard players set @s rpg_fs_h3 0
scoreboard players set @s rpg_fs_h2 1
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
