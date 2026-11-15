# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/3_4
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m14
# 停摆 —— 不眠之钟的反面，连一刻都不再向前。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.35
playsound minecraft:entity.warden.heartbeat hostile @a[distance=..32] ~ ~ ~ 1 0.42
particle sculk_soul ~ ~1 ~ 4 1 4 0.04 80
particle dust{color:[0.65,0.69,0.79],scale:2} ~ ~1 ~ 4 1 4 0.04 64
execute as @e[tag=rpg.unit.f,distance=..10] run function rpg:taint/sk3d_still
# 亚巴顿外观（add_abaddon_model.py）
execute if entity @s[tag=rpg.ab] run function rpg:abaddon/skill/sk3_4
