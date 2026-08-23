# @s 是佣兵，rpg.sq.boss 是雇主。他原本拿的掉在地上 —— 那就是取回的方式。
execute if items entity @s weapon.mainhand * run function rpg:squad/drop_weapon
item replace entity @s weapon.mainhand from entity @a[tag=rpg.sq.boss,limit=1] weapon.offhand
item replace entity @a[tag=rpg.sq.boss,limit=1] weapon.offhand with air
particle enchant ~ ~1.4 ~ 0.3 0.4 0.3 0.6 24
playsound minecraft:item.armor.equip_iron player @a[distance=..12] ~ ~ ~ 1 1.1
execute as @a[tag=rpg.sq.boss,limit=1] run function rpg:hud/m9
