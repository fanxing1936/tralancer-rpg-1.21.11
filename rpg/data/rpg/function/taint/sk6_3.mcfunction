# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/6_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m28
# 献身 —— 他要的从来不是你的命，是你的血。
playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle dust{color:[0.36,0.17,0.44],scale:2} ~ ~1 ~ 3 1 3 0.1 90
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk6c_drain
