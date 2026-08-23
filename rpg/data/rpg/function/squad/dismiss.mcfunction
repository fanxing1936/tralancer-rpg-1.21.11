# 解雇。装备掉在地上，人散了，退回一半雇金。
execute if items entity @s weapon.mainhand *[] run function rpg:squad/drop_weapon
execute at @s run particle poof ~ ~1 ~ 0.4 0.6 0.4 0.05 40
execute at @s run playsound minecraft:entity.husk.death hostile @a[distance=..16] ~ ~ ~ 0.7 1.2
execute at @s if entity @s[scores={rpg_sq_tier=1}] run loot spawn ~ ~1 ~ loot rpg:squad/refund1
execute at @s if entity @s[scores={rpg_sq_tier=2}] run loot spawn ~ ~1 ~ loot rpg:squad/refund2
execute at @s if entity @s[scores={rpg_sq_tier=3}] run loot spawn ~ ~1 ~ loot rpg:squad/refund3
execute at @s if entity @s[scores={rpg_sq_tier=4}] run loot spawn ~ ~1 ~ loot rpg:squad/refund4
execute at @s if entity @s[scores={rpg_sq_tier=5}] run loot spawn ~ ~1 ~ loot rpg:squad/refund5
execute as @a[tag=rpg.sq.boss,limit=1] run function rpg:hud/m16
kill @s
