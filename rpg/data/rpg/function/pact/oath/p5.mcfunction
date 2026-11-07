# 萨麦尔：每 30 点伤害换 1 点契合；五分钟不动手就犯禁。
execute if score @s rpg_ps_dmg matches 300.. run function rpg:pact/oath/rage
execute if score @s rpg_ps_dmg > @s rpg_pv_a run scoreboard players set @s rpg_pv_b 0
scoreboard players operation @s rpg_pv_a = @s rpg_ps_dmg
scoreboard players add @s rpg_pv_a 1
scoreboard players add @s rpg_pv_b 1
execute if score @s rpg_pv_b matches 150.. run function rpg:pact/oath/taboo_reset
