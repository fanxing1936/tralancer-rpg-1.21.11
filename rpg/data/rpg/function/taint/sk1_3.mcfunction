# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m3
# 高踞 —— 傲慢把人举起来，再让他自己摔下去。
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle end_rod ~ ~1 ~ 3 1 3 0.1 60
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk1c_lift
# Lucifer mesh appearance (add_lucifer_model.py)
execute if entity @s[tag=rpg.lu,tag=!rpg.lu.phase2] run function rpg:lucifer_lord/skill/sk1_3
