# 贪婪不用弯腰 —— 6 格内的掉落物自己飘过来。
# 只有签了第七柱的人才会进到这里，其余柱位连一次走查都不欠。
tag @s add rpg.mam.pull
execute as @e[type=minecraft:item,distance=0.6..6,nbt={PickupDelay:0s}] at @s facing entity @a[tag=rpg.mam.pull,limit=1] feet run tp @s ^ ^ ^0.45
tag @s remove rpg.mam.pull
