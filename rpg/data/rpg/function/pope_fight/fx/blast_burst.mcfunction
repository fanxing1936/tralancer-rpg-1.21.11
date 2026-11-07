function rpg:pope_fight/fx/impact
particle dust{color:[1.000f,0.949f,0.659f],scale:1.6} ~ ~ ~ 0.3 0.3 0.3 0.1 16 normal
particle flash{color:16773800} ~ ~ ~ 0 0 0 0 1 normal
playsound rpg:pope.magic_impact hostile @a[distance=..24] ~ ~ ~ 0.5 1
kill @s
