# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/6_5
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m30
# 欲障 —— 紫幕落下，真实与渴望只剩一层薄纱。
playsound minecraft:block.respawn_anchor.ambient hostile @a[distance=..32] ~ ~ ~ 1 0.55
particle portal ~ ~1 ~ 4 1.5 4 0.55 80
particle reverse_portal ~ ~1 ~ 3.5 1.2 3.5 0.25 80
execute as @e[tag=rpg.unit.f,distance=..10] run function rpg:taint/sk6e_veil
# 贝利尔外观（add_belial_model.py）
execute if entity @s[tag=rpg.bll] run function rpg:belial_lord/skill/sk6_5
