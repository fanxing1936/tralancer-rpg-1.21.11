# 掉阶：多出来的槽退回柱印。
execute if score @s rpg_pact_lv matches ..2 if score @s rpg_pact_s2 matches 1.. run function rpg:pact/seal/eject2
execute if score @s rpg_pact_lv matches ..1 if score @s rpg_pact_s1 matches 1.. run function rpg:pact/seal/eject1
