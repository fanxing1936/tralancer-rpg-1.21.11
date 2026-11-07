# 亚巴顿：潜行且这两秒没挪窝，累计 10 秒换 1 点契合。
execute if predicate rpg:sneaking if score @s rpg_ps_crouch matches 0 run scoreboard players add @s rpg_pv_b 1
scoreboard players set @s rpg_ps_crouch 0
execute if score @s rpg_pv_b matches 5.. run function rpg:pact/oath/still
execute if score @s rpg_pv_t matches 0 if score @s rpg_ps_sprint matches 30000.. run function rpg:pact/oath/violate
execute if score @s rpg_pv_t matches 0 run scoreboard players set @s rpg_ps_sprint 0
