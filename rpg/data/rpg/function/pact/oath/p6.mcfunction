# 贝利尔：每献 10 点血换 2 点契合；五分钟满血就犯禁。
execute if score @s rpg_ps_taken matches 100.. run function rpg:pact/oath/blood
execute store result score #max rpg_pact run attribute @s minecraft:max_health get
execute if score @s rpg_ps_hp < #max rpg_pact run return run scoreboard players set @s rpg_pv_b 0
scoreboard players add @s rpg_pv_b 1
execute if score @s rpg_pv_b matches 150.. run function rpg:pact/oath/taboo_reset
