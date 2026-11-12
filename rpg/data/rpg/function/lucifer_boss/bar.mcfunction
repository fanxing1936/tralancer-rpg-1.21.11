execute if score @s rpg_lub matches 1 run scoreboard players operation #v rpg_lub = @s rpg_lub_h
execute if score @s rpg_lub matches 2 run scoreboard players operation #v rpg_lub = @s rpg_lub_h
execute if score #v rpg_lub matches ..-1 run scoreboard players set #v rpg_lub 0
execute store result bossbar rpg:lucifer_boss value run scoreboard players get #v rpg_lub
# 横幅每 50 血一档，跨档才换图。
scoreboard players operation #s rpg_lub = #v rpg_lub
scoreboard players add #s rpg_lub 49
scoreboard players set #k rpg_lub 50
scoreboard players operation #s rpg_lub /= #k rpg_lub
execute if score #s rpg_lub matches 21.. run scoreboard players set #s rpg_lub 20
execute unless score #s rpg_lub = @s rpg_lub_s run function rpg:lucifer_boss/bar_name
