# 工作台总页（as/at 玩家）
scoreboard players set #i rpg_fg 30
scoreboard players set #found rpg_fg 0
execute anchored eyes positioned ^ ^ ^ run function rpg:forge/smelt/ray
execute if score #found rpg_fg matches 0 run return run tellraw @s ["",{"text":"[工作台] ","color":"#E39745","bold":true,"italic":false},{"text":"对准灵魂营火右键","color":"#FF6B5E","bold":false,"italic":false}]
scoreboard players enable @s rpg_fg_do
scoreboard players set @s rpg_fg_op 10
scoreboard players set @s rpg_fg_arg -1
playsound minecraft:block.campfire.crackle player @s ~ ~ ~ 1 0.8
execute store result storage rpg:bench d.nb int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"blank"}] 0
execute store result storage rpg:bench d.ns int 1 run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute store result storage rpg:bench d.nf int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"forge_stone"}] 0
execute store result storage rpg:bench d.nw int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"wash_gem"}] 0
execute store result storage rpg:bench d.ng int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"gild_leaf"}] 0
execute store result storage rpg:bench d.nk int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"sin_shard"}] 0
execute store result storage rpg:bench d.np int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"bp_frag"}] 0
execute store result storage rpg:bench d.nv int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"vial"}] 0
execute store result storage rpg:bench d.nt int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"blank_rite"}] 0
function rpg:bench/home_m with storage rpg:bench d
