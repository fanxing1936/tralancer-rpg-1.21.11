# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/3_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m13
# 深渊之口 —— 地底下那张嘴张开了。
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 1 0.8
particle sonic_boom ~ ~1 ~ 0 0 0 0 3
particle sculk_charge_pop ~ ~0.2 ~ 4 0.3 4 0.2 80
execute as @e[tag=rpg.unit.f,distance=..8] at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^2
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk3c_maw
# 亚巴顿外观（add_abaddon_model.py）
execute if entity @s[tag=rpg.ab] run function rpg:abaddon/skill/sk3_3
