# 显形（as/at 他）
tag @s add rpg.mkb.solid
function rpg:michael/look/solid
attribute @s minecraft:knockback_resistance base set 0
particle minecraft:flash{color:16765117} ~ ~1.2 ~ 0 0 0 0 1 force
particle minecraft:dust{color:[1.0,0.96,0.93],scale:0.9} ~ ~1.2 ~ 0.5 0.8 0.5 0 16
playsound minecraft:block.beacon.deactivate hostile @a[distance=..32] ~ ~ ~ 1 1.4
