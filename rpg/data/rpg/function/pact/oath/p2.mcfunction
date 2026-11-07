# 利维坦：碰水就不算断。
execute if predicate rpg:pact_wet run return run scoreboard players set @s rpg_pv_b 0
scoreboard players add @s rpg_pv_b 1
execute if score @s rpg_pv_b matches 300.. run function rpg:pact/oath/taboo_reset
