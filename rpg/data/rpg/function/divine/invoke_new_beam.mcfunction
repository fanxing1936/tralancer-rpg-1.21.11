scoreboard players set @s rpg_lt_div_cd 400
scoreboard players set @s rpg_lt_div_max 400
tag @s add rpg.divine.cast
tag @e[tag=rpg.divine.hit] remove rpg.divine.hit
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^1 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^1 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^1 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^1 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^2 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^2 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^2 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^2 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^2 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^3 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^3 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^3 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^3 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^4 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^4 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^4 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^4 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^4 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^5 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^5 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^5 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^5 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^6 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^6 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^6 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^6 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^6 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^7 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^7 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^7 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^7 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^8 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^8 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^8 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^8 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^8 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^9 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^9 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^9 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^9 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^10 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^10 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^10 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^10 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^10 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^11 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^11 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^11 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^11 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^12 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^12 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^12 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^12 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^12 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^13 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^13 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^13 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^13 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^14 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^14 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^14 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^14 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^14 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^15 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^15 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^15 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^15 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^16 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^16 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^16 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^16 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^16 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^17 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^17 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^17 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^17 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^18 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^18 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^18 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^18 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^18 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^19 0.10 0.10 0.10 0.01 4 force
execute positioned ^ ^1 ^19 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^19 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^19 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
particle dust{color:[0.78,0.92,1.0],scale:1.25} ^ ^1 ^20 0.10 0.10 0.10 0.01 4 force
particle end_rod ^ ^1 ^20 0.14 0.14 0.14 0.01 2 force
execute positioned ^ ^1 ^20 as @e[tag=rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^20 as @e[tag=rpg.demon.minion,tag=!rpg.demon,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
execute positioned ^ ^1 ^20 as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,tag=!rpg.divine.hit,distance=..2.5] at @s run function rpg:divine/damage/new_target
tag @e[tag=rpg.divine.hit] remove rpg.divine.hit
tag @s remove rpg.divine.cast
particle minecraft:flash{color:8641023} ^ ^1 ^1 0 0 0 0 1 force
playsound minecraft:block.beacon.activate master @a[distance=..32] ~ ~ ~ 1 1.65
function rpg:hud/m60
