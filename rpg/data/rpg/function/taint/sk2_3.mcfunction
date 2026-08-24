# 嫉羡 —— 你身上那些好东西，他也想要。
playsound minecraft:entity.elder_guardian.hurt hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle witch ~ ~1 ~ 3 1 3 0.3 80
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk2c_envy
