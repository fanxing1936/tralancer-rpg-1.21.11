# 建完扫掉被挤出来的掉落物（刚建好，里面不会有玩家的东西）
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 0 run kill @e[type=minecraft:item,distance=..60]
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 -120 run kill @e[type=minecraft:item,distance=..60]
execute in rpg:paradise_lost positioned 0 83 0 positioned 120 82 0 run kill @e[type=minecraft:item,distance=..60]
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 120 run kill @e[type=minecraft:item,distance=..60]
execute in rpg:paradise_lost positioned 0 83 0 positioned -120 82 0 run kill @e[type=minecraft:item,distance=..60]
execute in rpg:paradise_lost positioned 0 83 0 run forceload remove all
execute as @a[tag=rpg.pl.wait] run function rpg:pl/go
