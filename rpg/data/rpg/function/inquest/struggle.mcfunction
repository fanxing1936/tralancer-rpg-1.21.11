execute store result score @s rpg_ex_struggle run random value 120..180
function rpg:inquest/stability/hit5
particle gust ~ ~0.8 ~ 2.5 0.35 2.5 0.08 45 normal
playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.65 0.55
tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"〖恶魔挣脱〗","color":"#C04A3C","bold":true,"italic":false},{"text":" 𝔘𝔫𝔟𝔬𝔲𝔫𝔡","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"法阵边界承受冲击，稳定度下降。","color":"#9C9A94","italic":false}]
