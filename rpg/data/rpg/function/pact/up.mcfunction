# 深契。条件不足时只提示，不扣东西。
execute if score @s rpg_pact_lv matches 3.. run return run function rpg:pact/say/up_max
execute if entity @s[gamemode=creative] run return run function rpg:pact/up_done
execute unless score @s rpg_pact_bond matches 100.. run return run function rpg:pact/say/up_bond
execute if score @s rpg_pact_lv matches 1 run return run function rpg:pact/up_soul
function rpg:pact/up_name
