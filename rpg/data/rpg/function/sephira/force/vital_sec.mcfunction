# 生命力（as/at 圣力者）：每分钟 +1；睡一觉 +40；灵魂营火旁休息每秒 +1
scoreboard players add @s rpg_fz_r 1
execute if score @s rpg_fz_r matches 60.. run scoreboard players add @s rpg_vital 1
execute if score @s rpg_fz_r matches 60.. run scoreboard players set @s rpg_fz_r 0
execute if score @s rpg_fz_sl matches 1.. run scoreboard players add @s rpg_vital 40
scoreboard players set @s rpg_fz_sl 0
execute if score @s rpg_vital matches ..99 run function rpg:sephira/force/campfire
execute if score @s rpg_vital matches 101.. run scoreboard players set @s rpg_vital 100
execute if score @s rpg_vital matches ..-1 run scoreboard players set @s rpg_vital 0
# 燃尽：归零时圣力和圣器保护失效，回到 30 才解除
execute if score @s rpg_vital matches 0 unless entity @s[tag=rpg.burnt] run function rpg:sephira/force/burn
execute if score @s rpg_vital matches 30.. if entity @s[tag=rpg.burnt] run function rpg:sephira/force/unburn
# 生命力越低，最大生命扣得越多（只在档位变了时重挂）
scoreboard players set #b rpg_sef 0
execute if score @s rpg_vital matches 41..70 run scoreboard players set #b rpg_sef 1
execute if score @s rpg_vital matches 11..40 run scoreboard players set #b rpg_sef 2
execute if score @s rpg_vital matches ..10 run scoreboard players set #b rpg_sef 3
execute unless score @s rpg_fz_b = #b rpg_sef run function rpg:sephira/force/band
execute if score #b rpg_sef matches 2.. if predicate rpg:sephira/sprinting run effect give @s minecraft:hunger 2 0 true
