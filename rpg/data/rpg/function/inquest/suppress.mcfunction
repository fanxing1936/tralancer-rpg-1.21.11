scoreboard players set @s rpg_ex_stage 1
data merge entity @s {Health:420f}
effect give @s minecraft:resistance 2 4 true
title @a[distance=..18,gamemode=!spectator] times 10 50 15
title @a[distance=..18,gamemode=!spectator] title ["",{"text":"Ⅰ · 镇　压","color":"#DAA520","bold":true,"italic":false}]
title @a[distance=..18,gamemode=!spectator] subtitle ["",{"text":"肉身已伏 · 真名与法阵缺一不可","color":"gray","italic":false}]
tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"[镇压] ","color":"#DAA520","bold":true,"italic":false},{"text":"恶魔被锁在 420 / 700 生命；完成调查并点燃驱魔图腾。","color":"gray","italic":false}]
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..28] ~ ~ ~ 1 0.55
