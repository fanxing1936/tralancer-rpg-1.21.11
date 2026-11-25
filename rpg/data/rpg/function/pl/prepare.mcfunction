# 新地形（BUILT 10）要连同重置维度一起用：散落的小建筑重放一遍
execute unless score #built rpg_pl matches 10 run scoreboard players set #sites rpg_pl 0
scoreboard players set #built rpg_pl 1
execute in rpg:paradise_lost positioned 0 83 0 run forceload add -32 -32 40 40
execute in rpg:paradise_lost positioned 0 83 0 run forceload add -56 -176 56 -64
execute in rpg:paradise_lost positioned 0 83 0 run forceload add 64 -56 176 56
execute in rpg:paradise_lost positioned 0 83 0 run forceload add -56 64 56 176
execute in rpg:paradise_lost positioned 0 83 0 run forceload add -176 -56 -64 56
schedule function rpg:pl/build/all 100t
