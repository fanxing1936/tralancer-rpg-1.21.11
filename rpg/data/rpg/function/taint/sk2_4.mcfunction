# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/2_4
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m9
# 逆潮 —— 近者被推离，远者被卷近，所有距离都由他重写。
playsound minecraft:entity.generic.splash hostile @a[distance=..32] ~ ~ ~ 1.2 0.65
playsound minecraft:block.conduit.attack.target hostile @a[distance=..32] ~ ~ ~ 0.8 0.7
particle nautilus ~ ~1 ~ 4 1.2 4 0.12 80
particle bubble_column_up ~ ~0.4 ~ 4 0.5 4 0.35 80
execute as @e[tag=rpg.unit.f,distance=..4] at @s run function rpg:taint/sk2d_out
execute as @e[tag=rpg.unit.f,distance=4.01..10] at @s run function rpg:taint/sk2d_in
# 利维坦外观（add_leviathan_model.py）
execute if entity @s[tag=rpg.lv] run function rpg:leviathan/skill/sk2_4
