# Only this carrier's phase-two displays; no death sound on switch.
execute unless entity @s[tag=rpg.lu2] run return 0
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run kill @s
tag @s remove rpg.lu2
tag @s remove rpg.lu2.glow
tag @s remove rpg.lu2.death_played
tag @s remove rpg.lu2.flower
scoreboard players reset @s rpg_lu2_anim
scoreboard players reset @s rpg_lu2_t
scoreboard players reset @s rpg_lu2_mv
scoreboard players reset @s rpg_lu2_mc
scoreboard players reset @s rpg_lu2_x
scoreboard players reset @s rpg_lu2_z
scoreboard players reset @s rpg_lu2_flower
execute if score @s rpg_dm_lord matches 1 unless entity @s[tag=rpg.lu] run function #rpg:lucifer_p2/phase1_return
