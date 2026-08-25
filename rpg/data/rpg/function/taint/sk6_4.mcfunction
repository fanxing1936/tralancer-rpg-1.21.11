# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/6_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m29
# 顾盼 —— 一个眼神就把所有人的视线强行转向王座。
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.65
particle witch ~ ~1.4 ~ 4 1.4 4 0.18 105
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:2.4} ~ ~1 ~ 4 1 4 0.05 72
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk6d_gaze
