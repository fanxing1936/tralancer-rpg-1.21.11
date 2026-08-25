# 当前契约对象。身份是持续状态，即使力量已经冷却也一直显示。
scoreboard players set @s rpg_hud_on 1
execute if entity @s[scores={rpg_pact=1}] run function rpg:hud/pact1
execute if entity @s[scores={rpg_pact=2}] run function rpg:hud/pact2
execute if entity @s[scores={rpg_pact=3}] run function rpg:hud/pact3
execute if entity @s[scores={rpg_pact=4}] run function rpg:hud/pact4
execute if entity @s[scores={rpg_pact=5}] run function rpg:hud/pact5
execute if entity @s[scores={rpg_pact=6}] run function rpg:hud/pact6
execute if entity @s[scores={rpg_pact=7}] run function rpg:hud/pact7
