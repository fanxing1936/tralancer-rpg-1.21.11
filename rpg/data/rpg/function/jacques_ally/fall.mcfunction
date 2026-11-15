# 死亡保护被吃掉：他倒下，1.5 秒后消失（敌人不再把他当目标）。
tag @s add rpg.jqa.down
tag @s remove rpg.unit
tag @s remove rpg.unit.ns
tag @s remove rpg.unit.nc
tag @s remove rpg.unit.f
data merge entity @s {Invulnerable:1b}
scoreboard players set @s rpg_al_mt 0
function rpg:jacques/weapon/glaive
function rpg:jacques/anim/enter/fall
tellraw @a[distance=..32] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……抱歉，只能到这里了。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:entity.player.death player @a[distance=..32] ~ ~ ~ 1 0.8
