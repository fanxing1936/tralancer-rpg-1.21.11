# 解雇。装备掉在地上，人散了，退回一半雇金。
execute if items entity @s weapon.mainhand *[] run function rpg:squad/drop_weapon
execute at @s run particle poof ~ ~1 ~ 0.4 0.6 0.4 0.05 40
execute at @s run playsound minecraft:entity.husk.death hostile @a[distance=..16] ~ ~ ~ 0.7 1.2
execute at @s run loot spawn ~ ~1 ~ loot rpg:squad/refund
execute as @a[tag=rpg.sq.boss,limit=1] run function rpg:hud/m7
kill @s
