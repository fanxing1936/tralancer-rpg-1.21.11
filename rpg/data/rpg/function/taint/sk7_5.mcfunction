# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/7_5
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m35
# 金牢 —— 黄金不是奖赏，是把脚钉在账本上的铆钉。
playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 0.8 1.35
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.75
particle end_rod ~ ~1 ~ 3 1 3 0.08 72
particle wax_on ~ ~0.5 ~ 3 0.5 3 0.12 88
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk7e_prison
