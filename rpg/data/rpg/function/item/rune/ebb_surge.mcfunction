# 回涌：再生与抗性各 6 秒，然后压 30 秒冷却。
scoreboard players set @s rpg_rune_ebb 600
effect give @s minecraft:regeneration 6 1 true
effect give @s minecraft:resistance 6 0 true
particle dust_color_transition{from_color:[0.31,0.66,0.78],to_color:[0.85,0.95,1.0],scale:2} ~ ~1 ~ 0.5 0.8 0.5 0.05 50
particle splash ~ ~1 ~ 0.5 0.6 0.5 0.3 30
playsound minecraft:block.conduit.activate player @a[distance=..16] ~ ~ ~ 1 1.3
