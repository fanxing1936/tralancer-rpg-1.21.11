# Orphan-anchor fallback; explicit death clip has already voiced it.
execute unless entity @s[tag=rpg.lu2.death_played] run playsound rpg:lucifer_p2.death_voice hostile @a[distance=..48] ~ ~ ~ 1.35 1
execute unless entity @s[tag=rpg.lu2.death_played] run playsound rpg:lucifer_p2.death_foley hostile @a[distance=..48] ~ ~ ~ 1 1
