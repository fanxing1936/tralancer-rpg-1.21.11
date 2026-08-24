# 蛇矛 —— 一记贯穿，连着把人钉退。
playsound minecraft:entity.breeze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk1b_thrust
