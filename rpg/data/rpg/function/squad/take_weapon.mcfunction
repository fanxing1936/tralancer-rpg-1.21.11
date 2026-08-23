# 把雇主手里那件塞给他，然后清空雇主的手。
execute unless items entity @a[tag=rpg.sq.boss,limit=1] weapon.mainhand *[] run return 0
item replace entity @s weapon.mainhand from entity @a[tag=rpg.sq.boss,limit=1] weapon.mainhand
item replace entity @a[tag=rpg.sq.boss,limit=1] weapon.mainhand with air
particle enchant ~ ~1.4 ~ 0.3 0.4 0.3 0.6 24
playsound minecraft:item.armor.equip_iron player @a[distance=..12] ~ ~ ~ 1 1.1
title @a[tag=rpg.sq.boss,limit=1] actionbar ["",{"text":"已配装","color":"#D4AF37"}]
