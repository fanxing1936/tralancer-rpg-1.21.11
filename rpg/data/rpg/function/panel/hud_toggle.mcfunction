tag @s remove rpg.panel.was_off
execute if entity @s[tag=rpg.panel.hud_off] run tag @s add rpg.panel.was_off
execute if entity @s[tag=rpg.panel.was_off] run tag @s remove rpg.panel.hud_off
execute unless entity @s[tag=rpg.panel.was_off] run tag @s add rpg.panel.hud_off
execute if entity @s[tag=rpg.panel.hud_off] run title @s actionbar {"text":"","italic":false}
tag @s remove rpg.panel.was_off
function rpg:panel/open
