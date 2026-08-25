# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/7_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m33
# 重金一击 —— 一次结清。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.levelup hostile @a[distance=..24] ~ ~ ~ 0.8 0.6
particle flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~1 ~ 1 1 1 0.4 60
execute as @a[distance=..5,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk7c_settle
