# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/5_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m23
# 死亡低语 —— 死亡天使开口，不必碰到你。
playsound minecraft:entity.wither.spawn hostile @a[distance=..32] ~ ~ ~ 0.8 1.6
particle soul_fire_flame ~ ~1 ~ 3 1 3 0.05 80
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5c_whisper
