# 契约界面的按钮。trigger 用过一次就关，下次打开界面时才重新开。
execute if score @s rpg_pact_do matches 11..17 run function rpg:pact/do_sign
execute if score @s rpg_pact_do matches 2 if entity @s[tag=rpg.pact] run function rpg:pact/up
execute if score @s rpg_pact_do matches 3 if entity @s[tag=rpg.pact] run function rpg:pact/seal/eject1
execute if score @s rpg_pact_do matches 4 if entity @s[tag=rpg.pact] run function rpg:pact/seal/eject2
execute if score @s rpg_pact_do matches 5 if score @s rpg_pact matches 7 run function rpg:pact/oath/gold
scoreboard players set @s rpg_pact_do 0
