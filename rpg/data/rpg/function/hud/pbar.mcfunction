# 契约冷却条。契约对象由 add_pact 从七柱同一份数据生成；
# 这里只负责第三槽的七柱回响；第四槽由上位契约生成器接管。
scoreboard players set @s rpg_hud_on 1
scoreboard players operation @s rpg_hud_p = #pact_full rpg_hud
scoreboard players operation @s rpg_hud_p -= @s rpg_pact_cd
scoreboard players operation @s rpg_hud_p *= #hud_mini rpg_hud
scoreboard players operation @s rpg_hud_p /= #pact_full rpg_hud
execute if entity @s[scores={rpg_hud_p=0}] run data modify storage rpg:hud c set value '["",{"text":"　","italic":false,"color":"dark_gray"},{"text":"▱▱▱▱▱","italic":false,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_p=1}] run data modify storage rpg:hud c set value '["",{"text":"　","italic":false,"color":"dark_gray"},{"text":"▰","italic":false,"color":"#D4AF37"},{"text":"▱▱▱▱","italic":false,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_p=2}] run data modify storage rpg:hud c set value '["",{"text":"　","italic":false,"color":"dark_gray"},{"text":"▰▰","italic":false,"color":"#D4AF37"},{"text":"▱▱▱","italic":false,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_p=3}] run data modify storage rpg:hud c set value '["",{"text":"　","italic":false,"color":"dark_gray"},{"text":"▰▰▰","italic":false,"color":"#D4AF37"},{"text":"▱▱","italic":false,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_p=4}] run data modify storage rpg:hud c set value '["",{"text":"　","italic":false,"color":"dark_gray"},{"text":"▰▰▰▰","italic":false,"color":"#D4AF37"},{"text":"▱","italic":false,"color":"dark_gray"}]'
execute if entity @s[scores={rpg_hud_p=5}] run data modify storage rpg:hud c set value '["",{"text":"　","italic":false,"color":"dark_gray"},{"text":"▰▰▰▰▰","italic":false,"color":"#D4AF37"}]'
