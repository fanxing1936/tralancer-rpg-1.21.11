advancement revoke @s only rpg:item/power
execute at @s[tag=rpg.e.offhand_power_tag1] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20


execute at @s[tag=rpg.h.power_tag1] run scoreboard players add @s power_step 1
execute at @s[tag=rpg.h.power_tag1] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20

