# 妒海沉城 —— 深潮将十二格内的一切拖向海眼。
particle bubble_column_up ~ ~0.5 ~ 5 1 5 0.55 72 normal
particle dust_color_transition{from_color:[0.24,0.66,0.91],to_color:[0.02,0.09,0.18],scale:3} ~ ~1 ~ 5 1 5 0.05 72 normal
particle flash{color:4041192} ~ ~1 ~ 0 0 0 0 1 normal
particle nautilus ~ ~1 ~ 5 1.5 5 0.14 72 normal
particle splash ~ ~0.7 ~ 5 1 5 0.25 72 normal
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..36] ~ ~ ~ 1.25 0.45
playsound minecraft:entity.generic.splash hostile @a[distance=..36] ~ ~ ~ 1.4 0.55
execute as @a[distance=..12,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult2_hit
