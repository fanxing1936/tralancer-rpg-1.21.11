# 罪的蔓延：把原罪递给最近的一个尚且干净的邻居
execute as @e[distance=0.1..4,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,tag=!rpg.luci.sin,limit=1,sort=nearest] at @s run function rpg:item/extra/lucifer_bite
particle dust_color_transition{from_color:2257486,to_color:14344834,scale:1} ~ ~0.9 ~ 1.6 0.6 1.6 0.02 30
