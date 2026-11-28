scoreboard players operation #do rpg_ob = @s rpg_ob_do
scoreboard players set @s rpg_ob_do 0
# 旁白里聊天栏的「跳过」
execute if score #do rpg_ob matches 98 if score @s rpg_ob matches 17 run return run function rpg:onboard/intro/end
execute if score #do rpg_ob matches 98 run return 0
execute if score #do rpg_ob matches 99 run return run function rpg:onboard/show
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 0.55 1.2
execute if score @s rpg_ob matches 2 run return run function rpg:onboard/name/press
execute if score @s rpg_ob matches 3 run return run function rpg:onboard/card/press
execute if score @s rpg_ob matches 4 run return run function rpg:onboard/ident/draw
execute if score @s rpg_ob matches 5 run return run function rpg:onboard/tut/start
execute if score @s rpg_ob matches 6 run return run function rpg:onboard/tut/weapon_press
execute if score @s rpg_ob matches 7 run return run function rpg:onboard/tut/to_wash
execute if score @s rpg_ob matches 8 run return run function rpg:onboard/tut/wash_roll
execute if score @s rpg_ob matches 9 run return run function rpg:onboard/tut/wash_pick
execute if score @s rpg_ob matches 10 run return run function rpg:onboard/tut/gild_do
execute if score @s rpg_ob matches 11 run return run function rpg:onboard/tut/to_inlay
execute if score @s rpg_ob matches 12 run return run function rpg:onboard/tut/inlay_press
execute if score @s rpg_ob matches 13 run return run function rpg:onboard/tut/rune_press
execute if score @s rpg_ob matches 14 run return run function rpg:onboard/tut/stone_press
execute if score @s rpg_ob matches 15 run return run function rpg:onboard/pro/enter
