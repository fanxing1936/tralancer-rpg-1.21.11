# 圣卫方阵：视线前方 8 格，三人一排。
execute positioned ^-2.5 ^ ^8 run function rpg:tower_guard/summon
execute positioned ^ ^ ^9 run function rpg:tower_guard/summon
execute positioned ^2.5 ^ ^8 run function rpg:tower_guard/summon
tellraw @s {"text": "[宣传片] 圣卫方阵已列队。", "color": "#E3B04B"}
