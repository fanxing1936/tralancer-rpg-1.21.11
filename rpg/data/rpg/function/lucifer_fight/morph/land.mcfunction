function rpg:lucifer_p2/play/jungleabomination_land
tag @s add rpg.dm.cast
execute as @e[tag=rpg.unit.f,distance=..6] run function rpg:lucifer_fight/morph/shock
tag @s remove rpg.dm.cast
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 3 0.2 3 0.15 90
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~0.5 ~ 3 0.3 3 0.05 50
