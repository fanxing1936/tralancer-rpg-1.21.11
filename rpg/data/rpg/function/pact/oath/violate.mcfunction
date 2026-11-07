# 犯了禁忌。
scoreboard players remove @s rpg_pact_bond 10
scoreboard players add @s rpg_taint 5
playsound minecraft:entity.wither.hurt player @s ~ ~ ~ 0.6 0.6
function rpg:pact/oath/taboo_msg
execute if score @s rpg_pact_bond matches ..0 run function rpg:pact/oath/fall
