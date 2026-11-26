# 灯灭（as/at 灯）
scoreboard players set @s rpg_dt_lt 0
setblock ~ ~5 ~ minecraft:air
playsound minecraft:block.candle.extinguish block @a[distance=..40] ~ ~3 ~ 1 0.6
particle minecraft:smoke ~ ~3.8 ~ 0.2 0.3 0.2 0.02 12
