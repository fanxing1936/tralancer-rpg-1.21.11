# 到档的奖励（每档一次）
execute if score #rep rpg_tl matches 70.. unless entity @s[tag=rpg.tl.bp] run function rpg:town/life/rep_bp
execute if score #rep rpg_tl matches 100.. unless entity @s[tag=rpg.tl.guardian] run function rpg:town/life/rep_guard
