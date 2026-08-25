# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/2_3
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m8
# 嫉羡 —— 你身上那些好东西，他也想要。
playsound minecraft:entity.elder_guardian.hurt hostile @a[distance=..32] ~ ~ ~ 1 1.2
particle witch ~ ~1 ~ 3 1 3 0.3 80
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk2c_envy
