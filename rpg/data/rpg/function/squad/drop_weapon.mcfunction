# 原版没有"让实体丢下手里那件"的命令，所以先召一个占位掉落物，
# 再把他的装备整份写进去。
execute at @s run summon minecraft:item ~ ~1 ~ {Tags:["rpg.sq.drop"],Item:{id:"minecraft:stone",count:1}}
data modify entity @e[type=minecraft:item,tag=rpg.sq.drop,limit=1,sort=nearest] Item set from entity @s equipment.mainhand
tag @e[type=minecraft:item,tag=rpg.sq.drop] remove rpg.sq.drop
item replace entity @s weapon.mainhand with air
