# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/2_4
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m9
# 逆潮 —— 近者被推离，远者被卷近，所有距离都由他重写。
playsound minecraft:entity.generic.splash hostile @a[distance=..32] ~ ~ ~ 1.2 0.65
playsound minecraft:block.conduit.attack.target hostile @a[distance=..32] ~ ~ ~ 0.8 0.7
particle nautilus ~ ~1 ~ 4 1.2 4 0.12 96
particle bubble_column_up ~ ~0.4 ~ 4 0.5 4 0.35 110
execute as @a[distance=..4,gamemode=!spectator,gamemode=!creative] at @s run function rpg:taint/sk2d_out
execute as @a[distance=4.01..10,gamemode=!spectator,gamemode=!creative] at @s run function rpg:taint/sk2d_in
