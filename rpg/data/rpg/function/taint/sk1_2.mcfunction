# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/1_2
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m2
# 蛇矛 —— 一记贯穿，连着把人钉退。
playsound minecraft:entity.breeze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6
execute at @s anchored eyes facing entity @e[tag=rpg.unit.f,limit=1,sort=nearest] feet run function rpg:taint/sk1b_thrust
# Lucifer mesh appearance (add_lucifer_model.py)
execute if entity @s[tag=rpg.lu,tag=!rpg.lu.phase2] run function rpg:lucifer_lord/skill/sk1_2
