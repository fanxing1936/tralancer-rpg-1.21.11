# 收割 —— 周身爆发，每收一个回一颗心。
playsound minecraft:entity.wither.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_charge_pop ~ ~1 ~ 3 1 3 0.1 90
execute as @a[distance=..6,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3_reap
