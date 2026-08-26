# 派蒙 · 咒使（利维坦）：海渊重压
scoreboard players add #casts rpg_mn_tick 1
scoreboard players set @s rpg_mn_cd 104
scoreboard players set @s rpg_mn_cast 20
tag @s add rpg.demon.minion.casting
tellraw @a[distance=..8,gamemode=!spectator] ["",{"text":"[罪仆术式] ","color":"#1B4F72","bold":true,"italic":false},{"text":"派蒙 · ","color":"#62D9E8","bold":false,"italic":false},{"text":"海渊重压","color":"#62D9E8","bold":true,"italic":false},{"text":"｜咒使","color":"gray","bold":false,"italic":false},{"text":"　倒影令众人迟滞而失明","color":"dark_gray","bold":false,"italic":false}]
playsound minecraft:entity.guardian.attack hostile @a[distance=..20] ~ ~ ~ 0.35 1.12
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.28 0.92
particle dust_color_transition{from_color:[0.25,0.78,0.93],to_color:[0.02,0.16,0.31],scale:1.05} ~ ~1 ~ 0.55 0.7 0.55 0.03 4
particle nautilus ~8 ~0.18 ~0 0 0 0 0 1
particle nautilus ~-8 ~0.18 ~0 0 0 0 0 1
particle nautilus ~0 ~0.18 ~8 0 0 0 0 1
particle nautilus ~0 ~0.18 ~-8 0 0 0 0 1
particle nautilus ~5.6 ~0.18 ~5.6 0 0 0 0 1
particle nautilus ~-5.6 ~0.18 ~5.6 0 0 0 0 1
particle nautilus ~5.6 ~0.18 ~-5.6 0 0 0 0 1
particle nautilus ~-5.6 ~0.18 ~-5.6 0 0 0 0 1
