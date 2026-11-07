execute as @a[distance=..2.3,gamemode=!spectator,gamemode=!creative] run damage @s 10 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1]
execute positioned ~ ~1.5 ~ run function rpg:pope_fight/fx/impact_void
particle dust{color:[0.835f,0.588f,0.949f],scale:1.6} ~ ~0.3 ~ 0.6 0.2 0.6 0.1 12 normal
playsound rpg:heart_of_ender.mortar_land hostile @a[distance=..32] ~ ~ ~ 0.6 1
