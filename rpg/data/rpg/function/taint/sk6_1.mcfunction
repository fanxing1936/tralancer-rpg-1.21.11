# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/6_1
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m26
# 朝拜 —— 七格之内，全都得低头。
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[0.85,0.48,0.85],to_color:[0.36,0.17,0.44],scale:2} ~ ~1 ~ 3 1.2 3 0.06 80
execute as @e[tag=rpg.unit.f,distance=..7] run function rpg:taint/sk6_kneel
# 贝利尔外观（add_belial_model.py）
execute if entity @s[tag=rpg.bll] run function rpg:belial_lord/skill/sk6_1
