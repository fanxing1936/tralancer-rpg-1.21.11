execute unless score @s rpg_k25 matches 1.. run return run function rpg:force/fail/say {m:"终式要到王冠阶（第 10 阶）"}
execute unless score @s rpg_force matches 1 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有圣力"}
execute if score @s rpg_fs_h1 matches 25 run scoreboard players set @s rpg_fs_h1 0
execute if score @s rpg_fs_h3 matches 25 run scoreboard players set @s rpg_fs_h3 0
scoreboard players set @s rpg_fs_h2 25
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
