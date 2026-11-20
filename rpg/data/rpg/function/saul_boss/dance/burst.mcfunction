# 所有剑痕同时斩开（as 他）
execute as @e[tag=rpg.slb.danceseg] at @s run tag @e[tag=rpg.unit.f,distance=..1.3] add rpg.slb.hit
execute as @e[tag=rpg.slb.danceseg] at @s run function rpg:saul_boss/flash/burst
kill @e[tag=rpg.slb.danceseg]
kill @e[tag=rpg.slb.dancebeam]
particle minecraft:flash{color:13193306} ~ ~1 ~ 0 0 0 0 1 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 1.4
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.4 0.8
