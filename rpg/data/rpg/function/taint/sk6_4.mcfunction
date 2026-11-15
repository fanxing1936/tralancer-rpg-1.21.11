# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/6_4
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m29
# 顾盼 —— 一个眼神就把所有人的视线强行转向王座。
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.65
particle witch ~ ~1.4 ~ 4 1.4 4 0.18 80
particle dust_color_transition{from_color:[0.85,0.48,0.85],to_color:[0.36,0.17,0.44],scale:2} ~ ~1 ~ 4 1 4 0.05 72
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk6d_gaze
# 贝利尔外观（add_belial_model.py）
execute if entity @s[tag=rpg.bll] run function rpg:belial_lord/skill/sk6_4
