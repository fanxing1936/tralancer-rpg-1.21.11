# 献身 —— 他要的从来不是你的命，是你的血。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust{color:[0.36,0.17,0.44],scale:2} ~ ~1 ~ 3 1 3 0.1 90
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk6c_drain
