# 待雇 -> 在编。
tag @s remove rpg.sq.free
tag @s add rpg.squad
scoreboard players operation @s rpg_squad = #sq rpg_squad
scoreboard players set @s rpg_sq_mode 0
scoreboard players set @s rpg_sq_cd 0
# 队里的编号。站位按它分开 —— 不然四个人会停在同一个点上。
scoreboard players operation @s rpg_sq_slot = #cnt rpg_squad
execute if entity @s[scores={rpg_sq_tier=1}] run data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"HAIKU","color":"gray","bold":true}]
execute if entity @s[scores={rpg_sq_tier=2}] run data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"SONNET","color":"#57C6D6","bold":true}]
execute if entity @s[scores={rpg_sq_tier=3}] run data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"OPUS","color":"#A275DE","bold":true}]
execute if entity @s[scores={rpg_sq_tier=4}] run data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"FABLE","color":"#D9A02B","bold":true}]
execute if entity @s[scores={rpg_sq_tier=5}] run data modify entity @s CustomName set value [{"text":"佣兵 · ","color":"gray"},{"text":"MYTHOS","color":"#FFD700","bold":true}]
function rpg:squad/board
particle happy_villager ~ ~1.6 ~ 0.3 0.3 0.3 0.1 30
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.03 16
