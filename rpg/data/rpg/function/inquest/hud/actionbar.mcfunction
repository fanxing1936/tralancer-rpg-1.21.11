data modify storage rpg:hud a set value '{"text":""}'
data modify storage rpg:hud b set value '{"text":""}'
data modify storage rpg:hud c set value '{"text":""}'
data modify storage rpg:hud d set value '{"text":""}'
function rpg:inquest/hud/stability
execute if score @s rpg_hud_dmt matches 1.. run return run function rpg:hud/demon/render with storage rpg:hud
function rpg:hud/render with storage rpg:hud
