# 死亡低语 —— 死亡天使开口，不必碰到你。
playsound minecraft:entity.wither.spawn hostile @a[distance=..32] ~ ~ ~ 0.8 1.6
particle soul_fire_flame ~ ~1 ~ 3 1 3 0.05 80
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk5c_whisper
