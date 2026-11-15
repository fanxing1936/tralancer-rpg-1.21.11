# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/2_2
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m7
# 溺没 —— 深海的规矩：在这儿，你不会呼吸。
playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle bubble ~ ~1 ~ 3 1.2 3 0.2 80
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk2b_drown
# 利维坦外观（add_leviathan_model.py）
execute if entity @s[tag=rpg.lv] run function rpg:leviathan/skill/sk2_2
