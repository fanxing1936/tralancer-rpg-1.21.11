# 二阶段体型。手动挂 rpg.lu.phase2 调试时也会走到这里。
tag @s add rpg.lu2f.big
attribute @s minecraft:scale base set 2.5
effect clear @s minecraft:speed
attribute @s minecraft:movement_speed modifier remove rpg:lu2f_slow
attribute @s minecraft:movement_speed modifier add rpg:lu2f_slow -0.4 add_multiplied_total
# 原版近战归零：伤害全部来自对得上动作的「碾」。
attribute @s minecraft:attack_damage modifier remove rpg:lu2f_melee
attribute @s minecraft:attack_damage modifier add rpg:lu2f_melee -1 add_multiplied_total
attribute @s minecraft:knockback_resistance modifier remove rpg:lu2f_root
attribute @s minecraft:knockback_resistance modifier add rpg:lu2f_root 1 add_value
