# 朝拜：叛天的首谋一开口，方圆七格都得低头。
particle enchant ~ ~1.2 ~ 3 1.5 3 1 150
particle dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 3 1.2 3 0.06 90
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..28] ~ ~ ~ 1 0.6
playsound minecraft:block.beacon.power_select master @a[distance=..28] ~ ~ ~ 0.8 0.5
execute as @e[distance=0.1..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run function rpg:pact/p6_kneel
