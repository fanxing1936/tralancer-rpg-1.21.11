# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/5_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m24
# 血猎 —— 他循着最近的血气突入，不给伤者喘息。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.55
playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 0.8 1.15
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:2} ~ ~1 ~ 3 1 3 0.06 80
execute at @s facing entity @a[distance=..12,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run tp @s ^ ^ ^5
execute as @a[distance=..5,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5d_hunt
