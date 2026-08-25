# 终末收割 —— 灵魂被一并割下，每一枚都反哺收割者。
particle sculk_charge_pop ~ ~1 ~ 5 1 5 0.14 72 normal
particle soul ~ ~1 ~ 4 1.5 4 0.08 72 normal
particle sonic_boom ~ ~1 ~ 0 0 0 0 4 normal
particle flash{color:9605787} ~ ~1 ~ 0 0 0 0 1 normal
particle reverse_portal ~ ~1 ~ 4 1.5 4 0.3 72 normal
particle soul_fire_flame ~ ~1 ~ 4 1 4 0.08 72 normal
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..36] ~ ~ ~ 1.1 0.65
playsound minecraft:entity.wither.spawn hostile @a[distance=..40] ~ ~ ~ 0.7 0.55
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult3_hit
