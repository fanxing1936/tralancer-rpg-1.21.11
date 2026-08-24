# 原罪 —— 蛇矛沿视线破土，尖牙同路。
data modify storage rpg:demon uuid set from entity @s UUID
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle dust{color:[0.0,0.29,0.11],scale:2} ~ ~1 ~ 0.6 0.8 0.6 0.05 40
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk1_line with storage rpg:demon
