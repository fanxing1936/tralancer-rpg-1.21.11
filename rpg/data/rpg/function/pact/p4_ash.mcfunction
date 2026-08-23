# 沿视线三段。`positioned ^ ^ ^N` 取点，整条线不需要递归。
execute positioned ^ ^ ^2 run particle ash ~ ~ ~ 1 1 1 0.05 40
execute positioned ^ ^ ^2 run particle sweep_attack ~ ~ ~ 0.8 0.8 0.8 0 4
execute positioned ^ ^ ^2 run particle lava ~ ~ ~ 0.6 0.6 0.6 0 6
execute positioned ^ ^ ^2 as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run damage @s 7 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
execute positioned ^ ^ ^2 as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run effect give @s minecraft:hunger 8 2 true
execute positioned ^ ^ ^4 run particle ash ~ ~ ~ 1 1 1 0.05 40
execute positioned ^ ^ ^4 run particle sweep_attack ~ ~ ~ 0.8 0.8 0.8 0 4
execute positioned ^ ^ ^4 run particle lava ~ ~ ~ 0.6 0.6 0.6 0 6
execute positioned ^ ^ ^4 as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run damage @s 7 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
execute positioned ^ ^ ^4 as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run effect give @s minecraft:hunger 8 2 true
execute positioned ^ ^ ^6 run particle ash ~ ~ ~ 1 1 1 0.05 40
execute positioned ^ ^ ^6 run particle sweep_attack ~ ~ ~ 0.8 0.8 0.8 0 4
execute positioned ^ ^ ^6 run particle lava ~ ~ ~ 0.6 0.6 0.6 0 6
execute positioned ^ ^ ^6 as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run damage @s 7 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
execute positioned ^ ^ ^6 as @e[distance=..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:item_display] at @s run effect give @s minecraft:hunger 8 2 true
