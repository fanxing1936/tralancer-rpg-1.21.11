
particle minecraft:sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 0 6 normal
particle large_smoke ~0.5 ~1.2 ~0.5 -1 -1 -1 0.2 6 normal
execute anchored feet run tp @s ^ ^ ^1
execute anchored feet run damage @e[limit=1,sort=nearest,distance=0.1..3,tag=ashes] 20 minecraft:outside_border
scoreboard players add @s rpg_boss_fx 1
execute if score @s rpg_boss_fx matches 20.. run kill @s
execute unless entity @e[type=minecraft:vindicator,distance=..50,tag=devil2] run kill @s
