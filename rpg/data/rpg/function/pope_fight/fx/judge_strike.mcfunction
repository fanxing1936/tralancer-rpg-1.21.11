# 光柱落下。判定只看距离。
execute as @a[distance=..2.8,gamemode=!spectator,gamemode=!creative] run damage @s 12 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1]
function rpg:pope_fight/fx/pillar
execute positioned ~ ~1 ~ run function rpg:pope_fight/fx/impact
