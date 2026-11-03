# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/5_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m21
# 毒雾 —— 剧毒与凋零并存。
playsound minecraft:entity.witch.throw hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:2} ~ ~1 ~ 3 1.2 3 0.06 80
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5_hit
