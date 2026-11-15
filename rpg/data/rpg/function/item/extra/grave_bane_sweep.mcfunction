# 第三下：前方横扫。施放者带 rpg.gb.cast，伤害记在他名下。
tag @s add rpg.gb.cast
playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.7
playsound minecraft:block.bell.use player @a[distance=..16] ~ ~ ~ 0.5 1.7
execute anchored eyes positioned ^ ^-0.5 ^ run particle minecraft:sweep_attack ^-1 ^ ^1.6 0 0 0 0 1
execute anchored eyes positioned ^ ^-0.5 ^ run particle minecraft:sweep_attack ^ ^ ^2 0 0 0 0 1
execute anchored eyes positioned ^ ^-0.5 ^ run particle minecraft:sweep_attack ^1 ^ ^1.6 0 0 0 0 1
execute anchored eyes positioned ^ ^-0.5 ^ run particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[0.83,0.69,0.22],scale:1.2} ^ ^ ^1.8 1.2 0.15 1.2 0 14
execute positioned ^ ^ ^1.8 as @e[distance=..2.8,type=!player,type=!#rpg:no_damage_track,tag=!rpg.ally] at @s run function rpg:item/extra/grave_bane_sweep_hit
tag @s remove rpg.gb.cast
