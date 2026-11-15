# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/4_5
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m20
# 饥啮 —— 万千张口只追最近的一份血肉。
playsound minecraft:entity.fox.bite hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle ash ~ ~1 ~ 2.5 1 2.5 0.14 80
particle damage_indicator ~ ~1 ~ 2 0.8 2 0.08 36
execute as @e[tag=rpg.unit.f,distance=..10,limit=1,sort=nearest] run function rpg:taint/sk4e_bite
# 别西卜外观（add_beelzebub.py）
execute if entity @s[tag=rpg.bz] run function rpg:beelzebub/skill/sk4_5
