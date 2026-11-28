schedule function rpg:town/near 100t
# 每 5 秒：有人走到某座镇名义位置 700 格内，就排队建它
execute if score #s1 rpg_tw matches 0 in minecraft:overworld positioned 556 100 -1712 if entity @a[distance=..700] run scoreboard players set #s1 rpg_tw 1
execute if score #s2 rpg_tw matches 0 in minecraft:overworld positioned 1456 100 -1058 if entity @a[distance=..700] run scoreboard players set #s2 rpg_tw 1
execute if score #s3 rpg_tw matches 0 in minecraft:overworld positioned 1800 100 0 if entity @a[distance=..700] run scoreboard players set #s3 rpg_tw 1
execute if score #s4 rpg_tw matches 0 in minecraft:overworld positioned 1456 100 1058 if entity @a[distance=..700] run scoreboard players set #s4 rpg_tw 1
execute if score #s5 rpg_tw matches 0 in minecraft:overworld positioned 556 100 1712 if entity @a[distance=..700] run scoreboard players set #s5 rpg_tw 1
execute if score #s6 rpg_tw matches 0 in minecraft:overworld positioned -556 100 1712 if entity @a[distance=..700] run scoreboard players set #s6 rpg_tw 1
execute if score #s7 rpg_tw matches 0 in minecraft:overworld positioned -1456 100 1058 if entity @a[distance=..700] run scoreboard players set #s7 rpg_tw 1
execute if score #s8 rpg_tw matches 0 in minecraft:overworld positioned -1800 100 0 if entity @a[distance=..700] run scoreboard players set #s8 rpg_tw 1
execute if score #s9 rpg_tw matches 0 in minecraft:overworld positioned -1456 100 -1058 if entity @a[distance=..700] run scoreboard players set #s9 rpg_tw 1
execute if score #s10 rpg_tw matches 0 in minecraft:overworld positioned -556 100 -1712 if entity @a[distance=..700] run scoreboard players set #s10 rpg_tw 1
execute if score #s11 rpg_tw matches 0 in minecraft:overworld positioned 1051 100 -3234 if entity @a[distance=..700] run scoreboard players set #s11 rpg_tw 1
execute if score #s12 rpg_tw matches 0 in minecraft:overworld positioned 2751 100 -1998 if entity @a[distance=..700] run scoreboard players set #s12 rpg_tw 1
execute if score #s13 rpg_tw matches 0 in minecraft:overworld positioned 3400 100 0 if entity @a[distance=..700] run scoreboard players set #s13 rpg_tw 1
execute if score #s14 rpg_tw matches 0 in minecraft:overworld positioned 2751 100 1998 if entity @a[distance=..700] run scoreboard players set #s14 rpg_tw 1
execute if score #s15 rpg_tw matches 0 in minecraft:overworld positioned 1051 100 3234 if entity @a[distance=..700] run scoreboard players set #s15 rpg_tw 1
execute if score #s16 rpg_tw matches 0 in minecraft:overworld positioned -1051 100 3234 if entity @a[distance=..700] run scoreboard players set #s16 rpg_tw 1
execute if score #s17 rpg_tw matches 0 in minecraft:overworld positioned -2751 100 1998 if entity @a[distance=..700] run scoreboard players set #s17 rpg_tw 1
execute if score #s18 rpg_tw matches 0 in minecraft:overworld positioned -3400 100 0 if entity @a[distance=..700] run scoreboard players set #s18 rpg_tw 1
execute if score #s19 rpg_tw matches 0 in minecraft:overworld positioned -2751 100 -1998 if entity @a[distance=..700] run scoreboard players set #s19 rpg_tw 1
execute if score #s20 rpg_tw matches 0 in minecraft:overworld positioned -1051 100 -3234 if entity @a[distance=..700] run scoreboard players set #s20 rpg_tw 1
execute if score #s21 rpg_tw matches 0 in minecraft:overworld positioned 2103 100 -1528 if entity @a[distance=..700] run scoreboard players set #s21 rpg_tw 1
execute if score #s22 rpg_tw matches 0 in minecraft:overworld positioned -2103 100 1528 if entity @a[distance=..700] run scoreboard players set #s22 rpg_tw 1
execute if score #s23 rpg_tw matches 0 in minecraft:overworld positioned 3479 100 2527 if entity @a[distance=..700] run scoreboard players set #s23 rpg_tw 1
execute if score #s24 rpg_tw matches 0 in minecraft:overworld positioned -2103 100 -1528 if entity @a[distance=..700] run scoreboard players set #s24 rpg_tw 1
