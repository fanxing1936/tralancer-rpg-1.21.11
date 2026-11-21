# 玩家挨打：静水清零、不屈与反震的窗口、符石能量、傲慢的代价、余生。
scoreboard players set @s rpg_fg_calm 0
execute if entity @s[tag=rpg.fg.src.resolve] run scoreboard players set @s rpg_fg_rs 60
execute if entity @s[tag=rpg.fg.a.recoil] on attacker if entity @s[distance=..4] run scoreboard players set #rc rpg_fg 1
execute if score #rc rpg_fg matches 1 run scoreboard players set @s rpg_fg_rw 20
scoreboard players set #rc rpg_fg 0
execute if entity @s[tag=rpg.fg.st] run scoreboard players add @s rpg_fg_en 5
scoreboard players set @s[scores={rpg_fg_en=101..}] rpg_fg_en 100
execute if entity @s[tag=rpg.fg.src.pride] run function rpg:forge/src/pride_cost
execute if entity @s[tag=rpg.fg.a.lastbreath] unless score @s rpg_fg_lb matches 1.. run function rpg:forge/rune/lastbreath
