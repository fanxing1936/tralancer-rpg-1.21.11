execute if entity @e[tag=rpg.lu2f.fx,limit=1] as @e[tag=rpg.lu2f.fx] run function rpg:lucifer_fight/fx_life
scoreboard players add #clock rpg_l2_t 1
execute if score #clock rpg_l2_t matches 20.. run function rpg:lucifer_fight/minion/sweep
