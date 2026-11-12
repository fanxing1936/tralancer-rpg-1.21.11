# Public single-carrier entry; no combat/phase-condition changes.
execute unless entity @s[type=minecraft:vindicator,scores={rpg_dm_lord=1},tag=rpg.lu.phase2,tag=rpg.lu2] run return 0
tag @s add rpg.lu2.death_played
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run tag @s add rpg.lu2.death_played
function rpg:lucifer_p2/flower/stop
return run function rpg:lucifer_p2/anim/enter/jungleabomination_death
