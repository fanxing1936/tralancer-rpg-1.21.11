# 血怒天罚 —— 死亡天使沿最近的血气突入人群。
execute at @s facing entity @e[tag=rpg.unit.f,limit=1,sort=nearest] feet run tp @s ^ ^ ^5
particle flash{color:16735314} ~ ~1 ~ 0 0 0 0 1 normal
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:3} ~ ~1 ~ 4 1.2 4 0.06 72 normal
particle sweep_attack ~ ~1 ~ 3 0.8 3 0 34 normal
particle trial_omen ~ ~1 ~ 4 1 4 0.1 72 normal
particle crit ~ ~1 ~ 4 1 4 0.22 72 normal
playsound minecraft:entity.ravager.roar hostile @a[distance=..36] ~ ~ ~ 1.2 0.8
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 1.15
execute as @e[tag=rpg.unit.f,distance=..8] run function rpg:taint/ult5_hit
# 萨麦尔外观（add_samael_model.py）
execute if entity @s[tag=rpg.sml] run function rpg:samael_lord/skill/ult5
