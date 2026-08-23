# 贝利尔［朝拜］—— 七格之内，全都得低头。
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2} ~ ~1 ~ 3 1.2 3 0.06 90
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk6_kneel
