# 反转完成。魔化没有被洗掉 —— 它被烧穿了，从另一面出来。
particle minecraft:flash{color:16777215} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~0.8 ~ 1.4 0.8 1.4 0.5 220
particle dust{color:[1.0,0.99,0.92],scale:4} ~ ~1 ~ 1.2 0.8 1.2 0.25 180
particle totem_of_undying ~ ~1 ~ 0.8 0.8 0.8 0.4 120
playsound minecraft:item.totem.use master @a[distance=..48] ~ ~ ~ 1 1
playsound minecraft:block.beacon.power_select master @a[distance=..48] ~ ~ ~ 1 0.8
execute as @a[tag=rpg.inv.subject,distance=..7] run function rpg:rite/inv_grant
kill @s
