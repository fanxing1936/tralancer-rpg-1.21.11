# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/2_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m10
# 海渊重压 —— 不需要海水，深度本身压在骨头上。
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..32] ~ ~ ~ 1 0.42
particle bubble_pop ~ ~1 ~ 4 1.4 4 0.18 120
particle dust_color_transition{from_color:[0.24,0.66,0.91],to_color:[0.02,0.09,0.18],scale:2.5} ~ ~1 ~ 4 1 4 0.04 72
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk2e_pressure
