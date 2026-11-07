# 戒律的结算，由 taint/step 每 40 刻调用一次。
execute unless score @s rpg_pact_lv matches 1.. run function rpg:pact/oath/migrate
execute if score @s rpg_ps_dead matches 1.. if score @s rpg_ps_hp matches 1.. run function rpg:pact/oath/respawn
scoreboard players add @s rpg_pv_t 1
execute if score @s rpg_pv_t matches 30.. run scoreboard players set @s rpg_pv_t 0
execute if score @s rpg_pv_a matches 1.. run scoreboard players remove @s rpg_pv_a 1
execute if entity @s[tag=rpg.pact.s3] if score @s rpg_pv_t matches 0 run effect give @s minecraft:regeneration 4 0 true
execute if entity @s[tag=rpg.pact.s3] if score @s rpg_pv_t matches 15 run effect give @s minecraft:regeneration 4 0 true
execute if score @s rpg_pact matches 2 run function rpg:pact/oath/p2
execute if score @s rpg_pact matches 3 run function rpg:pact/oath/p3
execute if score @s rpg_pact matches 4 run function rpg:pact/oath/p4
execute if score @s rpg_pact matches 5 run function rpg:pact/oath/p5
execute if score @s rpg_pact matches 6 run function rpg:pact/oath/p6
execute if score @s rpg_pact matches 7 run function rpg:pact/oath/p7
