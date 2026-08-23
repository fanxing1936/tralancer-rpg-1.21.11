# 一次挥砍。伤害读的是队员**自己的 attack_damage 属性** ——
# 那个值天然含手持武器（空手 5，拿下界合金剑 12），所以配什么武器就按什么打，
# 不需要任何武器数值表，本包所有自定义武器也一并适用。
#
# damage 的数值不能直接吃记分板，所以走宏：把属性存进 storage 再展开。
scoreboard players set @s rpg_sq_cd 13
tag @s add rpg.sq.striker
execute store result storage rpg:squad atk int 1 run attribute @s minecraft:attack_damage get
function rpg:squad/strike_do with storage rpg:squad
tag @s remove rpg.sq.striker
particle sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..16] ~ ~ ~ 0.7 1.1
playsound minecraft:entity.husk.ambient hostile @a[distance=..16] ~ ~ ~ 0.5 0.8
