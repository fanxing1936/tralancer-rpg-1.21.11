# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/3_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m15
# 死寂 —— 无底坑吞掉声音，也吞掉继续抵抗的力气。
playsound minecraft:entity.warden.roar hostile @a[distance=..32] ~ ~ ~ 0.7 0.45
particle soul ~ ~1 ~ 4 1.4 4 0.06 92
particle reverse_portal ~ ~1 ~ 4 1 4 0.18 78
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3e_silence
