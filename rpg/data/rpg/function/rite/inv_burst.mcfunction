# 反转完成。魔化没有被洗掉 —— 它被烧穿了，从另一面出来。
particle minecraft:flash{color:16777215} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~0.8 ~ 1.4 0.8 1.4 0.35 96
particle dust_color_transition{from_color:[1.0,1.0,1.0],to_color:[1.0,0.95,0.66],scale:3} ~ ~1 ~ 1.2 0.8 1.2 0.25 80
particle totem_of_undying ~ ~1 ~ 0.8 0.8 0.8 0.35 64
playsound minecraft:item.totem.use master @a[distance=..48] ~ ~ ~ 1 1
playsound minecraft:block.beacon.power_select master @a[distance=..48] ~ ~ ~ 1 0.8
execute as @a[tag=rpg.inv.subject,distance=..7] if score @s rpg_inv_id = #inv_id rpg_inv_id run function rpg:rite/inv_grant
kill @s
