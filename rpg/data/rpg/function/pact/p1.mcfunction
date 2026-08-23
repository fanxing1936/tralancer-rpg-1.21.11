# 借的就是同一位魔神的力，表现与［原罪］一模一样 —— 蛇矛与尖牙都是罪器原件。
particle dust_color_transition{from_color:9882230,to_color:4895350,scale:1} ~ ~1.1 ~ 0.3 0.3 0.3 0.02 20
playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.7 1.7
playsound minecraft:block.sculk_catalyst.bloom player @a[distance=..24] ~ ~ ~ 1 0.6
tag @s add rpg.luci.cast
execute at @s anchored eyes run function rpg:item/extra/lucifer_lance
execute at @s rotated ~ 0 run function rpg:item/extra/lucifer_fangs
tag @s remove rpg.luci.cast
