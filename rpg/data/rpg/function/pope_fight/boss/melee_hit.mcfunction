# 杖击：普攻。
execute positioned ^ ^1.4 ^1.8 run function rpg:pope_fight/fx/slash
execute at @a[distance=..4.0,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] positioned ~ ~1 ~ run function rpg:pope_fight/fx/impact
damage @a[distance=..4.0,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] 8 minecraft:indirect_magic by @s
particle dust{color:[1.000f,0.949f,0.659f],scale:1.6} ~ ~1 ~ 0.8 0.5 0.8 0.1 24 normal
