# 余烬：灰扑出去，三段刀罡跟着切进去。
particle campfire_cosy_smoke ~ ~1 ~ 0.4 0.4 0.4 0.02 30
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.8
playsound minecraft:entity.blaze.shoot hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute at @s anchored eyes run function rpg:pact/p4_ash
