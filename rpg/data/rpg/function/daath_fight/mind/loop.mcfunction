tag @s add rpg.dt.loop
execute unless score @s rpg_dt_say > @s rpg_dt_orb run function rpg:daath_fight/mind/loop_say
function rpg:daath_fight/eye/loop
playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 0.8 0.7
