# 每秒（as/at 玩家）
scoreboard players enable @s rpg_fo_do
execute unless score @s rpg_ob matches 100 run return 0
execute if score @s rpg_force matches 1 unless entity @s[tag=rpg.fo.g1] run function rpg:force/give/first_1
execute if score @s rpg_force matches 3 unless entity @s[tag=rpg.fo.g1] run function rpg:force/give/first_1
execute if score @s rpg_force matches 2..3 unless entity @s[tag=rpg.fo.g2] run function rpg:force/give/first_2
# 神职者：祝福生来 1 级（不花点，洗点后也还在）
execute if score @s rpg_ident matches 3 if score @s rpg_force matches 1 unless score @s rpg_k05 matches 1.. run scoreboard players set @s rpg_k05 1
function rpg:force/x/id/sec
