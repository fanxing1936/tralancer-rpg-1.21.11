# 燃尽。图腾炸开 —— 最后一下把余威全部吐出来。
particle explosion ~ ~0.6 ~ 0.6 0.3 0.6 0 6
particle end_rod ~ ~0.6 ~ 1.2 0.6 1.2 0.3 80
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:2} ~ ~0.8 ~ 1 0.6 1 0.2 72
particle minecraft:flash{color:16773800} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.generic.explode player @a[distance=..28] ~ ~ ~ 1 1.4
playsound minecraft:block.beacon.deactivate player @a[distance=..28] ~ ~ ~ 1 1.1

# 最后一击：范围内的空缺者一并驱出，敌意生物被震开
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..6] at @s run function rpg:rite/free
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,type=!minecraft:villager] at @s run damage @s 6 minecraft:magic
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display,type=!minecraft:villager] at @s run data merge entity @s {Motion:[0d,0.6d,0d]}
execute as @a[distance=..10] run function rpg:hud/m32
kill @s
