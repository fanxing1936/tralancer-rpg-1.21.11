# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/3_1
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m11
# 收割 —— 周身爆发，每收一个回一颗心。
playsound minecraft:entity.wither.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_charge_pop ~ ~1 ~ 3 1 3 0.1 80
execute as @e[tag=rpg.unit.f,distance=..6] run function rpg:taint/sk3_reap
# 亚巴顿外观（add_abaddon_model.py）
execute if entity @s[tag=rpg.ab] run function rpg:abaddon/skill/sk3_1
