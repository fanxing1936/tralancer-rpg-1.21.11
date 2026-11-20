# 落剑（as/at 它）：出生 3 刻后用 10 刻插到地上
execute if score @s rpg_sl_life matches 21 run data merge entity @s {teleport_duration:10}
execute if score @s rpg_sl_life matches 21 run tp @s ~ ~-9.2 ~
execute if score @s rpg_sl_life matches 12..20 run particle minecraft:end_rod ~ ~0.5 ~ 0.05 0.3 0.05 0 1
