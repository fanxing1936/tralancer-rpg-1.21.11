# 打断正在进行的招式：只收预警标记，已破土的藤蔓、飞出的果核按寿命自然消失。
scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
execute as @e[type=minecraft:marker,tag=rpg.lu2f.mark] if score @s rpg_l2_id = #id rpg_l2_id run kill @s
function rpg:lucifer_fight/free
