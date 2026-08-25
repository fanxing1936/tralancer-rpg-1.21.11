# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/5_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m21
# 毒雾 —— 剧毒与凋零并存。
playsound minecraft:entity.witch.throw hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.24,0.0,0.12],scale:3} ~ ~1 ~ 3 1.2 3 0.06 100
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5_hit
