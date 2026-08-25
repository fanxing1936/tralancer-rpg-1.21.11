execute as @e[type=minecraft:item,tag=rpg.counter.food,distance=..6,limit=1,sort=nearest] run function rpg:inquest/tool/consume
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run data merge entity @s {Health:455f}
function rpg:inquest/stability/hit10
tag @e[type=minecraft:item,tag=rpg.counter.food,distance=..6] remove rpg.counter.food
particle item{item:{id:"minecraft:poisonous_potato"}} ~ ~1 ~ 0.8 0.6 0.8 0.08 35 normal
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·吞媒] ","color":"#DCEB72","bold":true,"italic":false},{"text":"别西卜吞下一件地面媒介并恢复生命。","color":"gray","italic":false}]
tag @s remove rpg.rite.anchor.active
