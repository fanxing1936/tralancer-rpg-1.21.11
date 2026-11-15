# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/2_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m8
# 嫉羡 —— 你身上那些好东西，他也想要。
playsound minecraft:entity.elder_guardian.hurt hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle witch ~ ~1 ~ 3 1 3 0.3 80
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk2c_envy
# 利维坦外观（add_leviathan_model.py）
execute if entity @s[tag=rpg.lv] run function rpg:leviathan/skill/sk2_3
