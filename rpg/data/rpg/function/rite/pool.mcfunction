# 每 20 刻结算一次 —— 逐刻洗魔化太快，也白费开销。
scoreboard players add @s rpg_rite 1
execute if entity @s[scores={rpg_rite=20..}] run function rpg:rite/pool_beat
