# 毒雾 —— 剧毒与凋零并存。
playsound minecraft:entity.witch.throw hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.24,0.0,0.12],scale:3} ~ ~1 ~ 3 1.2 3 0.06 100
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5_hit
