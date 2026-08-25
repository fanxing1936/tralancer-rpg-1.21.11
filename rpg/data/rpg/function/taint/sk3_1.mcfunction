# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/3_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m11
# 收割 —— 周身爆发，每收一个回一颗心。
playsound minecraft:entity.wither.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5
particle sculk_charge_pop ~ ~1 ~ 3 1 3 0.1 90
execute as @a[distance=..6,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk3_reap
