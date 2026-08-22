# 砸地。热浪不是一片持续的场，而是三次定时脉冲 ——
# 计数器一到零整段就结束，没有任何东西留在场上每刻跑。
scoreboard players set @s rpg_forge_chg 0
scoreboard players set @s rpg_forge 24
particle minecraft:flash{color:16553767} ~ ~0.6 ~ 0 0 0 0 1
particle lava ~ ~0.3 ~ 0.6 0.1 0.6 0 30
playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:block.lava.extinguish player @a[distance=..20] ~ ~ ~ 1 0.7
