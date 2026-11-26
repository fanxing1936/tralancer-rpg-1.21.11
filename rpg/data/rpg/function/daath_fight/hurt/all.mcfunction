# 打中带 rpg.dt.hit 的挑战者：#pc 由调用者设
execute as @a[tag=rpg.dt.hit] at @s run function rpg:daath_fight/hurt/me
tag @a remove rpg.dt.hit
