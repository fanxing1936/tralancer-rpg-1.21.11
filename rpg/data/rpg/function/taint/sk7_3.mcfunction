# 重金一击 —— 一次结清。
playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..32] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.levelup hostile @a[distance=..24] ~ ~ ~ 0.8 0.6
particle flash{color:16777200} ~ ~1 ~ 0 0 0 0 1
particle end_rod ~ ~1 ~ 1 1 1 0.4 60
execute as @a[distance=..5,limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk7c_settle
