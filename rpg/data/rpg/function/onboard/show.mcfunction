tag @s remove rpg.ob.wait
# 新手流程里不再问要不要看序章（用户 2026-11-23）：停在这一步的老存档直接去名字卡
execute if score @s rpg_ob matches 16 run scoreboard players set @s rpg_ob 3
execute if score @s rpg_ob matches 17 run return run function rpg:onboard/intro/start
# 旁白之后的流程都配同一首曲子
execute unless score @s rpg_ob_mi matches 2 run function rpg:onboard/music/flow
# 序章排队中：没有对话框，等调度把人接走
execute if score @s rpg_ob matches 1 run return run dialog clear @s
execute if score @s rpg_ob matches 2 run return run function rpg:onboard/name/show
execute if score @s rpg_ob matches 3 run return run function rpg:onboard/card/show
execute if score @s rpg_ob matches 4 run return run function rpg:onboard/ident/ask
execute if score @s rpg_ob matches 5 run return run function rpg:onboard/ident/show
execute if score @s rpg_ob matches 6 run return run function rpg:onboard/tut/weapon
execute if score @s rpg_ob matches 7 run return run function rpg:onboard/tut/made_show
execute if score @s rpg_ob matches 8 run return run function rpg:onboard/tut/wash
execute if score @s rpg_ob matches 9 run return run function rpg:onboard/tut/wash_show
execute if score @s rpg_ob matches 10 run return run function rpg:onboard/tut/gild
execute if score @s rpg_ob matches 11 run return run function rpg:onboard/tut/gild_show
execute if score @s rpg_ob matches 12 run return run function rpg:onboard/tut/inlay
execute if score @s rpg_ob matches 13 run return run function rpg:onboard/tut/runes
execute if score @s rpg_ob matches 14 run return run function rpg:onboard/tut/stones
execute if score @s rpg_ob matches 15 run return run function rpg:onboard/tut/end
