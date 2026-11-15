# 弩光往前走（每 1 格一步，最多 24 步），碰到目标就结算
scoreboard players add #d rpg_al 1
particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.2} ~ ~ ~ 0.02 0.02 0.02 0 1
# 弩光朝目标的眼睛飞，目标的位置在脚底：在弩光下方 1.2 格处量
execute positioned ~ ~-1.2 ~ if entity @e[tag=rpg.al.aim,distance=..1.5] run return run function rpg:jacques_ally/hit/bolt_hit
execute if entity @e[tag=rpg.al.aim,distance=..1.2] run return run function rpg:jacques_ally/hit/bolt_hit
execute unless block ~ ~ ~ #minecraft:replaceable run return 0
execute if score #d rpg_al matches ..24 positioned ^ ^ ^1 run function rpg:jacques_ally/hit/fly
