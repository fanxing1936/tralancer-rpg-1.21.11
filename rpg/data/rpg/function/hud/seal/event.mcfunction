execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud a set from storage rpg:hud e
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud b set value '{"text":""}'
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud c set value '{"text":""}'
execute if entity @s[scores={rpg_hud_dmt=1..}] run data modify storage rpg:hud d set value '{"text":""}'
execute if entity @s[scores={rpg_hud_dmt=1..}] run return run function rpg:hud/demon/render with storage rpg:hud
$execute if entity @s[tag=rpg.seal.carrier] run return run title @s actionbar ["",$(top),$(back),$(r),$(e)]
$title @s actionbar $(e)
