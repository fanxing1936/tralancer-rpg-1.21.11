execute if score #t rpg_pf matches 20 run function rpg:pope_fight/stage1_spawn
execute if score #t rpg_pf matches ..20 run return 0
execute store result bossbar minecraft:pope value if entity @e[type=minecraft:vindicator,tag=rpg.pf.unit]
execute store result score #hud rpg_pf if entity @e[type=minecraft:vindicator,tag=rpg.pf.unit]
execute unless score #hud rpg_pf = #hudl rpg_pf run function rpg:pope_fight/bar/guard
execute unless entity @e[type=minecraft:vindicator,tag=rpg.pf.unit,limit=1] run function rpg:pope_fight/stage2_enter
