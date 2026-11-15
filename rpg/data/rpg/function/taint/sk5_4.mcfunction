# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @e[tag=rpg.unit.ns,tag=rpg.holy,distance=..18] run function rpg:inquest/clue/5_4
execute at @s as @e[tag=rpg.unit.f,distance=..14] run function rpg:hud/demon/m24
# 血猎 —— 他循着最近的血气突入，不给伤者喘息。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.55
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 0.8 1.15
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:2} ~ ~1 ~ 3 1 3 0.06 80
execute at @s facing entity @e[tag=rpg.unit.f,distance=..12,limit=1,sort=nearest] feet run tp @s ^ ^ ^5
execute as @e[tag=rpg.unit.f,distance=..5] run function rpg:taint/sk5d_hunt
# 萨麦尔外观（add_samael_model.py）
execute if entity @s[tag=rpg.sml] run function rpg:samael_lord/skill/sk5_4
