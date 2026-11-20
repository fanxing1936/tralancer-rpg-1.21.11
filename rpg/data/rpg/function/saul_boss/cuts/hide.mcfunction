# 化作剑风（as 他）：藏到地下，部件跟着；无敌
data merge entity @s {Invulnerable:1b,NoGravity:1b}
tag @s add rpg.slb.hidden
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.6 1 0.6 0 30 force
particle minecraft:sweep_attack ~ ~1 ~ 0.8 0.6 0.8 0 6 force
playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..40] ~ ~ ~ 1 1.4
tp @s ~ ~-40 ~
