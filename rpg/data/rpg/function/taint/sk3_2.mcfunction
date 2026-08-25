# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/3_2
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m12
# 沉眠 —— 怠惰不杀你，它只让你抬不起手。
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_soul ~ ~1 ~ 3 1 3 0.05 70
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3b_sleep
