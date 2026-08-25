# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m3
# 高踞 —— 傲慢把人举起来，再让他自己摔下去。
playsound minecraft:entity.illusioner.prepare_blindness hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle end_rod ~ ~1 ~ 3 1 3 0.1 60
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk1c_lift
