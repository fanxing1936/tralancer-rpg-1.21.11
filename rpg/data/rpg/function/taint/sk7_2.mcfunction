# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/7_2
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m32
# 夺财 —— 掉在地上的也是他的。
playsound minecraft:entity.item.pickup hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle wax_off ~ ~1 ~ 4 1 4 0.2 80
execute at @s as @e[type=minecraft:item,distance=..10] run function rpg:taint/sk7b_seize
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:inquest/seal/ability/record_magic
execute as @e[tag=rpg.unit.f,distance=..8] run damage @s 3 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
# 玛门外观（add_mammon_model.py）
execute if entity @s[tag=rpg.mml] run function rpg:mammon_lord/skill/sk7_2
