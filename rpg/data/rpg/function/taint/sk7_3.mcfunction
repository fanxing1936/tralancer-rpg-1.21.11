# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/7_3
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m33
# 重金一击 —— 一次结清。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.levelup hostile @a[distance=..24] ~ ~ ~ 0.8 0.6
particle flash{color:16777215} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~1 ~ 1 1 1 0.3 60
execute as @e[tag=rpg.unit.f,distance=..5,limit=1,sort=nearest] run function rpg:taint/sk7c_settle
# 玛门外观（add_mammon_model.py）
execute if entity @s[tag=rpg.mml] run function rpg:mammon_lord/skill/sk7_3
