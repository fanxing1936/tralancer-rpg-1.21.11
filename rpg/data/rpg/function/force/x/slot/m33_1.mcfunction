execute unless score @s rpg_k33 matches 1.. run return run function rpg:force/fail/say {m:"还没习得「圣殿誓约」"}
execute unless score @s rpg_force matches 2 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有魔力"}
execute if score @s rpg_fs_m2 matches 33 run scoreboard players set @s rpg_fs_m2 0
execute if score @s rpg_fs_m3 matches 33 run scoreboard players set @s rpg_fs_m3 0
scoreboard players set @s rpg_fs_m1 33
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4
