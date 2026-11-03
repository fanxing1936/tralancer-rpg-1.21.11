tag @s remove rpg.rite.nailed
scoreboard players add @a[distance=..10,gamemode=!spectator] rpg_ex_xp 3
particle end_rod ~ ~0.5 ~ 1.8 0.25 1.8 0.04 55 normal
playsound minecraft:item.shield.block player @a[distance=..18] ~ ~ ~ 1 0.75
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"〖银钉守界〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣钉替法阵承受了暴怒的一击。","color":"#9C9A94","italic":false}]
