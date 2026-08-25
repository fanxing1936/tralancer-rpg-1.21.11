tag @s remove rpg.panel.was_off
execute if entity @s[tag=rpg.panel.hud_off] run tag @s add rpg.panel.was_off
execute if entity @s[tag=rpg.panel.was_off] run tag @s remove rpg.panel.hud_off
execute unless entity @s[tag=rpg.panel.was_off] run tag @s add rpg.panel.hud_off
execute if entity @s[tag=rpg.panel.hud_off] run title @s actionbar {"text":"","italic":false}
execute if entity @s[tag=rpg.panel.hud_off] run tellraw @s ["",{"text":"[玩家面板] HUD 已隐藏","color":"#8FC7FF","italic":false,"bold":true}]
execute unless entity @s[tag=rpg.panel.hud_off] run tellraw @s ["",{"text":"[玩家面板] HUD 已恢复","color":"#70DB70","italic":false,"bold":true}]
tag @s remove rpg.panel.was_off
tellraw @s ["",{"text":"[返回面板]","color":"#D4AF37","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 8"}}]
