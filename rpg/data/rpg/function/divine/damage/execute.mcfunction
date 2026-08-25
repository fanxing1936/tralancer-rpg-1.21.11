particle minecraft:flash{color:16777215} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:soul_fire_flame ~ ~1 ~ 0.5 0.8 0.5 0.05 36 force
playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..20] ~ ~ ~ 0.8 1.6
execute if entity @a[tag=rpg.divine.cast,limit=1] run damage @s 100000 rpg:divine_light by @a[tag=rpg.divine.cast,limit=1,sort=nearest]
execute unless entity @a[tag=rpg.divine.cast,limit=1] run damage @s 100000 rpg:divine_light
