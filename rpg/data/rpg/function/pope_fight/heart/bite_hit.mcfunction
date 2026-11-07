# 咬：身前一块。
execute positioned ^ ^ ^4 as @a[distance=..4.5,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1]
execute positioned ^ ^2 ^4 run function rpg:pope_fight/fx/impact_void
particle dust{color:[0.835f,0.588f,0.949f],scale:1.6} ^ ^1 ^4 1 0.5 1 0.1 16 normal
playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..32] ~ ~ ~ 1 0.6
