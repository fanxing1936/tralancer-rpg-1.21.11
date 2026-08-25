# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m4
# 失坠 —— 王冠之下不许任何人保有自己的高度。
playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1 0.55
playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..32] ~ ~ ~ 0.7 1.45
particle dragon_breath ~ ~1.5 ~ 3 1.2 3 0.08 72
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:2.2} ~ ~1 ~ 3 1 3 0.04 54
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk1d_fall
