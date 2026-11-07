execute as @a[distance=..1.4,gamemode=!spectator,gamemode=!creative] run damage @s 12 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1]
scoreboard players add #d rpg_pf 1
execute if score #d rpg_pf matches ..11 positioned ^ ^ ^2 run function rpg:pope_fight/fx/beam_step
