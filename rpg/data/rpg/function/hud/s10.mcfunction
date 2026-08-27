# 旧镶嵌蓄力条；由统一 HUD 渲染，不直接争抢 actionbar。
execute if entity @s[scores={rpg_hud_p=0}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"","italic":false,"color":"red"},{"text":"▱▱▱▱▱▱▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  0%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=0}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=1}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰","italic":false,"color":"red"},{"text":"▱▱▱▱▱▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  10%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=1}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=2}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰","italic":false,"color":"red"},{"text":"▱▱▱▱▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  20%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=2}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=3}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰","italic":false,"color":"red"},{"text":"▱▱▱▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  30%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=3}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=4}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰","italic":false,"color":"red"},{"text":"▱▱▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  40%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=4}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=5}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰▰","italic":false,"color":"red"},{"text":"▱▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  50%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=5}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=6}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰▰▰","italic":false,"color":"red"},{"text":"▱▱▱▱","italic":false,"color":"dark_gray"},{"text":"  60%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=6}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=7}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰▰▰▰","italic":false,"color":"red"},{"text":"▱▱▱","italic":false,"color":"dark_gray"},{"text":"  70%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=7}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=8}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰▰▰▰▰","italic":false,"color":"red"},{"text":"▱▱","italic":false,"color":"dark_gray"},{"text":"  80%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=8}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=9}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰▰▰▰▰▰","italic":false,"color":"red"},{"text":"▱","italic":false,"color":"dark_gray"},{"text":"  90%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=9}] run function rpg:hud/seal/event with storage rpg:hud
execute if entity @s[scores={rpg_hud_p=10}] run data modify storage rpg:hud e set value '["",{"text":"烈　焰 ","italic":false,"color":"dark_red"},{"text":"▰▰▰▰▰▰▰▰▰▰","italic":false,"color":"red"},{"text":"","italic":false,"color":"dark_gray"},{"text":"  100%","italic":false,"color":"gray"}]'
execute if entity @s[scores={rpg_hud_p=10}] run function rpg:hud/seal/event with storage rpg:hud
