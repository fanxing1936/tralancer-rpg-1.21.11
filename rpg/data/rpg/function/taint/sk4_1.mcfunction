# 余烬 —— 前方喷灰，吸进去的人饿得站不住。
playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk4_cone
