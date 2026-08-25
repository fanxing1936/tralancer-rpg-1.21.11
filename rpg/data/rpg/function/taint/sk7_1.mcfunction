# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/7_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m31
# 点金 —— 他不打你，他从你身上抽。
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..32] ~ ~ ~ 1 1.4
particle wax_on ~ ~1 ~ 3 1 3 0.1 80
particle end_rod ~ ~1 ~ 2 1 2 0.05 40
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk7_take
