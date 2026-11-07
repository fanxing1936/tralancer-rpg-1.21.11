# 战场中心（as、at 标记）。
scoreboard players add #t rpg_pf 1
scoreboard players add #s rpg_pf 1
execute if score #s rpg_pf matches 20.. run function rpg:pope_fight/second
scoreboard players remove #bgm rpg_pf 1
execute if score #bgm rpg_pf matches ..0 run function rpg:pope_fight/bgm/again
execute if score #stage rpg_pf matches 1 run return run function rpg:pope_fight/stage1
execute if score #stage rpg_pf matches 2 run return run function rpg:pope_fight/stage2
execute if score #stage rpg_pf matches 3 run return run function rpg:pope_fight/stage3
execute if score #stage rpg_pf matches 4 run return run function rpg:pope_fight/stage4
execute if score #stage rpg_pf matches 5 run return run function rpg:pope_fight/stage5
