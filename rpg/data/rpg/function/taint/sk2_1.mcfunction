# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/2_1
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m6
# 沉锚 —— 锚落处涌起漩涡，把人拖向锚心。
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle bubble_column_up ~ ~0.5 ~ 2 0.5 2 0.4 80
particle dust{color:[0.31,0.62,0.94],scale:2} ~ ~1 ~ 2 1 2 0.05 60
execute as @e[tag=rpg.unit.f,distance=..8] at @s facing entity @e[tag=rpg.dm.cast,limit=1] feet run tp @s ^ ^ ^1.2
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:inquest/seal/ability/record_magic
execute as @e[tag=rpg.unit.f,distance=..8] run damage @s 5 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
# 利维坦外观（add_leviathan_model.py）
execute if entity @s[tag=rpg.lv] run function rpg:leviathan/skill/sk2_1
