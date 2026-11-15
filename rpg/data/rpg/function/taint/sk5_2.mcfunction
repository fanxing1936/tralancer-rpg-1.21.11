# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/5_2
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m22
# 怒斩 —— 暴怒不讲章法，它只是冲上来。
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle crit ~ ~1 ~ 1 1 1 0.3 60
execute at @s facing entity @e[tag=rpg.unit.f,limit=1,sort=nearest] feet run tp @s ^ ^ ^4
execute as @e[tag=rpg.unit.f,distance=..6] run function rpg:taint/sk5b_slash
# 萨麦尔外观（add_samael_model.py）
execute if entity @s[tag=rpg.sml] run function rpg:samael_lord/skill/sk5_2
