tag @s add rpg.dm.cast
execute positioned ^ ^1.2 ^ run function rpg:taint/sk1b_thrust
tag @s remove rpg.dm.cast
playsound minecraft:entity.breeze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6
execute positioned ^ ^1.3 ^5 run function rpg:lucifer_fight/p1/spear/beam
