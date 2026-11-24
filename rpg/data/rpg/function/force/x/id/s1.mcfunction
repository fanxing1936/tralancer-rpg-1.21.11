# 无知者：阅历 +20%（美丽阶起 +40%）
execute unless score @s rpg_fo_xl matches 0.. run scoreboard players operation @s rpg_fo_xl = @s rpg_ex_xp
scoreboard players operation #d rpg_fo = @s rpg_ex_xp
scoreboard players operation #d rpg_fo -= @s rpg_fo_xl
execute if score #d rpg_fo matches 1.. run function rpg:force/x/id/xp
scoreboard players operation @s rpg_fo_xl = @s rpg_ex_xp
execute if entity @e[tag=rpg.demon,distance=..32,limit=1] run return run function rpg:force/x/id/cut
execute if entity @e[tag=rpg.demon.minion,distance=..32,limit=1] run function rpg:force/x/id/cut
