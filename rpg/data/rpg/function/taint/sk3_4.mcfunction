# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/3_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m14
# 停摆 —— 不眠之钟的反面，连一刻都不再向前。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.35
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..32] ~ ~ ~ 1 0.42
particle sculk_soul ~ ~1 ~ 4 1 4 0.04 82
particle dust{color:[0.58,0.58,0.61],scale:2.2} ~ ~1 ~ 4 1 4 0.04 64
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3d_still
