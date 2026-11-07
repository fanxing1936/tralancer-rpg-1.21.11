# 只打贴地的人：跳起来就能躲过去。as 玩家，at 环心。
execute positioned ~-48 ~ ~-48 if entity @s[dx=96,dy=0,dz=96] run damage @s 10 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1]
