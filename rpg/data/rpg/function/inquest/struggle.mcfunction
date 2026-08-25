execute store result score @s rpg_ex_struggle run random value 120..180
function rpg:inquest/stability/hit5
particle gust ~ ~0.8 ~ 2.5 0.35 2.5 0.08 45 force
playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.65 0.55
tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"[恶魔挣脱] ","color":"#FF6B5E","bold":true,"italic":false},{"text":"法阵边界承受冲击，稳定度下降。","color":"gray","italic":false}]
