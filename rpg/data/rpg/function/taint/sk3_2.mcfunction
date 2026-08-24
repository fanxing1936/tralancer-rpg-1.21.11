# 沉眠 —— 怠惰不杀你，它只让你抬不起手。
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_soul ~ ~1 ~ 3 1 3 0.05 70
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3b_sleep
