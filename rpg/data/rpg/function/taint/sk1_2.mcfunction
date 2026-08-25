# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_2
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m2
# 蛇矛 —— 一记贯穿，连着把人钉退。
playsound minecraft:entity.breeze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk1b_thrust
