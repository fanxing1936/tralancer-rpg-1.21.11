# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/5_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m23
# 死亡低语 —— 死亡天使开口，不必碰到你。
playsound minecraft:entity.wither.spawn hostile @a[distance=..32] ~ ~ ~ 0.8 1.6
particle soul_fire_flame ~ ~1 ~ 3 1 3 0.05 80
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/sk5c_whisper
# 萨麦尔外观（add_samael_model.py）
execute if entity @s[tag=rpg.sml] run function rpg:samael_lord/skill/sk5_3
