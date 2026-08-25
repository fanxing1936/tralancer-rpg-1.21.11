# 空缺者的显形与反扑。两条走查，都带类型。
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=!rpg.ch1.vacant.safe] at @s if entity @a[tag=rpg.holy,distance=..16] run function rpg:vacant/reveal
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt,tag=!rpg.ch1.vacant.safe] at @s run function rpg:vacant/lash
